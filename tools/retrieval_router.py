# Digi-Brain Staged Retrieval Router
# Implements REQ-4.1, REQ-4.3, REQ-7.1

import os
import re
from typing import Dict, Any, List, Set

class StagedRetrievalRouter:
    def __init__(self, agents_dir: str):
        self.agents_dir = agents_dir
        self.memory_dir = os.path.join(agents_dir, "memory")
        self.rules_dir = os.path.join(agents_dir, "rules")

    def stage1_boot_context(self) -> Dict[str, Any]:
        context = {
            "stage": 1,
            "identity": {},
            "safety_invariants": [],
            "working_conditions": {}
        }
        brain_path = os.path.join(self.memory_dir, "brain.md")
        if os.path.isfile(brain_path):
            with open(brain_path, "r", encoding="utf-8") as f:
                text = f.read()
                context["has_brain"] = True
                twin_match = re.search(r"twin identity\s*:\s*([^\r\n]+)", text, re.IGNORECASE)
                if twin_match:
                    context["identity"]["twin_name"] = twin_match.group(1).strip()

        std_path = os.path.join(self.rules_dir, "engineering-standards.md")
        if os.path.isfile(std_path):
            with open(std_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip().startswith("- ") or line.strip().startswith("1. ")]
                context["safety_invariants"] = lines[:5]
        return context

    def stage2_task_context(self, task_query: str, keywords: List[str] = None) -> Dict[str, Any]:
        keywords = [k.lower() for k in (keywords or task_query.split()) if len(k) > 2]
        retrieved_decisions = []
        retrieved_lessons = []
        dec_path = os.path.join(self.memory_dir, "decisions.md")
        if os.path.isfile(dec_path):
            with open(dec_path, "r", encoding="utf-8") as f:
                blocks = f.read().split("### ")
                for b in blocks:
                    b_lower = b.lower()
                    if any(k in b_lower for k in keywords):
                        retrieved_decisions.append(b.strip())
        les_path = os.path.join(self.memory_dir, "agent-lessons.md")
        if os.path.isfile(les_path):
            with open(les_path, "r", encoding="utf-8") as f:
                blocks = f.read().split("### ")
                for b in blocks:
                    b_lower = b.lower()
                    if any(k in b_lower for k in keywords):
                        retrieved_lessons.append(b.strip())
        return {
            "stage": 2,
            "relevant_decisions": retrieved_decisions,
            "relevant_lessons": retrieved_lessons,
            "item_count": len(retrieved_decisions) + len(retrieved_lessons)
        }

    def stage3_verification_context(self, domain: str = "general") -> Dict[str, Any]:
        commands = []
        checklist_path = os.path.join(self.agents_dir, "BOOT-CHECKLIST.md")
        if os.path.isfile(checklist_path):
            with open(checklist_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "test command" in line.lower() or "verify" in line.lower():
                        commands.append(line.strip())
        return {
            "stage": 3,
            "verification_commands": commands,
            "domain": domain
        }

    def stage4_consolidation(self, items_to_save: List[Dict[str, Any]]) -> Dict[str, Any]:
        accepted = []
        rejected = []
        for item in items_to_save:
            if item.get("title") and item.get("content") and len(item.get("content", "")) >= 10:
                accepted.append(item)
            else:
                rejected.append({"item": item, "reason": "Insufficient detail or missing fields"})
        return {
            "stage": 4,
            "accepted_for_storage": accepted,
            "rejected_items": rejected
        }
