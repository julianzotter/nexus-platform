import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class WorkflowCouplingTests(unittest.TestCase):
    """The delivery workflow is triggered by the monitor workflow name; a rename must not break it silently."""

    def test_monitor_name_matches_delivery_trigger(self):
        monitor = re.search(r"^name:\s*(.+?)\s*$", read(".github/workflows/nexus-monitor.yml"), re.M).group(1)
        delivery = read(".github/workflows/nexus-delivery.yml")
        self.assertIn(f"workflows: [{monitor}]", delivery)

    def test_delivery_script_expects_same_workflow(self):
        monitor = re.search(r"^name:\s*(.+?)\s*$", read(".github/workflows/nexus-monitor.yml"), re.M).group(1)
        script = read("tools/deliver_work.py")
        self.assertIn(f"'{monitor}'", script)
        self.assertIn(".github/workflows/nexus-monitor.yml", script)


if __name__ == "__main__":
    unittest.main()
