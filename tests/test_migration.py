# Automated Migration & Backward Compatibility Tests
# Covers REQ-9.1, REQ-12.1

import os
import shutil
import sys
import tempfile
import unittest

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tools.migrate_memory import detect_legacy_format, migrate_agents_directory

class TestMemoryMigration(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix='digi_mig_test_')
        self.agents_dir = os.path.join(self.test_dir, '.agents')
        self.memory_dir = os.path.join(self.agents_dir, 'memory')
        os.makedirs(self.memory_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_legacy_format_detection_and_migration(self):
        # 1. Seed legacy formatted decisions.md and agent-lessons.md
        dec_path = os.path.join(self.memory_dir, 'decisions.md')
        with open(dec_path, 'w', encoding='utf-8') as f:
            f.write("""# Decisions Record\n\n## ADR-001: Legacy Monolith Architecture\n- **Context**: Rapid prototyping.\n- **Decision**: Put all routes in index.js.\n""")

        les_path = os.path.join(self.memory_dir, 'agent-lessons.md')
        with open(les_path, 'w', encoding='utf-8') as f:
            f.write("""# Engineering Lessons\n\n### Lesson 001: Respect the blast radius\n- Every fix gets a neighbor audit.\n""")

        # 2. Verify legacy detection
        det = detect_legacy_format(self.agents_dir)
        self.assertTrue(det['is_legacy'])
        self.assertEqual(len(det['findings']), 2)

        # 3. Perform migration
        res = migrate_agents_directory(self.agents_dir)
        self.assertEqual(res['status'], 'migrated')
        self.assertEqual(res['migrated_entries'], 2)
        self.assertTrue(os.path.isdir(res['backup_path']), 'Safety backup was not created!')

        # 4. Verify migrated decisions content
        with open(dec_path, 'r', encoding='utf-8') as f:
            new_dec = f.read()
            self.assertIn('### [ADR-001] Legacy Monolith Architecture', new_dec)
            self.assertIn('- **Type**: Semantic', new_dec)
            self.assertIn('- **SourceClass**: ExplicitUser', new_dec)
            self.assertIn('- **Status**: Current', new_dec)
            self.assertIn('- **Context**: Rapid prototyping.', new_dec)

        # 5. Verify migrated lessons content
        with open(les_path, 'r', encoding='utf-8') as f:
            new_les = f.read()
            self.assertIn('### [LES-001] Respect the blast radius', new_les)
            self.assertIn('- **Type**: Procedural', new_les)

        # 6. Verify second migration pass is a no-op
        res2 = migrate_agents_directory(self.agents_dir)
        self.assertEqual(res2['status'], 'up_to_date')
        self.assertEqual(res2['migrated_entries'], 0)

if __name__ == '__main__':
    unittest.main()
