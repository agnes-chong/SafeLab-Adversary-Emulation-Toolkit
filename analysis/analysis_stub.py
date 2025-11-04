#!/usr/bin/env python3
"""
analysis/analysis_stub.py

Simple analysis helper to compute detection metrics from demo/report.json (normalized output).
This file is intentionally minimal so it can be run as a script or opened in Jupyter.

Usage:
    python analysis/analysis_stub.py demo/report.json
"""

import json
import sys
from pprint import pprint
from collections import Counter

def load(path="demo/report.json"):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)

def summary(data):
    alerts = data.get("alerts", [])
    total = len(alerts)
    detected = sum(1 for a in alerts if a.get("detected"))
    missed = total - detected
    technique_counts = Counter(a.get("technique_id") for a in alerts)
    print("===== SafeLab Analysis Summary =====")
    print(f"Scenario: {data.get('scenario')}")
    print(f"Host: {data.get('host')} ({data.get('platform')})")
    print(f"Started: {data.get('started_at')}  Finished: {data.get('finished_at')}")
    print()
    print(f"Total steps: {total}")
    print(f"Detected: {detected}")
    print(f"Missed: {missed}")
    print()
    print("Technique counts:")
    for t, c in technique_counts.items():
        print(f"  {t}: {c}")
    print()
    print("Detailed alerts:")
    for a in alerts:
        print(f"- {a.get('timestamp')} | {a.get('technique_id')} | {a.get('technique_name')} | detected={a.get('detected')}")
        print(f"    evidence: {a.get('evidence')}")
    print("====================================")

if __name__ == "__main__":
    path = "demo/report.json" if len(sys.argv) < 2 else sys.argv[1]
    data = load(path)
    summary(data)
