# Digi-Brain Persona Exporter & Preference Learning Engine (POSIX & Cross-Platform)
# Implements REQ-5.1, REQ-5.2, REQ-5.3, REQ-5.4

import argparse
import json
import os
import re
import sys
from typing import Dict, Any, List, Tuple

SECRET_PATTERNS = [
    r"ghp_[A-Za-z0-9_]{36,}",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"AKIA[0-9A-Z]{16}",
    r"bearer\s+[A-Za-z0-9_\-\.]+",
    r"password\b|passwd\b",
    r"postgres://",
    r"mongodb://",
    r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
    r"api[_-]?key\b"
]

def scan_secrets(text: str) -> Tuple[bool, str]:
    for pat in SECRET_PATTERNS:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return True, f"Pattern matched: {pat}"
    return False, ""

def parse_divergence_table(input_path: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    rows = []
    in_twin = False
    for line in lines:
        if re.search(r"twin|divergence", line, re.IGNORECASE):
            in_twin = True
        if in_twin and line.strip().startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                date_cell = parts[1]
                pick_cell = parts[2]
                corr_cell = parts[3]
                lesson_cell = parts[4] if len(parts) > 4 else ''
                if date_cell in ("Date", "---", "") or "---" in date_cell:
                    continue
                if "---" in pick_cell or pick_cell.lower() == "pick":
                    continue
                rows.append({
                    "date": date_cell,
                    "pick": pick_cell,
                    "correction": corr_cell,
                    "lesson": lesson_cell
                })
    return rows

def export_persona(input_path: str, out_path: str, schema_ver: str = "v1", quarantine_path: str = None) -> Dict[str, Any]:
    rows = parse_divergence_table(input_path)
    if not quarantine_path:
        quarantine_path = os.path.splitext(out_path)[0] + ".quarantine.jsonl"
    valid_records = []
    quarantine_records = []
    skipped = 0
    idx = 0
    for r in rows:
        idx += 1
        pick = r["pick"].strip()
        corr = r["correction"].strip()
        lesson = r["lesson"].strip()
        date_val = r["date"].strip()
        if not pick or not corr:
            skipped += 1
            continue
        if ("{" in pick and "}" in pick) or ("{" in corr and "}" in corr):
            skipped += 1
            continue
        blob = f"{date_val} {pick} {corr} {lesson}"
        has_secret, secret_reason = scan_secrets(blob)
        if has_secret:
            quarantine_records.append({
                "row_index": idx,
                "date": date_val,
                "reason": secret_reason,
                "raw_text": blob[:100]
            })
            continue
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_val):
            date_val = "unknown"
        date_clean = date_val.replace("-", "")
        pair_id = f"div-{date_clean}-{idx:02d}"
        if schema_ver == "v2":
            record = {
                "pair_id": pair_id,
                "schema": "digi-brain-divergence-pair-v2",
                "date": date_val,
                "twin_pick": pick,
                "owner_correction": corr,
                "scope": "project",
                "decision_category": "workflow",
                "review_status": "verified"
            }
        else:
            record = {
                "pair_id": pair_id,
                "schema": "digi-brain-divergence-pair-v1",
                "date": date_val,
                "twin_pick": pick,
                "owner_correction": corr
            }
        if lesson:
            record["lesson"] = lesson
        valid_records.append(record)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        for rec in valid_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if quarantine_records:
        with open(quarantine_path, "w", encoding="utf-8", newline="\n") as f:
            for q in quarantine_records:
                f.write(json.dumps(q, ensure_ascii=False) + "\n")
    return {
        "total_rows": len(rows),
        "written": len(valid_records),
        "skipped": skipped,
        "quarantined": len(quarantine_records),
        "out_path": out_path,
        "quarantine_path": quarantine_path
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Digi-Brain Persona Exporter")
    parser.add_argument("--input", required=True, help="Path to personalities.md")
    parser.add_argument("--out", default="", help="Output pairs.jsonl path")
    parser.add_argument("--schema", default="v1", choices=["v1", "v2"], help="Schema version")
    args = parser.parse_args()
    out_p = args.out
    if not out_p:
        out_p = os.path.join(os.path.dirname(args.input), "persona-pairs.jsonl")
    stats = export_persona(args.input, out_p, schema_ver=args.schema)
    print(f"EXPORT OK: {stats['out_path']} (written={stats['written']} skipped={stats['skipped']} quarantined={stats['quarantined']})")
