'use strict';

const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const { performance } = require('perf_hooks');

const WAIT_BUFFER = new Int32Array(new SharedArrayBuffer(4));

function sameIdentity(left, right) {
  return left.dev === right.dev && left.ino === right.ino;
}

function processIsAlive(pid) {
  try { process.kill(pid, 0); return true; }
  catch (error) { return error.code !== 'ESRCH'; }
}

function inspectLock(lockPath, fileSystem) {
  let descriptor;
  try {
    descriptor = fileSystem.openSync(lockPath, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
    const identity = fileSystem.fstatSync(descriptor, { bigint: true });
    if (!identity.isFile() || identity.size > 4096n) return null;
    const raw = fileSystem.readFileSync(descriptor, 'utf8');
    const current = fileSystem.lstatSync(lockPath, { bigint: true });
    if (current.isSymbolicLink() || !current.isFile() || !sameIdentity(identity, current)) return null;
    let metadata;
    try { metadata = JSON.parse(raw); } catch (_error) { metadata = null; }
    return { identity, metadata };
  } catch (error) {
    if (error.code === 'ENOENT') return null;
    throw error;
  } finally {
    if (descriptor !== undefined) fileSystem.closeSync(descriptor);
  }
}

function removeLockIfOwned(lockPath, expectedIdentity, fileSystem) {
  let descriptor;
  try {
    descriptor = fileSystem.openSync(lockPath, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
    const opened = fileSystem.fstatSync(descriptor, { bigint: true });
    const current = fileSystem.lstatSync(lockPath, { bigint: true });
    if (!opened.isFile() || current.isSymbolicLink() || !sameIdentity(opened, expectedIdentity)
      || !sameIdentity(current, expectedIdentity)) return false;
    const descriptorToClose = descriptor;
    descriptor = undefined;
    fileSystem.closeSync(descriptorToClose);
    const finalPath = fileSystem.lstatSync(lockPath, { bigint: true });
    if (!finalPath.isFile() || finalPath.isSymbolicLink() || !sameIdentity(finalPath, expectedIdentity)) return false;
    fileSystem.unlinkSync(lockPath);
    return true;
  } catch (error) {
    if (error.code === 'ENOENT' || error.code === 'ELOOP') return false;
    throw error;
  } finally {
    if (descriptor !== undefined) fileSystem.closeSync(descriptor);
  }
}

function createLock(lockPath, fileSystem, label) {
  const temporaryPath = `${lockPath}.tmp-${process.pid}-${crypto.randomBytes(8).toString('hex')}`;
  let descriptor = fileSystem.openSync(temporaryPath, 'wx', 0o600);
  let identity = null;
  try {
    identity = fileSystem.fstatSync(descriptor, { bigint: true });
    fileSystem.writeFileSync(descriptor, `${JSON.stringify({
      pid: process.pid,
      hostname: os.hostname(),
      startedAt: new Date().toISOString(),
      token: crypto.randomBytes(16).toString('hex'),
    })}\n`);
    fileSystem.fsyncSync(descriptor);
  } catch (error) {
    try { fileSystem.closeSync(descriptor); }
    finally { fileSystem.unlinkSync(temporaryPath); }
    throw error;
  }
  const descriptorToClose = descriptor;
  descriptor = undefined;
  let linked = false;
  let primaryError;
  try {
    fileSystem.closeSync(descriptorToClose);
    fileSystem.linkSync(temporaryPath, lockPath);
    linked = true;
  } catch (error) {
    primaryError = error;
  }
  try { fileSystem.unlinkSync(temporaryPath); }
  catch (error) { if (!primaryError) primaryError = error; }
  if (primaryError) {
    if (linked) {
      try { removeLockIfOwned(lockPath, identity, fileSystem); }
      catch (_cleanupError) { /* Keep the original acquisition error. */ }
    }
    throw primaryError;
  }

  let released = false;
  return () => {
    if (released) return;
    released = true;
    const current = fileSystem.lstatSync(lockPath, { bigint: true });
    if (!current.isFile() || current.isSymbolicLink() || !sameIdentity(current, identity)) {
      throw new Error(`${label} lock changed while held: ${lockPath}`);
    }
    const finalPath = fileSystem.lstatSync(lockPath, { bigint: true });
    if (!finalPath.isFile() || finalPath.isSymbolicLink() || !sameIdentity(finalPath, identity)) {
      throw new Error(`${label} lock changed while releasing: ${lockPath}`);
    }
    fileSystem.unlinkSync(lockPath);
  };
}

function isStaleLock(observed, isOwnerAlive) {
  if (!observed) return false;
  const metadata = observed.metadata;
  if (metadata && typeof metadata.hostname === 'string' && metadata.hostname !== os.hostname()) return false;
  if (metadata
    && Number.isSafeInteger(metadata.pid) && metadata.pid > 1) {
    return !isOwnerAlive(metadata.pid);
  }
  return false;
}

function pathExists(lockPath, fileSystem) {
  try { fileSystem.lstatSync(lockPath); return true; }
  catch (error) { if (error.code === 'ENOENT') return false; throw error; }
}

function waitForRetry(deadline, label, lockPath, retryablePermissionError = false) {
  const remaining = deadline - performance.now();
  if (remaining <= 0) {
    if (retryablePermissionError) {
      const error = new Error(`${label} lock could not be opened: ${lockPath}`);
      error.code = 'EPERM';
      throw error;
    }
    const error = new Error(`${label} is busy; inspect ${lockPath} before recovering a stale lock.`);
    error.code = 'PROCESS_LOCK_BUSY';
    throw error;
  }
  Atomics.wait(WAIT_BUFFER, 0, 0, Math.min(25, remaining));
}

function acquireProcessLock(lockPath, { fileSystem = fs, timeoutMs = 5000, label = 'Operation', isProcessAlive: isOwnerAlive = processIsAlive } = {}) {
  const deadline = performance.now() + timeoutMs;
  const recoveryPath = `${lockPath}.reclaim`;
  for (;;) {
    let waitPath = lockPath;
    let waitLabel = label;
    if (pathExists(recoveryPath, fileSystem)) {
      waitForRetry(deadline, `${label} recovery`, recoveryPath);
      continue;
    }

    let retryablePermissionError = false;
    try {
      const release = createLock(lockPath, fileSystem, label);
      if (!pathExists(recoveryPath, fileSystem)) return release;
      release();
      waitForRetry(deadline, `${label} recovery`, recoveryPath);
      continue;
    }
    catch (error) {
      if (error.code === 'EEXIST') {
        const observed = inspectLock(lockPath, fileSystem);
        if (observed && isStaleLock(observed, isOwnerAlive)) {
          let releaseRecovery;
          try { releaseRecovery = createLock(recoveryPath, fileSystem, `${label} recovery`); }
          catch (recoveryError) {
            if (recoveryError.code !== 'EEXIST') throw recoveryError;
            waitPath = recoveryPath;
            waitLabel = `${label} recovery`;
          }
          if (releaseRecovery) {
            try {
              const current = inspectLock(lockPath, fileSystem);
              if (current && isStaleLock(current, isOwnerAlive)
                && removeLockIfOwned(lockPath, current.identity, fileSystem)) continue;
            } finally { releaseRecovery(); }
          }
        }
      } else if (process.platform === 'win32' && error.code === 'EPERM') {
        retryablePermissionError = true;
      } else throw error;
    }

    waitForRetry(deadline, waitLabel, waitPath, retryablePermissionError);
  }
}

module.exports = { acquireProcessLock };
