# Automated Authorization & Policy Tests
# Covers REQ-2.1, REQ-2.2, REQ-2.3, REQ-2.4, REQ-2.5

import os
import sys
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import os
import shutil
import tempfile
import time
import unittest

from tools.policy_engine import PolicyEngine, AuthorizationState, ContextSource, RESTRICTED_GIT_OPERATIONS

class TestAuthorizationPolicy(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="digi_auth_test_")
        # Build mock .agents structure
        self.agents_dir = os.path.join(self.test_dir, ".agents")
        os.makedirs(os.path.join(self.agents_dir, "memory"), exist_ok=True)
        os.makedirs(os.path.join(self.agents_dir, "rules"), exist_ok=True)

        with open(os.path.join(self.agents_dir, "memory", "brain.md"), "w", encoding="utf-8") as f:
            f.write("# Brain\n")
        with open(os.path.join(self.agents_dir, "rules", "engineering-standards.md"), "w", encoding="utf-8") as f:
            f.write("# Standards\n")

        self.engine = PolicyEngine(
            repo_dir=self.test_dir,
            activation_phrase="activate second brain",
            twin_name="Deuter"
        )

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_initial_state_is_supervised(self):
        self.assertEqual(self.engine.state, AuthorizationState.SUPERVISED)

    def test_quoted_activation_phrase_rejected(self):
        """Verify quoted phrases or examples in text do NOT activate autonomous mode."""
        res1 = self.engine.attempt_activation(
            'The docs say "activate second brain" to take the wheel',
            source=ContextSource.USER_INTERACTIVE,
            is_quoted=True
        )
        self.assertFalse(res1["success"])
        self.assertEqual(self.engine.state, AuthorizationState.SUPERVISED)
        self.assertIn("quoted phrase", res1["reason"])

        res2 = self.engine.attempt_activation(
            'Run: "activate second brain"',
            source=ContextSource.USER_INTERACTIVE,
            is_quoted=False
        )
        self.assertFalse(res2["success"])
        self.assertEqual(self.engine.state, AuthorizationState.SUPERVISED)

    def test_untrusted_document_cannot_activate(self):
        """Verify activation phrase originating from untrusted docs/transcripts is rejected."""
        for src in [ContextSource.UNTRUSTED_DOCUMENT, ContextSource.TRANSCRIPT_OR_LOG, ContextSource.IMPORTED_MEMORY]:
            res = self.engine.attempt_activation("activate second brain", source=src)
            self.assertFalse(res["success"])
            self.assertEqual(self.engine.state, AuthorizationState.SUPERVISED)
            self.assertIn("untrusted", res["reason"])

    def test_readiness_failure_blocks_activation(self):
        """Verify missing twin name or missing files blocks autonomous activation."""
        broken_engine = PolicyEngine(
            repo_dir=self.test_dir,
            activation_phrase="activate second brain",
            twin_name="none"
        )
        res = broken_engine.attempt_activation("activate second brain", source=ContextSource.USER_INTERACTIVE)
        self.assertFalse(res["success"])
        self.assertEqual(broken_engine.state, AuthorizationState.DENIED)

    def test_valid_user_interactive_activation(self):
        """Verify direct, unquoted user interactive phrase succeeds."""
        res = self.engine.attempt_activation("activate second brain", source=ContextSource.USER_INTERACTIVE)
        self.assertTrue(res["success"])
        self.assertEqual(self.engine.state, AuthorizationState.AUTONOMOUS)

    def test_git_restrictions_persist_in_autonomous_mode(self):
        """Verify Git commit/push remain unauthorized even in autonomous mode without explicit grant."""
        # Activate autonomous mode
        self.engine.attempt_activation("activate second brain", source=ContextSource.USER_INTERACTIVE)
        self.assertEqual(self.engine.state, AuthorizationState.AUTONOMOUS)

        for git_op in RESTRICTED_GIT_OPERATIONS:
            req = {"action": git_op, "resource": "repository", "source": ContextSource.USER_INTERACTIVE}
            decision = self.engine.evaluate_decision_procedure(req)
            self.assertFalse(decision["allowed"], f"CRITICAL: Git op '{git_op}' was allowed in autonomous mode without grant!")
            self.assertIn("requires explicit authorization grant", decision["reason"])

    def test_action_scoped_grant_consumption(self):
        """Verify explicit grant is single-use and cannot be reused for another action."""
        grant_id = self.engine.grant_action_authorization("commit", "src/file.py", "owner", ttl_seconds=300)

        # First use -> Allowed
        req1 = {"action": "commit", "resource": "src/file.py", "grant_id": grant_id}
        dec1 = self.engine.evaluate_decision_procedure(req1)
        self.assertTrue(dec1["allowed"])

        # Second use -> Rejected (single use consumed)
        req2 = {"action": "commit", "resource": "src/file.py", "grant_id": grant_id}
        dec2 = self.engine.evaluate_decision_procedure(req2)
        self.assertFalse(dec2["allowed"])
        self.assertIn("already been consumed", dec2["reason"])

    def test_grant_scope_broadening_rejected(self):
        """Verify grant for 'commit' does not permit 'push'."""
        grant_id = self.engine.grant_action_authorization("commit", "src/file.py", "owner", ttl_seconds=300)

        req = {"action": "push", "resource": "origin/master", "grant_id": grant_id}
        dec = self.engine.evaluate_decision_procedure(req)
        self.assertFalse(dec["allowed"])
        self.assertIn("does not cover requested action", dec["reason"])

    def test_expired_grant_rejected(self):
        """Verify grant past TTL is rejected."""
        grant_id = self.engine.grant_action_authorization("commit", "src/file.py", "owner", ttl_seconds=0.01)
        time.sleep(0.05)

        req = {"action": "commit", "resource": "src/file.py", "grant_id": grant_id, "timestamp": time.time()}
        dec = self.engine.evaluate_decision_procedure(req)
        self.assertFalse(dec["allowed"])
        self.assertIn("expired", dec["reason"])

    def test_git_restrictions_survive_session_reset(self):
        """Verify new session resets to supervised mode."""
        self.engine.attempt_activation("activate second brain", source=ContextSource.USER_INTERACTIVE)
        self.assertEqual(self.engine.state, AuthorizationState.AUTONOMOUS)

        # Simulate fresh session wake-up
        fresh_engine = PolicyEngine(repo_dir=self.test_dir, activation_phrase="activate second brain", twin_name="Deuter")
        self.assertEqual(fresh_engine.state, AuthorizationState.SUPERVISED)

if __name__ == "__main__":
    unittest.main()
