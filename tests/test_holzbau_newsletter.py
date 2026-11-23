import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_holzbau_newsletter import TOPICS, validate_text

MATRIX = "\n".join(f"| {t} | – | – | – | – | – |" for t in TOPICS)
GOOD = f"""---
name: metawissenholzbau-newsletter-KW46-2026
description: Wochen-Newsletter Holzbau
version: 1
status: erstellt
timestamp: 2026-11-10T16:00 (Europe/Vienna)
zeitraum: 2026-11-03 bis 2026-11-10
---
# METAWISSEN HOLZBAU – KW46/2026

## TL;DR
- Punkt

## QUICK-TOPIC-MATRIX
| Thema | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|
{MATRIX}

## MELDUNGEN
### S2 Holzbau Austria
- #1 [NORM] Titel (09.11.2026) – Kernaussage

## TERMINE & FRISTEN
- 12.11.2026 – Webinar – online – #1

## REFERENZEN
#1, HBA-Fakten, https://www.holzbauaustria.at/news.html

## LOG
- Lauf: 2026-11-10T16:00
"""


class HolzbauNewsletterTests(unittest.TestCase):
    def test_complete_newsletter_passes(self):
        self.assertEqual(validate_text(GOOD), [])

    def test_item_without_reference_fails(self):
        errors = validate_text(GOOD.replace("#1, HBA-Fakten", "#2, HBA-Fakten"))
        self.assertIn("item #1: no reference line", errors)

    def test_missing_section_matrix_row_and_frontmatter_fail(self):
        broken = GOOD.replace("## LOG\n", "").replace("| MARKT |", "| XX |").replace("zeitraum:", "zr:")
        errors = validate_text(broken)
        self.assertIn("section missing: ## LOG", errors)
        self.assertIn("matrix row missing: MARKT", errors)
        self.assertIn("frontmatter key missing: zeitraum", errors)

    def test_malformed_reference_and_unknown_topic_fail(self):
        errors = validate_text(GOOD.replace("[NORM]", "[FOO]").replace("https://", "www."))
        self.assertTrue(any("unknown topic FOO" in e for e in errors))
        self.assertTrue(any(e.startswith("reference line not") for e in errors))

    def test_cli_reports_no_data_and_fail_exit_codes(self):
        script = str(ROOT / "tools/validate_holzbau_newsletter.py")
        with tempfile.TemporaryDirectory() as directory:
            empty = subprocess.run([sys.executable, script, directory], capture_output=True, text=True)
            self.assertEqual(empty.returncode, 2)
            self.assertIn("NO_DATA", empty.stdout)
            path = Path(directory) / "26_11_10_METAWISSENHOLZBAU_NEWSLETTER_KW46.md"
            path.write_text(GOOD, encoding="utf-8")
            self.assertEqual(subprocess.run([sys.executable, script, directory]).returncode, 0)
            path.write_text("no frontmatter", encoding="utf-8")
            self.assertEqual(subprocess.run([sys.executable, script, directory]).returncode, 1)


if __name__ == "__main__":
    unittest.main()
