import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import fitz
import openpyxl


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def run_script(script_name: str, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPTS_DIR / script_name), *args]
    return subprocess.run(command, capture_output=True, text=True, env=env, cwd=PROJECT_ROOT)


class KnowledgeBaseCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name)
        self.fake_home = self.root / "home"
        self.fake_home.mkdir()
        self.env = os.environ.copy()
        self.env["HOME"] = str(self.fake_home)

    def test_kb_config_and_init_flow(self) -> None:
        kb_path = self.root / "kb"

        check_before = run_script("kb_config.py", "--check", env=self.env)
        self.assertEqual(check_before.returncode, 0, check_before.stderr)
        self.assertFalse(json.loads(check_before.stdout)["configured"])

        set_result = run_script("kb_config.py", "--set", str(kb_path), env=self.env)
        self.assertEqual(set_result.returncode, 0, set_result.stderr)
        self.assertEqual(json.loads(set_result.stdout)["kb_path"], str(kb_path.resolve()))

        init_result = run_script("kb_init.py", str(kb_path), env=self.env)
        self.assertEqual(init_result.returncode, 0, init_result.stderr)
        self.assertTrue((kb_path / "README.md").exists())
        self.assertTrue((kb_path / "FAQ.md").exists())
        self.assertTrue((kb_path / "BADCASE.md").exists())
        self.assertTrue((kb_path / "contents_overview").exists())

    def test_kb_migrate_copies_existing_files(self) -> None:
        original_kb = self.root / "kb"
        migrated_kb = self.root / "kb-migrated"

        run_script("kb_config.py", "--set", str(original_kb), env=self.env)
        run_script("kb_init.py", str(original_kb), env=self.env)
        (original_kb / "notes.md").write_text("# Note\n", encoding="utf-8")

        migrate_result = run_script("kb_config.py", "--migrate", str(migrated_kb), env=self.env)
        self.assertEqual(migrate_result.returncode, 0, migrate_result.stderr)
        payload = json.loads(migrate_result.stdout)
        self.assertEqual(payload["kb_path"], str(migrated_kb.resolve()))
        self.assertTrue((migrated_kb / "notes.md").exists())
        self.assertTrue((original_kb / "notes.md").exists())

    def test_complexity_analyzer_reports_standard_sheet(self) -> None:
        workbook_path = self.root / "sample.xlsx"
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Data"
        sheet.append(["name", "value"])
        sheet.append(["alpha", 1])
        sheet.append(["beta", 2])
        workbook.save(workbook_path)

        result = run_script("complexity_analyzer.py", str(workbook_path), env=self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["sheets"]["Data"]["recommended_strategy"], "pandas")

    def test_smart_convert_converts_digital_pdf(self) -> None:
        pdf_path = self.root / "digital.pdf"
        document = fitz.open()
        page = document.new_page()
        page.insert_text((72, 72), "Knowledge Base Skill PDF Test")
        document.save(pdf_path)
        document.close()

        result = run_script("smart_convert.py", str(pdf_path), "--json-output", env=self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["success"])
        markdown_path = Path(payload["markdown_file"])
        self.assertTrue(markdown_path.exists())
        self.assertIn("Knowledge Base Skill PDF Test", markdown_path.read_text(encoding="utf-8"))

    def test_smart_convert_flags_scanned_pdf_for_ocr(self) -> None:
        pdf_path = self.root / "scan.pdf"
        document = fitz.open()
        page = document.new_page()
        page.insert_text((72, 72), "OCR route")
        document.save(pdf_path)
        document.close()

        result = run_script("smart_convert.py", str(pdf_path), "--force-ocr", "--json-output", env=self.env)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["success"])
        self.assertTrue(payload["needs_ocr"])
        self.assertTrue(payload["scanned"])


if __name__ == "__main__":
    unittest.main()
