"""Non-destructive single-main-branch rollback contract tests."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "bin" / "rollback.sh"

@unittest.skipUnless(shutil.which("git"), "git not available")
class SafeRollbackTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        (self.repo / "bin").mkdir()
        shutil.copy2(SCRIPT, self.repo / "bin" / "rollback.sh")
        self.git("init")
        self.git("checkout", "-b", "main")
        self.git("config", "user.name", "AGYOS Test")
        self.git("config", "user.email", "test@example.invalid")
        (self.repo / "sample.txt").write_text("first\n")
        self.git("add", "-A")
        self.git("commit", "-m", "first")
        (self.repo / "sample.txt").write_text("second\n")
        self.git("add", "-A")
        self.git("commit", "-m", "second")

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True, capture_output=True, text=True,
        ).stdout.strip()

    def rollback(self, *args):
        return subprocess.run(
            ["bash", str(self.repo / "bin" / "rollback.sh"), *args],
            text=True, capture_output=True,
        )

    def test_default_and_invalid_invocations_do_not_write(self):
        old = self.git("rev-parse", "HEAD")
        self.assertEqual(self.rollback().returncode, 0)
        self.assertEqual(self.rollback("--plan").returncode, 0)
        self.assertNotEqual(self.rollback("--apply").returncode, 0)
        self.assertNotEqual(self.rollback("--apply", "--commit", "HEAD~1").returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), old)

    def test_dirty_worktree_refuses_without_deleting_user_files(self):
        private = self.repo / "private-work.txt"
        private.write_text("do not delete")
        result = self.rollback("--apply", "--commit", "HEAD")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(private.read_text(), "do not delete")

    def test_clean_explicit_revert_creates_new_commit_on_main(self):
        old = self.git("rev-parse", "HEAD")
        result = self.rollback("--apply", "--commit", "HEAD")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.repo / "sample.txt").read_text(), "first\n")
        self.assertNotEqual(self.git("rev-parse", "HEAD"), old)
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual(self.git("branch", "--list").replace("*", "").strip(), "main")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_other_branch_refuses(self):
        self.git("checkout", "-b", "other")
        self.assertNotEqual(self.rollback("--apply", "--commit", "HEAD").returncode, 0)

if __name__ == "__main__":
    unittest.main()
