from pathlib import Path
import re
import unittest


SCRIPT = (
    Path(__file__).parents[1]
    / "tools"
    / "windows"
    / "P205_FT_Excel_Native_Recalc_v1_2.ps1"
)


class P205ExcelScriptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = SCRIPT.read_text(encoding="utf-8")

    def test_parameters_are_mandatory(self) -> None:
        for name in ("InputXlsx", "OutputDirectory", "ExpectedSha256"):
            self.assertRegex(
                self.text,
                rf"\[Parameter\(Mandatory = \$true\)\][\s\S]{{0,160}}\${name}\b",
            )

    def test_uninitialized_source_variable_is_absent(self) -> None:
        self.assertIsNone(re.search(r"\$source\b", self.text, re.IGNORECASE))
        self.assertIn("$sourcePath = [IO.Path]::GetFullPath($InputXlsx)", self.text)
        self.assertIn("Workbooks.Open($sourcePath, 0, $true)", self.text)

    def test_fail_closed_and_source_is_immutable(self) -> None:
        required = (
            "Set-StrictMode -Version Latest",
            "E_SOURCE_HASH_MISMATCH",
            "E_SOURCE_MUTATED",
            "$sourceWorkbook.SaveCopyAs($copyPath)",
            "Workbooks.Open($copyPath, 0, $false)",
            "$excel.CalculateFullRebuild()",
            "$copyWorkbook.Save()",
            "$copyWorkbook.Close($true)",
        )
        for token in required:
            self.assertIn(token, self.text)

    def test_cleanup_and_audit_report_are_mandatory(self) -> None:
        for token in (
            "finally {",
            "$excel.Quit()",
            "FinalReleaseComObject",
            "source_sha256_before",
            "output_sha256",
            "source_unchanged",
            "Set-Content -LiteralPath $reportPath",
        ):
            self.assertIn(token, self.text)


if __name__ == "__main__":
    unittest.main()
