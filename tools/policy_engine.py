# Digi-Brain Policy & Authorization Engine
# Implements Layer B (Policy) and coordinates Layer C (Enforcement)
# Mandate Phase Two: REQ-2.1, REQ-2.2, REQ-2.3, REQ-2.4, REQ-2.5

import enum
import json
import os
import re
import time
from typing import Dict, Any, Optional, Tuple, List

class AuthorizationState(enum.Enum):
    SUPERVISED = "SUPERVISED"
    AUTONOMOUS = "AUTONOMOUS"
    PENDING = "PENDING"
    DENIED = "DENIED"
    EXPIRED = "EXPIRED"
    RESTRICTED = "RESTRICTED"

class ContextSource(enum.Enum):
    USER_INTERACTIVE = "USER_INTERACTIVE"
    UNTRUSTED_DOCUMENT = "UNTRUSTED_DOCUMENT"
    TRANSCRIPT_OR_LOG = "TRANSCRIPT_OR_LOG"
    IMPORTED_MEMORY = "IMPORTED_MEMORY"
    SYSTEM_CONFIG = "SYSTEM_CONFIG"

# Sensitive operations requiring explicit per-operation authorization
RESTRICTED_GIT_OPERATIONS = {
    "commit", "push", "rebase", "reset", "branch_delete", "force_push", "tag_delete"
}

DESTRUCTIVE_OPERATIONS = {
    "delete_database", "drop_table", "truncate_table", "rm_rf_root", "destroy_repo"
}

