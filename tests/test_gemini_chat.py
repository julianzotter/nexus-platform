import shutil
import subprocess
import unittest
from pathlib import Path

TEST = Path(__file__).resolve().parents[1] / "prototypes" / "gemini-chat" / "test" / "server.test.mjs"


@unittest.skipUnless(shutil.which("node"), "node not available")
class GeminiChatServerTests(unittest.TestCase):
    def test_node_suite(self):
        res = subprocess.run(["node", "--test", str(TEST)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main()
