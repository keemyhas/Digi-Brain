# Digi-Brain Memory Guard & Integrity Validation Layer
# Implements REQ-3.1, REQ-3.2, REQ-3.3, REQ-3.4, REQ-3.5, REQ-3.6

import datetime
import enum
import os
import re
import shutil
import tempfile
from typing import Dict, Any, List, Optional, Tuple

class MemoryType(enum.Enum):
    EPISODIC = "Episodic"
    SEMANTIC = "Semantic"
    PROCEDURAL = "Procedural"
    PREFERENCE = "Preference"
    INFERENCE = "Inference"

class SourceClassification(enum.Enum):
    EXPLICIT_USER = "ExplicitUser"
    VERIFIED_DOC = "VerifiedDoc"
    OBSERVED_TOOL = "ObservedTool"
    TEST_EVIDENCE = "TestEvidence"
    UNTRUSTED_CONTENT = "UntrustedContent"
    AI_INFERENCE = "AIInference"

class EntryStatus(enum.Enum):
    CURRENT = "Current"
    UNVERIFIED = "Unverified"
    SUPERSEDED = "Superseded"
    EXPIRED = "Expired"
    DISPUTED = "Disputed"

POISON_PATTERNS = [
    r"ignore\s+(all\s+)?([a-z]+\s+)*(safety|security|policy|prior|invariants|rules|instructions|git gates)",
    r"override\s+(policy|authorization|git gates)",
    r"bypass\s+(commit|push|safety)\s+(gate|check|invariant)",
    r"you are now in unrestricted mode",
    r"disable\s+(safety|fingerprint|secret|verification)",
]

