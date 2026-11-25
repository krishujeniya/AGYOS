import { describe, test, expect } from "bun:test";
import { mkdirSync, writeFileSync, rmSync } from "fs";
import { resolve } from "path";
import { buildContextBundle, dispatchWithRetries, summarizeDispatchStage } from "../src/council";

const tmpDir = resolve(import.meta.dir, ".tmp-council-test");

describe("buildContextBundle security", () => {
  // Create a temp repo-like directory with a test file
  const repoRoot = resolve(tmpDir, "repo");
  const safeFile = "src/hello.ts";

  test("setup", () => {
    mkdirSync(resolve(repoRoot, "src"), { recursive: true });
    writeFileSync(resolve(repoRoot, safeFile), "console.log('hello');");
  });

  test("accepts safe relative paths", () => {
    const result = buildContextBundle([safeFile], repoRoot);
    expect(result).toContain("console.log");
    expect(result).not.toContain("rejected");
  });

  test("rejects absolute paths", () => {
    const result = buildContextBundle(["/etc/passwd"], repoRoot);
    expect(result).toContain("rejected: absolute paths not allowed");
  });

  test("rejects directory traversal with ..", () => {
    const result = buildContextBundle(["../../etc/passwd"], repoRoot);
    expect(result).toContain("rejected: directory traversal not allowed");
  });

  test("rejects hidden traversal in middle of path", () => {
    const result = buildContextBundle(["src/../../../etc/passwd"], repoRoot);
    expect(result).toContain("rejected: directory traversal not allowed");
  });

  test("rejects sensitive file extensions", () => {
    const exts = [".key", ".pem", ".env", ".secret", ".token"];
    for (const ext of exts) {
      const result = buildContextBundle([`config${ext}`], repoRoot);
      expect(result).toContain("rejected: sensitive file type");
    }
  });

  test("handles missing files gracefully", () => {
    const result = buildContextBundle(["nonexistent.ts"], repoRoot);
    expect(result).toContain("file not found");
  });

  test("handles empty file list", () => {
    const result = buildContextBundle([], repoRoot);
    expect(result).toBe("");
  });

  test("cleanup", () => {
    rmSync(tmpDir, { recursive: true, force: true });
  });
});

describe("council dispatch retry state", () => {
  test("uses the configured retry count for transient failures", async () => {
    let attempts = 0;
    const result = await dispatchWithRetries(async () => {
      attempts += 1;
      return {
        agent: "codex",
        status: attempts < 3 ? "error" : "ok",
        structured: attempts === 3,
        response: attempts === 3 ? "done" : "",
        error_class: attempts < 3 ? "timeout" : undefined,
        duration_ms: 1,
        timestamp: new Date().toISOString(),
      };
    }, 2, 0);
    expect(attempts).toBe(3);
    expect(result.status).toBe("ok");
  });

  test("does not retry non-transient failures", async () => {
    let attempts = 0;
    const result = await dispatchWithRetries(async () => {
      attempts += 1;
      return {
        agent: "codex",
        status: "error",
        structured: false,
        response: "",
        error_class: "auth",
        duration_ms: 1,
        timestamp: new Date().toISOString(),
      };
    }, 4, 0);
    expect(attempts).toBe(1);
    expect(result.error_class).toBe("auth");
  });
});

describe("council quorum stage state", () => {
  const agentResult = (status: "ok" | "error" | "timeout", error?: string) => ({
    agent: "codex" as const,
    status,
    structured: status === "ok",
    response: status === "ok" ? "response" : "",
    error,
    duration_ms: 1,
    timestamp: new Date().toISOString(),
  });

  test("records a complete stage when quorum is met and all agents returned", () => {
    const summary = summarizeDispatchStage([
      agentResult("ok"), agentResult("ok"), agentResult("ok"),
    ], 3);
    expect(summary.status).toBe("complete");
    expect(summary.quorumMet).toBe(true);
    expect(summary.successfulAgents).toBe(3);
  });

  test("records grace expiry while retaining a satisfied quorum", () => {
    const summary = summarizeDispatchStage([
      agentResult("ok"),
      agentResult("ok"),
      agentResult("timeout", "Skipped (quorum reached, grace period expired)"),
    ], 3);
    expect(summary.status).toBe("grace-expired");
    expect(summary.reason).toBe("grace-period-expired");
    expect(summary.quorumMet).toBe(true);
  });

  test("records failure when completed responses do not reach quorum", () => {
    const summary = summarizeDispatchStage([
      agentResult("ok"), agentResult("error"), agentResult("timeout", "agent timeout"),
    ], 3);
    expect(summary.status).toBe("quorum-failed");
    expect(summary.quorumMet).toBe(false);
  });
});
