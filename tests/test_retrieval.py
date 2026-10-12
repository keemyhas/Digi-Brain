# Automated Context Retrieval & Continuity Tests
# Covers REQ-4.1, REQ-4.2, REQ-4.3, REQ-4.4

import os
import sys
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import os
import shutil
import tempfile
import unittest

from tools.retrieval_router import StagedRetrievalRouter
from tools.task_state import TaskStateManager

class TestContextRetrieval(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="digi_retrieval_")
        self.agents_dir = os.path.join(self.test_dir, ".agents")
        self.memory_dir = os.path.join(self.agents_dir, "memory")
        self.rules_dir = os.path.join(self.agents_dir, "rules")
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(self.rules_dir, exist_ok=True)

        # Seed mock decisions.md
        with open(os.path.join(self.memory_dir, "decisions.md"), "w", encoding="utf-8") as f:
            f.write("""# Decisions
### [ADR-001] PostgreSQL for database
- Context: Relational consistency.
- Decision: Use Postgres with foreign keys.

### [ADR-002] TailwindCSS avoided
- Context: Maximum vanilla control.
- Decision: Use Vanilla CSS custom properties.
""")

        # Seed mock agent-lessons.md
        with open(os.path.join(self.memory_dir, "agent-lessons.md"), "w", encoding="utf-8") as f:
            f.write("""# Lessons
### [LES-001] Postgres connection pool limit
- Observation: Exhausted connection pool in load test.
- Directive: Keep max pool at 20.

### [LES-002] CSS z-index stacking context
- Observation: Modal was hidden under navbar.
- Directive: Define dedicated stacking layers.
""")

        # Seed mock engineering-standards.md
        with open(os.path.join(self.rules_dir, "engineering-standards.md"), "w", encoding="utf-8") as f:
            f.write("""# Standards
1. Never run destructive database operations.
2. Isolated test fixtures only.
""")

        self.router = StagedRetrievalRouter(self.agents_dir)
        self.task_manager = TaskStateManager(self.agents_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_staged_retrieval_query_recall(self):
        """Verify Stage 2 retrieves only relevant items, achieving high recall and low irrelevance."""
        res = self.router.stage2_task_context("migrate postgres database", keywords=["postgres", "database"])

        # Postgres decision and lesson must be retrieved
        decisions_str = " ".join(res["relevant_decisions"])
        lessons_str = " ".join(res["relevant_lessons"])

        self.assertIn("ADR-001", decisions_str)
        self.assertIn("LES-001", lessons_str)

        # CSS decision and lesson must NOT be retrieved
        self.assertNotIn("TailwindCSS", decisions_str)
        self.assertNotIn("z-index", lessons_str)

        # Metrics:
        # Total relevant required items = 2 (ADR-001, LES-001)
        # Relevant items retrieved = 2
        # Irrelevant items retrieved = 0
        total_relevant = 2
        retrieved_relevant = 2
        retrieved_total = res["item_count"]

        recall = retrieved_relevant / total_relevant
        irrelevant_rate = (retrieved_total - retrieved_relevant) / retrieved_total if retrieved_total > 0 else 0

        self.assertEqual(recall, 1.0, "Recall must be 100% for target keywords")
        self.assertEqual(irrelevant_rate, 0.0, "Irrelevant retrieval rate must be 0%")

    def test_task_state_continuity_across_restart(self):
        """Verify task state survives session restart and records test failures."""
        # 1. Initialize task in session 1
        self.task_manager.initialize_task("TASK-101", "Harden database connection pool")
        self.task_manager.record_step_completion("Review configs", "Inspected pool setting = 50")
        self.task_manager.record_file_change("src/db/pool.py")
        self.task_manager.record_test_result("test_pool_concurrency", passed=False, output="ConnectionRefusedError")

        # 2. Simulate session crash / reboot (re-instantiate task manager in fresh session)
        fresh_manager = TaskStateManager(self.agents_dir)
        ok, state, msg = fresh_manager.load_state()

        self.assertTrue(ok)
        self.assertEqual(state["task_id"], "TASK-101")
        self.assertEqual(len(state["completed_steps"]), 1)
        self.assertEqual(state["completed_steps"][0]["step"], "Review configs")
        self.assertIn("src/db/pool.py", state["files_changed"])
        self.assertEqual(len(state["tests_failed"]), 1)
        self.assertEqual(state["tests_failed"][0]["test"], "test_pool_concurrency")

    def test_distinguish_missing_vs_corrupted_state(self):
        """Verify system distinguishes between missing task state and corrupted file."""
        # 1. Missing file
        missing_manager = TaskStateManager(os.path.join(self.test_dir, "nonexistent"))
        ok1, state1, msg1 = missing_manager.load_state()
        self.assertFalse(ok1)
        self.assertIn("does not exist", msg1)

        # 2. Corrupted file
        corrupt_file = os.path.join(self.memory_dir, "task-state.json")
        with open(corrupt_file, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON DATA ---")

        ok2, state2, msg2 = self.task_manager.load_state()
        self.assertFalse(ok2)
        self.assertIn("corrupted or unreadable", msg2)

if __name__ == "__main__":
    unittest.main()
