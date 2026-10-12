# Automated Persona Export & Privacy Tests
# Covers REQ-5.1, REQ-5.2, REQ-5.3, REQ-5.4

import os
import sys
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import json
import os
import shutil
import subprocess
import tempfile
import unittest

from tools.export_persona import export_persona, scan_secrets

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXPORTER_PS1 = os.path.join(REPO_DIR, 'exporter', 'export-persona.ps1')
FIXTURE_PATH = os.path.join(REPO_DIR, 'exporter', 'test-fixture.md')

class TestPersonaExport(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix='digi_persona_test_')

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_python_export_standard_fixture(self):
        out_jsonl = os.path.join(self.test_dir, 'py_pairs.jsonl')
        quar_jsonl = os.path.join(self.test_dir, 'py_pairs.quarantine.jsonl')
        stats = export_persona(FIXTURE_PATH, out_jsonl, schema_ver='v1', quarantine_path=quar_jsonl)

        # Expected: written=1, skipped=2, quarantined=1
        self.assertEqual(stats['written'], 1)
        self.assertEqual(stats['skipped'], 2)
        self.assertEqual(stats['quarantined'], 1)

        # Validate valid record
        with open(out_jsonl, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record['schema'], 'digi-brain-divergence-pair-v1')
            self.assertEqual(record['date'], '2026-10-11')
            self.assertIn('Link the NOW card', record['twin_pick'])

        # Validate quarantine record
        self.assertTrue(os.path.exists(quar_jsonl))
        with open(quar_jsonl, 'r', encoding='utf-8') as f:
            q_lines = f.readlines()
            self.assertEqual(len(q_lines), 1)
            q_rec = json.loads(q_lines[0])
            self.assertIn('Pattern matched', q_rec['reason'])

    def test_v2_schema_export_with_scope(self):
        out_jsonl = os.path.join(self.test_dir, 'v2_pairs.jsonl')
        stats = export_persona(FIXTURE_PATH, out_jsonl, schema_ver='v2')
        self.assertEqual(stats['written'], 1)
        with open(out_jsonl, 'r', encoding='utf-8') as f:
            record = json.loads(f.readline())
            self.assertEqual(record['schema'], 'digi-brain-divergence-pair-v2')
            self.assertEqual(record['scope'], 'project')
            self.assertEqual(record['review_status'], 'verified')

    def test_unicode_and_escaping_survives_jsonl(self):
        custom_fixture = os.path.join(self.test_dir, 'custom_fixture.md')
        special_pick = 'Use \'quotes\', "double quotes", and emoji ?? with backslash \\'
        special_corr = 'Keep it purely functional: line1\\nline2 & tab\\t'
        with open(custom_fixture, 'w', encoding='utf-8') as f:
            f.write('# Divergence Table\n\n')
            f.write('| Date | Twin\'s pick | Owner\'s correction | Lesson |\n')
            f.write('|---|---|---|---|\n')
            f.write(f'| 2026-10-12 | {special_pick} | {special_corr} | Unicode Lesson |\n')

        out_jsonl = os.path.join(self.test_dir, 'unicode_pairs.jsonl')
        stats = export_persona(custom_fixture, out_jsonl)
        self.assertEqual(stats['written'], 1)

        with open(out_jsonl, 'r', encoding='utf-8') as f:
            rec = json.loads(f.readline())
            self.assertEqual(rec['twin_pick'], special_pick)
            self.assertEqual(rec['owner_correction'], special_corr)

    def test_parity_between_python_and_powershell(self):
        py_out = os.path.join(self.test_dir, 'py_parity.jsonl')
        ps_out = os.path.join(self.test_dir, 'ps_parity.jsonl')

        # Run Python exporter
        export_persona(FIXTURE_PATH, py_out, schema_ver='v1')

        # Run PowerShell exporter
        cmd = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', EXPORTER_PS1,
               '-InputPath', FIXTURE_PATH, '-Out', ps_out, '-Schema', 'v1']
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f'PowerShell export failed: {res.stderr}')

        # Parse both JSONL files and compare records
        with open(py_out, 'r', encoding='utf-8') as f:
            py_records = [json.loads(line) for line in f if line.strip()]
        with open(ps_out, 'r', encoding='utf-8') as f:
            ps_records = [json.loads(line) for line in f if line.strip()]

        self.assertEqual(len(py_records), len(ps_records))
        self.assertEqual(py_records[0]['pair_id'], ps_records[0]['pair_id'])
        self.assertEqual(py_records[0]['twin_pick'], ps_records[0]['twin_pick'])
        self.assertEqual(py_records[0]['owner_correction'], ps_records[0]['owner_correction'])

if __name__ == '__main__':
    unittest.main()