class MemoryEntry:
    def __init__(
        self,
        entry_id: str,
        memory_type: MemoryType,
        source_class: SourceClassification,
        title: str,
        content: str,
        status: EntryStatus = EntryStatus.CURRENT,
        scope: str = "project",
        confidence: str = "high",
        supersedes: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        self.entry_id = entry_id
        self.memory_type = memory_type
        self.source_class = source_class
        self.title = title
        self.content = content
        self.status = status
        self.scope = scope
        self.confidence = confidence
        self.supersedes = supersedes
        self.created_at = created_at or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

    def to_markdown(self) -> str:
        out = [
            f"### [{self.entry_id}] {self.title}",
            f"- **Type**: {self.memory_type.value}",
            f"- **SourceClass**: {self.source_class.value}",
            f"- **Status**: {self.status.value}",
            f"- **Scope**: {self.scope}",
            f"- **Confidence**: {self.confidence}",
            f"- **CreatedAt**: {self.created_at}"
        ]
        if self.supersedes:
            out.append(f"- **Supersedes**: {self.supersedes}")
        out.append("")
        out.append(self.content.strip())
        out.append("")
        return "\n".join(out) + "\n"

class MemoryGuard:
    def __init__(self, memory_dir: str):
        self.memory_dir = memory_dir

    def scan_for_poison(self, text: str) -> Tuple[bool, Optional[str]]:
        for pat in POISON_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                return True, f"Memory poisoning detected: pattern '{pat}'"
        return False, None

    def validate_entry(self, entry: MemoryEntry) -> Tuple[bool, List[str]]:
        errors = []
        if not entry.entry_id or not re.match(r"^[A-Z0-9_\-]+$", entry.entry_id):
            errors.append(f"Invalid entry_id format: '{entry.entry_id}'")
        if not entry.title or len(entry.title.strip()) < 3:
            errors.append("Title too short or missing")
        if not entry.content or len(entry.content.strip()) < 5:
            errors.append("Content too short or missing")
        is_poison, poison_reason = self.scan_for_poison(entry.title + ' ' + entry.content)
        if is_poison:
            errors.append(poison_reason)
        if entry.source_class == SourceClassification.UNTRUSTED_CONTENT:
            if entry.status == EntryStatus.CURRENT:
                errors.append("Untrusted content cannot be registered with status 'Current'; must be 'Unverified' or 'Disputed'")
            if entry.confidence.lower() in ("high", "verified"):
                errors.append("Untrusted content cannot hold 'high' or 'verified' confidence")
        if entry.memory_type == MemoryType.INFERENCE and entry.scope == "universal":
            errors.append("Inference memory cannot claim universal scope without explicit user confirmation")
        return len(errors) == 0, errors

    def check_append_only_integrity(self, file_path: str, proposed_content: str) -> Tuple[bool, List[str]]:
        if not os.path.isfile(file_path):
            return True, []
        with open(file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
        errors = []
        existing_ids = re.findall(r"###\s*\[([A-Z0-9_\-]+)\]", existing_content)
        for eid in existing_ids:
            if f"[{eid}]" not in proposed_content:
                errors.append(f"Historical entry '{eid}' was removed! Historical memory is append-oriented.")
        return len(errors) == 0, errors

    def detect_contradictions(self, file_name: str, entry: MemoryEntry) -> List[Dict[str, Any]]:
        """
        Detects potential contradictions between incoming entry and existing active entries.
        Flags cases where an entry touches the exact same scope/topic without superseding.
        """
        target_file = os.path.join(self.memory_dir, file_name)
        if not os.path.isfile(target_file):
            return []
        with open(target_file, "r", encoding="utf-8") as f:
            text = f.read()

        conflicts = []
        blocks = re.findall(r"###\s*\[([A-Z0-9_\-]+)\]\s*([^\n]+)", text)
        entry_words = set(re.findall(r"\w{4,}", (entry.title + " " + entry.content).lower()))

        for eid, title in blocks:
            if eid == entry.entry_id:
                continue
            if entry.supersedes == eid:
                continue
            block_match = re.search(rf"###\s*\[{re.escape(eid)}\][\s\S]*?(?=(?:###\s*\[|\Z))", text)
            if block_match:
                block_text = block_match.group(0)
                if "- **Status**: Superseded" in block_text or "- **Status**: Expired" in block_text:
                    continue
                exist_words = set(re.findall(r"\w{4,}", (title + " " + block_text).lower()))
                overlap = entry_words.intersection(exist_words)
                critical_topics = {"database", "postgres", "postgresql", "sqlite", "mysql", "tailwind", "css", "auth", "orm", "monolith", "microservices"}
                critical_overlap = overlap.intersection(critical_topics)
                if critical_overlap and "- **Status**: Disputed" not in block_text:
                    conflicts.append({
                        "entry_id": eid,
                        "title": title.strip(),
                        "overlapping_topics": sorted(list(critical_overlap)),
                        "reason": f"Direct topic conflict on {sorted(list(critical_overlap))} without explicit supersession link"
                    })
        return conflicts

    def append_decision(self, file_name: str, entry: MemoryEntry, enforce_contradiction_check: bool = False) -> Tuple[bool, str]:
        valid, errors = self.validate_entry(entry)
        if not valid:
            return False, f"Validation failed: {'; '.join(errors)}"
        if enforce_contradiction_check and entry.status != EntryStatus.DISPUTED and not entry.supersedes:
            conflicts = self.detect_contradictions(file_name, entry)
            if conflicts:
                first_c = conflicts[0]
                return False, f"Contradiction detected: conflicts with active entry [{first_c['entry_id']}] on {first_c['overlapping_topics']}. Must declare supersession or mark as Disputed."
        target_file = os.path.join(self.memory_dir, file_name)
        existing_text = ""
        if os.path.isfile(target_file):
            with open(target_file, "r", encoding="utf-8") as f:
                existing_text = f.read()
        updated_text = existing_text
        if entry.supersedes:
            target_pat = rf"###\s*\[{re.escape(entry.supersedes)}\][^\n]*\n(?:- \*\*[^\n]+\n)*"
            match = re.search(target_pat, updated_text)
            if match:
                block = match.group(0)
                if "- **Status**:" in block:
                    new_block = re.sub(
                        r"- \*\*Status\*\*:[^\n]+",
                        f"- **Status**: Superseded by {entry.entry_id}",
                        block
                    )
                    updated_text = updated_text.replace(block, new_block, 1)
        if not updated_text.endswith("\n\n") and updated_text:
            updated_text += "\n"
        updated_text += entry.to_markdown()
        ok, int_errs = self.check_append_only_integrity(target_file, updated_text)
        if not ok:
            return False, f"Integrity check failed: {'; '.join(int_errs)}"
        temp_dir = tempfile.mkdtemp(prefix="mem_stage_")
        try:
            temp_file = os.path.join(temp_dir, file_name)
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(updated_text)
            shutil.move(temp_file, target_file)
            return True, f"Successfully recorded entry {entry.entry_id}"
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
