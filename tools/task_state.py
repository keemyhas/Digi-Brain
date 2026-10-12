# Digi-Brain Explicit Task State Continuity Manager
# Implements REQ-4.2

import json
import os
import time
from typing import Dict, Any, List, Optional, Tuple

class TaskStateManager:
    def __init__(self, agents_dir: str):
        self.agents_dir = agents_dir
        self.state_file = os.path.join(agents_dir, "memory", "task-state.json")

    def initialize_task(self, task_id: str, description: str) -> Dict[str, Any]:
        state = {
            "task_id": task_id,
            "description": description,
            "status": "in_progress",
            "created_at": time.time(),
            "updated_at": time.time(),
            "completed_steps": [],
            "remaining_steps": [],
            "decisions_made": [],
            "files_changed": [],
            "tests_executed": [],
            "tests_failed": [],
            "unverified_items": [],
            "protected_invariants": [],
            "pending_authorizations": []
        }
        self.save_state(state)
        return state

    def save_state(self, state: Dict[str, Any]):
        state["updated_at"] = time.time()
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        # Safe atomic write
        tmp = self.state_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
        if os.path.exists(self.state_file):
            os.remove(self.state_file)
        os.rename(tmp, self.state_file)

    def load_state(self) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        if not os.path.isfile(self.state_file):
            return False, None, "No active task state found (file does not exist)"
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return True, data, "OK"
        except Exception as e:
            return False, None, f"Task state corrupted or unreadable: {str(e)}"

    def record_step_completion(self, step_name: str, verification_evidence: str):
        ok, state, msg = self.load_state()
        if not ok or not state:
            raise RuntimeError(msg)
        state["completed_steps"].append({
            "step": step_name,
            "evidence": verification_evidence,
            "timestamp": time.time()
        })
        if step_name in state.get("remaining_steps", []):
            state["remaining_steps"].remove(step_name)
        self.save_state(state)

    def record_file_change(self, file_path: str):
        ok, state, msg = self.load_state()
        if ok and state:
            if file_path not in state["files_changed"]:
                state["files_changed"].append(file_path)
            self.save_state(state)

    def record_test_result(self, test_name: str, passed: bool, output: str = ""):
        ok, state, msg = self.load_state()
        if ok and state:
            record = {"test": test_name, "passed": passed, "output": output[:200], "timestamp": time.time()}
            state["tests_executed"].append(record)
            if not passed:
                state["tests_failed"].append(record)
            self.save_state(state)