class PolicyEngine:
    def __init__(self, repo_dir: str, activation_phrase: str = "take the wheel", twin_name: str = "Deuter"):
        self.repo_dir = repo_dir
        self.activation_phrase = activation_phrase.strip().lower()
        self.twin_name = twin_name.strip()
        self.state = AuthorizationState.SUPERVISED
        self.active_grants: Dict[str, Dict[str, Any]] = {}
        self.state_history: List[Dict[str, Any]] = []
        self._record_transition(AuthorizationState.SUPERVISED, "initial_session_boot", "system")

    def _record_transition(self, new_state: AuthorizationState, reason: str, actor: str):
        self.state = new_state
        self.state_history.append({
            "timestamp": time.time(),
            "state": new_state.value,
            "reason": reason,
            "actor": actor
        })

    def check_autonomous_readiness(self) -> Tuple[bool, List[str]]:
        """Validates readiness criteria before autonomous mode can activate."""
        blockers = []
        if not self.twin_name or self.twin_name.lower() in ("none", "disabled"):
            blockers.append("Twin name not configured or autonomous mode disabled")

        # Check that core memory files exist
        agents_dir = os.path.join(self.repo_dir, ".agents")
        if not os.path.isdir(agents_dir):
            blockers.append(".agents directory missing")
        else:
            brain_file = os.path.join(agents_dir, "memory", "brain.md")
            if not os.path.isfile(brain_file):
                blockers.append(".agents/memory/brain.md missing")
            standards_file = os.path.join(agents_dir, "rules", "engineering-standards.md")
            if not os.path.isfile(standards_file):
                blockers.append(".agents/rules/engineering-standards.md missing")

        return (len(blockers) == 0, blockers)

    def attempt_activation(self, input_text: str, source: ContextSource, is_quoted: bool = False) -> Dict[str, Any]:
        """
        Evaluates activation phrase input.
        Rejects phrases originating from untrusted documents, logs, or quotes.
        """
        norm_text = input_text.strip().lower()

        # Reject if originating from untrusted source
        if source != ContextSource.USER_INTERACTIVE:
            return {
                "success": False,
                "reason": f"Activation rejected: source {source.value} is untrusted",
                "state": self.state.value
            }

        # Reject if quoted as an example or embedded in a document snippet
        if is_quoted or f'"{self.activation_phrase}"' in norm_text or f"'{self.activation_phrase}'" in norm_text:
            return {
                "success": False,
                "reason": "Activation rejected: quoted phrase or example reference detected",
                "state": self.state.value
            }

        if self.activation_phrase not in norm_text:
            return {
                "success": False,
                "reason": "Activation phrase not matched",
                "state": self.state.value
            }

        ready, blockers = self.check_autonomous_readiness()
        if not ready:
            self._record_transition(AuthorizationState.DENIED, f"Readiness check failed: {', '.join(blockers)}", "policy")
            return {
                "success": False,
                "reason": f"Readiness requirements not met: {', '.join(blockers)}",
                "state": self.state.value
            }

        self._record_transition(AuthorizationState.AUTONOMOUS, "User spoken activation phrase validated", "user")
        return {
            "success": True,
            "reason": f"Autonomous mode activated for twin {self.twin_name}",
            "state": self.state.value
        }

    def deactivate(self, reason: str = "User session requested stop"):
        self._record_transition(AuthorizationState.SUPERVISED, reason, "user")

    def grant_action_authorization(self, action: str, resource: str, granted_by: str, ttl_seconds: float = 300.0) -> str:
        """Grants explicit single-action authorization with expiration."""
        grant_id = f"grant-{int(time.time()*1000)}"
        self.active_grants[grant_id] = {
            "action": action,
            "resource": resource,
            "granted_by": granted_by,
            "created_at": time.time(),
            "expires_at": time.time() + ttl_seconds,
            "used": False
        }
        return grant_id

    def evaluate_decision_procedure(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the formal 8-step decision procedure:
        1. What action is being requested?
        2. What resource will it affect?
        3. Is the action permitted by policy?
        4. Is explicit authorization required?
        5. Is the authorization current and applicable to this exact action?
        6. Is the requested scope covered?
        7. Can the host enforce the restriction?
        8. What evidence will establish the outcome?
        """
        action = request.get("action", "").strip()
        resource = request.get("resource", "").strip()
        source = request.get("source", ContextSource.USER_INTERACTIVE)
        grant_id = request.get("grant_id")
        current_time = request.get("timestamp", time.time())
        host_enforced = request.get("host_enforced", False)

        # 1 & 2: Action and resource
        if not action or not resource:
            return {
                "allowed": False,
                "step_failed": 1,
                "reason": "Action or resource unspecified",
                "state": self.state.value
            }

        # 3: General policy permission
        if action in DESTRUCTIVE_OPERATIONS:
            return {
                "allowed": False,
                "step_failed": 3,
                "reason": f"Action '{action}' is strictly prohibited by non-negotiable safety invariant",
                "state": AuthorizationState.RESTRICTED.value
            }

        # 4: Is explicit authorization required?
        requires_explicit = (action in RESTRICTED_GIT_OPERATIONS) or (self.state != AuthorizationState.AUTONOMOUS)

        if not requires_explicit:
            # Autonomous mode permits standard read, test, edit within project scope
            return {
                "allowed": True,
                "reason": f"Permitted under autonomous twin mode ({self.twin_name})",
                "state": self.state.value,
                "enforcement": "host_enforced" if host_enforced else "behavioral_contract"
            }

        # 5 & 6: Check grant freshness, applicability, and scope
        if not grant_id or grant_id not in self.active_grants:
            return {
                "allowed": False,
                "step_failed": 5,
                "reason": f"Action '{action}' requires explicit authorization grant",
                "state": self.state.value
            }

        grant = self.active_grants[grant_id]
        if grant["used"]:
            return {
                "allowed": False,
                "step_failed": 5,
                "reason": f"Authorization grant '{grant_id}' has already been consumed",
                "state": AuthorizationState.EXPIRED.value
            }

        if current_time > grant["expires_at"]:
            return {
                "allowed": False,
                "step_failed": 5,
                "reason": f"Authorization grant '{grant_id}' expired at {grant['expires_at']}",
                "state": AuthorizationState.EXPIRED.value
            }

        if grant["action"] != action:
            return {
                "allowed": False,
                "step_failed": 6,
                "reason": f"Grant action '{grant['action']}' does not cover requested action '{action}'",
                "state": self.state.value
            }

        if grant["resource"] != resource and grant["resource"] != "*":
            return {
                "allowed": False,
                "step_failed": 6,
                "reason": f"Grant resource '{grant['resource']}' does not cover requested resource '{resource}'",
                "state": self.state.value
            }

        # Consume single-use grant
        grant["used"] = True

        return {
            "allowed": True,
            "reason": f"Action '{action}' authorized by grant '{grant_id}'",
            "state": self.state.value,
            "step_passed": 8,
            "enforcement": "host_enforced" if host_enforced else "behavioral_contract"
        }
