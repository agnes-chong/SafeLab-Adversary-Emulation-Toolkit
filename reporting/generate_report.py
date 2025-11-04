#!/usr/bin/env python3
"""
reporting/generate_report.py

Generate a simple HTML report from normalized demo/report.json.
Usage:
    python reporting/generate_report.py --input demo/report.json --out demo/report.html
"""

import argparse
import json
import os
from datetime import datetime
from html import escape

TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>SafeLab Report - {scenario}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ padding: 8px 10px; border: 1px solid #ddd; text-align: left; }}
    th {{ background: #f4f4f4; }}
    .yes {{ color: green; font-weight: bold; }}
    .no {{ color: red; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>SafeLab — Emulation Report</h1>
  <p><strong>Scenario:</strong> {scenario}</p>
  <p><strong>Host:</strong> {host} &nbsp; <strong>Platform:</strong> {platform}</p>
  <p><strong>Started:</strong> {started_at} &nbsp; <strong>Finished:</strong> {finished_at}</p>

  <h2>Executed Steps</h2>
  <table>
    <thead>
      <tr><th>Timestamp</th><th>Technique</th><th>Action</th><th>Status</th><th>Detected</th><th>Evidence</th></tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

  <h3>Summary</h3>
  <p>Total steps: {total}, Detected: {detected_count}, Missed: {missed_count}</p>

  <h3>MITRE ATT&CK mapping</h3>
  <p>Each technique id corresponds to a MITRE ATT&CK technique. This demo uses benign actions only.</p>

  <h3>Notes & Mitigations</h3>
  <ul>
    <li>Review Sysmon/auditd coverage for process creation and file writes.</li>
    <li>Consider enriching telemetry with command line, parent process, and hashes.</li>
    <li>Run detection scenarios on snapshot-enabled VMs and tune rules iteratively.</li>
  </ul>
</body>
</html>
"""

def generate(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    rows = []
    detected_count = 0
    for a in data.get("alerts", []):
        det = a.get("detected", False)
        if det:
            detected_count += 1
        det_label = '<span class="yes">YES</span>' if det else '<span class="no">NO</span>'
        evidence = escape(a.get("evidence") or "")
        row = "<tr><td>{timestamp}</td><td>{name} ({tid})</td><td>{action}</td><td>{status}</td><td>{det}</td><td>{evidence}</td></tr>".format(
            timestamp=escape(a.get("timestamp", "")),
            name=escape(a.get("technique_name", "")),
            tid=escape(a.get("technique_id", "")),
            action=escape(a.get("action", "")),
            status=escape(a.get("status", "")),
            det=det_label,
            evidence=evidence
        )
        rows.append(row)

    rows_html = "\n".join(rows)
    total = len(data.get("alerts", []))
    missed = total - detected_count

    html = TEMPLATE.format(
        scenario=escape(data.get("scenario", "n/a")),
        host=escape(data.get("host", "n/a")),
        platform=escape(data.get("platform", "n/a")),
        started_at=escape(data.get("started_at", "")),
        finished_at=escape(data.get("finished_at", "")),
        rows=rows_html,
        total=total,
        detected_count=detected_count,
        missed_count=missed
    )

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"[reporting] Generated HTML report: {output_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Generate HTML report from normalized JSON")
    ap.add_argument("--input", "-i", default="demo/report.json", help="Normalized JSON (collector output)")
    ap.add_argument("--out", "-o", default="demo/report.html", help="Output HTML report path")
    args = ap.parse_args()
    generate(args.input, args.out)
