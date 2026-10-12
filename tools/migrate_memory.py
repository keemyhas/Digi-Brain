# Digi-Brain Memory Schema Migration Utility
# Implements REQ-9.1, REQ-12.1

import argparse
import os
import re
import shutil
import sys
import time
from typing import Dict, Any, List, Tuple

def detect_legacy_format(agents_dir: str) -> Dict[str, Any]:
    memory_dir = os.path.join(agents_dir, "memory")
    legacy_findings = []
    dec_path = os.path.join(memory_dir, "decisions.md")
    if os.path.isfile(dec_path):
        with open(dec_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "## ADR-" in content and "- **Type**:" not in content:
                legacy_findings.append("decisions_lacks_provenance_header")
    les_path = os.path.join(memory_dir, "agent-lessons.md")
    if os.path.isfile(les_path):
        with open(les_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "### Lesson 00" in content and "- **Type**:" not in content:
                legacy_findings.append("lessons_lacks_provenance_header")
    return {
        'is_legacy': len(legacy_findings) > 0,
        'findings': legacy_findings
    }

def migrate_decisions_file(dec_path: str) -> Tuple[bool, int]:
    if not os.path.isfile(dec_path):
        return False, 0
    with open(dec_path, "r", encoding="utf-8") as f:
        content = f.read()
    migrated_count = 0
    def repl_adr(m):
        nonlocal migrated_count
        migrated_count += 1
        adr_num = m.group(1)
        title = m.group(2).strip()
        return f"### [ADR-{adr_num}] {title}\n- **Type**: Semantic\n- **SourceClass**: ExplicitUser\n- **Status**: Current\n- **Scope**: project\n- **Confidence**: verified\n- **CreatedAt**: legacy\n- **Supersedes**: none"
    new_content = re.sub(r"##\s*ADR-(\d+):\s*([^\n]+)", repl_adr, content)
    with open(dec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    return True, migrated_count

def migrate_lessons_file(les_path: str) -> Tuple[bool, int]:
    if not os.path.isfile(les_path):
        return False, 0
    with open(les_path, "r", encoding="utf-8") as f:
        content = f.read()
    migrated_count = 0
    def repl_les(m):
        nonlocal migrated_count
        migrated_count += 1
        les_num = m.group(1)
        title = m.group(2).strip()
        return f"### [LES-{les_num}] {title}\n- **Type**: Procedural\n- **SourceClass**: ExplicitUser\n- **Status**: Current\n- **Scope**: universal\n- **Confidence**: verified\n- **CreatedAt**: legacy"
    new_content = re.sub(r"###\s*Lesson\s*(\d+):\s*([^\n]+)", repl_les, content)
    with open(les_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)
    return True, migrated_count

def migrate_agents_directory(agents_dir: str) -> Dict[str, Any]:
    if not os.path.isdir(agents_dir):
        raise FileNotFoundError(f"Directory not found: {agents_dir}")
    check = detect_legacy_format(agents_dir)
    if not check['is_legacy']:
        return {'status': 'up_to_date', 'migrated_entries': 0}
    # 1. Create safety backup first
    ts = time.strftime("%Y%m%d-%H%M%S")
    backup_dir = f"{agents_dir}.backup-pre-migration-{ts}"
    shutil.copytree(agents_dir, backup_dir)
    # 2. Migrate files
    memory_dir = os.path.join(agents_dir, "memory")
    dec_path = os.path.join(memory_dir, "decisions.md")
    les_path = os.path.join(memory_dir, "agent-lessons.md")
    d_ok, d_count = migrate_decisions_file(dec_path)
    l_ok, l_count = migrate_lessons_file(les_path)
    return {
        'status': 'migrated',
        'backup_path': backup_dir,
        'migrated_entries': d_count + l_count,
        'decisions_migrated': d_count,
        'lessons_migrated': l_count
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digi-Brain Memory Migration Utility")
    parser.add_argument("--target", required=True, help="Path to .agents directory")
    args = parser.parse_args()
    res = migrate_agents_directory(args.target)
    print(f"MIGRATION RESULT: {res['status']} (migrated={res['migrated_entries']})")
