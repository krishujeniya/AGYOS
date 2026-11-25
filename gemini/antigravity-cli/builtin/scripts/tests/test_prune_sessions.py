"""Tests for AGY CLI session pruning engine."""

from datetime import datetime, timedelta
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest

from scripts.prune_sessions import (
    find_expired_sessions,
    delete_expired_records,
    purge_intermediate_outputs,
    vacuum_databases,
    run_prune,
)


class PruneSessionsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)
        self.conv_dir = self.base / "conversations"
        self.brain_dir = self.base / "brain"
        self.annot_dir = self.base / "annotations"
        self.summaries_db = self.base / "conversation_summaries.db"

        self.conv_dir.mkdir(parents=True)
        self.brain_dir.mkdir(parents=True)
        self.annot_dir.mkdir(parents=True)

        # Initialize test summaries database
        conn = sqlite3.connect(str(self.summaries_db))
        conn.execute("CREATE TABLE conversation_summaries (conversation_id TEXT PRIMARY KEY, summary TEXT)")
        conn.execute("INSERT INTO conversation_summaries VALUES ('session-old', 'Old summary')")
        conn.execute("INSERT INTO conversation_summaries VALUES ('session-recent', 'Recent summary')")
        conn.execute("INSERT INTO conversation_summaries VALUES ('session-active', 'Active summary')")
        conn.commit()
        conn.close()

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_mock_session(self, uuid: str, age_days: float) -> None:
        """Create a mock session with specific modification timestamp."""
        # Database
        db_path = self.conv_dir / f"{uuid}.db"
        conn = sqlite3.connect(str(db_path))
        conn.execute("CREATE TABLE test (id INT, val TEXT)")
        conn.execute("INSERT INTO test VALUES (1, 'hello')")
        conn.commit()
        conn.close()

        # Annotation
        ann_path = self.annot_dir / f"{uuid}.pbtxt"
        ann_path.write_text(f"id: '{uuid}'\n", encoding="utf-8")

        # Brain directory
        brain_sub = self.brain_dir / uuid / ".system_generated"
        (brain_sub / "steps").mkdir(parents=True)
        (brain_sub / "tasks").mkdir(parents=True)
        (brain_sub / "logs").mkdir(parents=True)
        (brain_sub / "steps" / "output.txt").write_text("step output", encoding="utf-8")
        (brain_sub / "tasks" / "task-1.log").write_text("task log", encoding="utf-8")
        (brain_sub / "logs" / "transcript.jsonl").write_text("transcript", encoding="utf-8")

        # Set modification timestamps
        mtime = (datetime.now() - timedelta(days=age_days)).timestamp()
        os.utime(db_path, (mtime, mtime))
        os.utime(ann_path, (mtime, mtime))
        os.utime(self.brain_dir / uuid, (mtime, mtime))

    def test_find_and_delete_expired_sessions(self):
        self._create_mock_session("session-old", age_days=5.0)
        self._create_mock_session("session-recent", age_days=0.5)
        self._create_mock_session("session-active", age_days=0.1)

        result = run_prune(
            retention_days=2.0,
            conv_dir=self.conv_dir,
            brain_dir=self.brain_dir,
            annot_dir=self.annot_dir,
            summaries_db=self.summaries_db,
            active_ids={"session-active"},
            dry_run=False,
        )

        self.assertEqual(result["expired_sessions_count"], 1)
        self.assertFalse((self.conv_dir / "session-old.db").exists())
        self.assertFalse((self.brain_dir / "session-old").exists())
        self.assertFalse((self.annot_dir / "session-old.pbtxt").exists())

        # Verify recent and active are preserved
        self.assertTrue((self.conv_dir / "session-recent.db").exists())
        self.assertTrue((self.conv_dir / "session-active.db").exists())
        self.assertTrue((self.brain_dir / "session-recent").exists())
        self.assertTrue((self.brain_dir / "session-active").exists())

        # Verify index deletion in summaries db
        conn = sqlite3.connect(str(self.summaries_db))
        rows = [r[0] for r in conn.execute("SELECT conversation_id FROM conversation_summaries").fetchall()]
        conn.close()
        self.assertNotIn("session-old", rows)
        self.assertIn("session-recent", rows)
        self.assertIn("session-active", rows)

    def test_safety_buffer_protects_freshly_updated_sessions(self):
        # A session modified 10 minutes ago must never be deleted even with days=0
        self._create_mock_session("session-just-now", age_days=0.005)

        result = run_prune(
            retention_days=0.0,
            conv_dir=self.conv_dir,
            brain_dir=self.brain_dir,
            annot_dir=self.annot_dir,
            summaries_db=self.summaries_db,
            dry_run=False,
        )

        self.assertEqual(result["expired_sessions_count"], 0)
        self.assertTrue((self.conv_dir / "session-just-now.db").exists())

    def test_dry_run_does_not_mutate_files(self):
        self._create_mock_session("session-old", age_days=10.0)

        result = run_prune(
            retention_days=2.0,
            conv_dir=self.conv_dir,
            brain_dir=self.brain_dir,
            annot_dir=self.annot_dir,
            summaries_db=self.summaries_db,
            dry_run=True,
        )

        self.assertEqual(result["expired_sessions_count"], 1)
        self.assertTrue(result["dry_run"])
        # Files must still exist on disk
        self.assertTrue((self.conv_dir / "session-old.db").exists())
        self.assertTrue((self.brain_dir / "session-old").exists())


if __name__ == "__main__":
    unittest.main()
