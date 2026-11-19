#!/usr/bin/env python3
"""AGY CLI Session Pruner — Autonomous Maintenance Engine.

Prunes historical session databases, execution steps, and task logs older
than a configurable threshold (default 2 days) to prevent disk head contention
and bloat on mechanical drives.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
import os
from pathlib import Path
import shutil
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

DEFAULT_BASE = Path.home() / ".gemini" / "antigravity-cli"
DEFAULT_CONVERSATIONS = DEFAULT_BASE / "conversations"
DEFAULT_BRAIN = DEFAULT_BASE / "brain"
DEFAULT_ANNOTATIONS = DEFAULT_BASE / "annotations"
DEFAULT_SUMMARIES_DB = DEFAULT_BASE / "conversation_summaries.db"
SAFETY_BUFFER_MINUTES = 120


def get_dir_size(target_dir: Path) -> int:
    """Recursively calculate total bytes in a directory tree."""
    total = 0
    if not target_dir.is_dir():
        return 0
    for root, _, files in os.walk(target_dir):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total


def find_expired_sessions(
    conv_dir: Path,
    brain_dir: Path,
    cutoff_time: datetime,
    safe_time: datetime,
    active_ids: Set[str],
) -> Set[str]:
    """Identify conversation IDs whose last modification exceeds the cutoff."""
    candidates: Set[str] = set()

    # Scan conversations directory
    if conv_dir.is_dir():
        for db_file in conv_dir.glob("*.db"):
            uuid = db_file.stem
            if uuid in active_ids:
                continue
            try:
                mtime = datetime.fromtimestamp(db_file.stat().st_mtime)
                if mtime >= safe_time:
                    continue
                if mtime < cutoff_time:
                    candidates.add(uuid)
            except OSError:
                pass

    # Scan brain directory
    if brain_dir.is_dir():
        for session_folder in brain_dir.iterdir():
            if not session_folder.is_dir() or session_folder.name in active_ids:
                continue
            try:
                mtime = datetime.fromtimestamp(session_folder.stat().st_mtime)
                if mtime >= safe_time:
                    continue
                if mtime < cutoff_time:
                    candidates.add(session_folder.name)
            except OSError:
                pass

    return candidates


def delete_expired_records(
    uuids: Set[str],
    conv_dir: Path,
    brain_dir: Path,
    annot_dir: Path,
    dry_run: bool = False,
) -> Tuple[int, int]:
    """Delete database files, brain directories, and annotations for expired sessions."""
    deleted_files = 0
    reclaimed_bytes = 0

    for u in uuids:
        # 1. Database file
        db_path = conv_dir / f"{u}.db"
        if db_path.is_file():
            try:
                reclaimed_bytes += db_path.stat().st_size
                deleted_files += 1
                if not dry_run:
                    db_path.unlink()
            except OSError:
                pass

        # 2. Annotation protobuf
        ann_path = annot_dir / f"{u}.pbtxt"
        if ann_path.is_file():
            try:
                reclaimed_bytes += ann_path.stat().st_size
                deleted_files += 1
                if not dry_run:
                    ann_path.unlink()
            except OSError:
                pass

        # 3. Brain directory tree
        b_path = brain_dir / u
        if b_path.is_dir():
            try:
                for root, _, files in os.walk(b_path):
                    for f in files:
                        deleted_files += 1
                        try:
                            reclaimed_bytes += os.path.getsize(os.path.join(root, f))
                        except OSError:
                            pass
                if not dry_run:
                    shutil.rmtree(b_path)
            except OSError:
                pass

    return deleted_files, reclaimed_bytes


def purge_intermediate_outputs(
    brain_dir: Path,
    preserved_ids: Set[str],
    dry_run: bool = False,
) -> Tuple[int, int]:
    """Purge heavy raw execution steps and tasks from completed past sessions."""
    purged_files = 0
    reclaimed_bytes = 0

    if not brain_dir.is_dir():
        return 0, 0

    for session_dir in brain_dir.iterdir():
        if not session_dir.is_dir() or session_dir.name in preserved_ids:
            continue
        for subfolder in ("steps", "tasks"):
            target_path = session_dir / ".system_generated" / subfolder
            if target_path.is_dir():
                try:
                    for root, _, files in os.walk(target_path):
                        for f in files:
                            purged_files += 1
                            try:
                                reclaimed_bytes += os.path.getsize(os.path.join(root, f))
                            except OSError:
                                pass
                    if not dry_run:
                        shutil.rmtree(target_path)
                except OSError:
                    pass

    return purged_files, reclaimed_bytes


def vacuum_databases(
    summaries_db: Path,
    conv_dir: Path,
    deleted_uuids: Set[str],
    dry_run: bool = False,
) -> int:
    """Clean expired IDs from the summaries index and defragment remaining SQLite files."""
    if dry_run:
        return 0

    vacuumed = 0
    if summaries_db.is_file():
        try:
            conn = sqlite3.connect(str(summaries_db))
            cur = conn.cursor()
            for u in deleted_uuids:
                cur.execute("DELETE FROM conversation_summaries WHERE conversation_id = ?", (u,))
            conn.commit()
            cur.execute("VACUUM")
            conn.close()
            vacuumed += 1
        except Exception:
            pass

    if conv_dir.is_dir():
        for db_file in conv_dir.glob("*.db"):
            try:
                conn = sqlite3.connect(str(db_file))
                conn.execute("VACUUM")
                conn.close()
                vacuumed += 1
            except Exception:
                pass

    return vacuumed


def run_prune(
    retention_days: float = 2.0,
    conv_dir: Path = DEFAULT_CONVERSATIONS,
    brain_dir: Path = DEFAULT_BRAIN,
    annot_dir: Path = DEFAULT_ANNOTATIONS,
    summaries_db: Path = DEFAULT_SUMMARIES_DB,
    active_ids: Optional[Set[str]] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Execute end-to-end pruning of stale AGY CLI session data."""
    now = datetime.now()
    cutoff_time = now - timedelta(days=retention_days)
    safe_time = now - timedelta(minutes=SAFETY_BUFFER_MINUTES)
    active = set(active_ids or [])

    # Include environment conversation ID if present
    env_id = os.environ.get("CONVERSATION_ID", "").strip()
    if env_id:
        active.add(env_id)

    expired_uuids = find_expired_sessions(conv_dir, brain_dir, cutoff_time, safe_time, active)
    del_files, del_bytes = delete_expired_records(expired_uuids, conv_dir, brain_dir, annot_dir, dry_run=dry_run)

    preserved = active | expired_uuids
    purge_files, purge_bytes = purge_intermediate_outputs(brain_dir, preserved, dry_run=dry_run)

    vacuumed_count = vacuum_databases(summaries_db, conv_dir, expired_uuids, dry_run=dry_run)

    total_files = del_files + purge_files
    total_bytes = del_bytes + purge_bytes

    return {
        "retention_days": retention_days,
        "cutoff_timestamp": cutoff_time.isoformat(),
        "expired_sessions_count": len(expired_uuids),
        "total_files_removed": total_files,
        "reclaimed_bytes": total_bytes,
        "reclaimed_mb": round(total_bytes / (1024 * 1024), 2),
        "databases_vacuumed": vacuumed_count,
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune old AGY CLI sessions and execution buffers.")
    parser.add_argument("--days", type=float, default=2.0, help="Retention window in days (default: 2.0)")
    parser.add_argument("--dry-run", action="store_true", help="Calculate reclaimable space without deleting")
    parser.add_argument("--conv-dir", type=Path, default=DEFAULT_CONVERSATIONS, help="Conversations directory")
    parser.add_argument("--brain-dir", type=Path, default=DEFAULT_BRAIN, help="Brain directory")
    parser.add_argument("--annot-dir", type=Path, default=DEFAULT_ANNOTATIONS, help="Annotations directory")
    parser.add_argument("--summaries-db", type=Path, default=DEFAULT_SUMMARIES_DB, help="Summaries SQLite database")
    parser.add_argument("--active-id", type=str, action="append", default=[], help="Session ID to exclude from pruning")
    parser.add_argument("--quiet", action="store_true", help="Suppress console summary")
    args = parser.parse_args()

    results = run_prune(
        retention_days=args.days,
        conv_dir=args.conv_dir,
        brain_dir=args.brain_dir,
        annot_dir=args.annot_dir,
        summaries_db=args.summaries_db,
        active_ids=set(args.active_id),
        dry_run=args.dry_run,
    )

    if not args.quiet:
        prefix = "[DRY RUN] " if results["dry_run"] else ""
        print(f"{prefix}AGY CLI Session Prune (Retention: {results['retention_days']} days)")
        print(f"Expired Sessions:    {results['expired_sessions_count']}")
        print(f"Total Files Removed: {results['total_files_removed']}")
        print(f"Reclaimed Space:     {results['reclaimed_mb']} MB")
        print(f"Databases Vacuumed:  {results['databases_vacuumed']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
