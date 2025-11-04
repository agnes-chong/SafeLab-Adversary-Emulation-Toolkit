#!/usr/bin/env python3
"""
collector/collect.py

Reads emulation output JSON and normalizes events into a simplified structure for reporting.
This script intentionally performs only benign normalization and simple detection heuristics.

Usage:
    python collector/collect.py --input demo/output.json --out demo/report.json
"""

import argparse
import json
import os

def simple_detect(evidence_text: str) -> bool:
    """Very simple detection heuristic for demo purposes."""
    if not evidence_text:
        return False
    t = evidence_text.lower()
    if any(k in t for k in ("launched", "spawned", "wrote file", "wrote", "post to", "attempted post")):
        return True
    return False

def normalize(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    normalized = {
        "scenario": data.get("scenario"),
        "started_at": data.get("started_at"),
        "finished_at": data.get("finished_at"),
        "host": data.get("metadata", {}).get("host"),
        "platform": data.get("metadata", {}).get("platform"),
        "alerts": []
    }

    for e in data.get("events", []):
        evidence = e.get("evidence") or ""
        alert = {
            "technique_id": e.get("technique_id"),
            "technique_name": e.get("technique_name"),
            "action": e.get("action"),
            "timestamp": e.get("timestamp"),
            "status": e.get("status"),
            "evidence": evidence,
            "detected": simple_detect(evidence)
        }
        normalized["alerts"].append(alert)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(normalized, fh, indent=2)

    print(f"[collector] Normalized {len(normalized['alerts'])} events -> {output_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Normalize emulation output")
    ap.add_argument("--input", "-i", default="demo/output.json", help="Emulation output JSON")
    ap.add_argument("--out", "-o", default="demo/report.json", help="Normalized report JSON")
    args = ap.parse_args()
    normalize(args.input, args.out)
