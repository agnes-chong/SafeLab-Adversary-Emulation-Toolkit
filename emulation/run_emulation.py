#!/usr/bin/env python3
"""
emulation/run_emulation.py

Safe emulation runner. Executes benign actions mapped to ATT&CK-style technique IDs.
Outputs structured JSON events describing each step.

Usage:
    python emulation/run_emulation.py --scenario quick-test --out demo/output.json
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from datetime import datetime

SCENARIOS = {
    "quick-test": [
        {"id": "T1059", "name": "Execution: spawn_process", "action": "spawn_process"},
        {"id": "T1033", "name": "Create benign file", "action": "create_file"},
        {"id": "T1041", "name": "Simulate exfil (local POST)", "action": "local_http_post"}
    ]
}

def ts():
    return datetime.utcnow().isoformat() + "Z"

def spawn_process(event):
    system = platform.system()
    if system == "Windows":
        try:
            p = subprocess.Popen(["notepad.exe"])
            time.sleep(0.8)
            p.terminate()
            event["evidence"] = "Launched notepad.exe (terminated)"
        except FileNotFoundError:
            event["evidence"] = "notepad.exe not found; skipped"
    else:
        # Unix: spawn sleep process
        try:
            p = subprocess.Popen(["sleep", "0.1"])
            p.wait()
            event["evidence"] = "spawned sleep 0.1"
        except Exception as e:
            event["evidence"] = f"spawn sleep failed: {e}"
    return event

def create_file(event):
    fpath = os.path.join(tempfile.gettempdir(), f"safelab_test_{int(time.time())}.txt")
    try:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("safelab benign test file\n")
        event["evidence"] = f"wrote file {fpath}"
    except Exception as e:
        event["evidence"] = f"file write failed: {e}"
    return event

def local_http_post(event):
    try:
        import requests
        url = "http://127.0.0.1:8000/echo"
        resp = requests.post(url, json={"test": "safelab"}, timeout=1)
        event["evidence"] = f"POST to {url} status={resp.status_code}"
    except Exception as e:
        event["evidence"] = f"Attempted POST to localhost (no server) - exception: {e}"
    return event

ACTION_MAP = {
    "spawn_process": spawn_process,
    "create_file": create_file,
    "local_http_post": local_http_post
}

def run_scenario(name, out_path):
    if name not in SCENARIOS:
        raise ValueError(f"unknown scenario '{name}'")
    events = []
    start = ts()
    for step in SCENARIOS[name]:
        event = {
            "scenario": name,
            "technique_id": step["id"],
            "technique_name": step["name"],
            "action": step["action"],
            "timestamp": ts(),
            "status": "pending",
            "evidence": None
        }
        try:
            handler = ACTION_MAP[step["action"]]
            event = handler(event)
            event["status"] = "success"
        except Exception as e:
            event["status"] = "error"
            event["evidence"] = str(e)
        events.append(event)
        time.sleep(0.2)
    end = ts()
    output = {
        "scenario": name,
        "started_at": start,
        "finished_at": end,
        "events": events,
        "metadata": {
            "host": platform.node(),
            "platform": platform.platform()
        }
    }
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2)
    print(f"[emulation] Wrote output to {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", default="quick-test", help="Name of scenario to run")
    ap.add_argument("--out", default="demo/output.json", help="Output path for scenario JSON")
    args = ap.parse_args()
    run_scenario(args.scenario, args.out)
