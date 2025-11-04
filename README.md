# 🧠 SafeLab: Adversary Emulation Toolkit (Ethical Red Team / Purple Team)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Category](https://img.shields.io/badge/Security-Red--Team--Simulation-orange)

> ⚠️ **Disclaimer:** This project is strictly for **educational and research use in isolated lab environments.**  
> Never deploy or use these scripts on systems you do not own or have explicit written authorization to test.

---

## 🧩 Overview

**SafeLab** is an **ethical adversary emulation toolkit** designed for cybersecurity students, red teamers, and defenders who want to **simulate and analyze attacker techniques safely**.

It automates benign attack simulations mapped to the **MITRE ATT&CK framework**, collects telemetry, and generates **HTML reports** highlighting detection coverage and gaps.

Everything in this repo is intentionally harmless — actions are limited to safe activities like spawning processes, writing files, and local HTTP requests.

---

## 🚀 Quickstart (safe demo)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run a safe emulation scenario
python emulation/run_emulation.py --scenario quick-test --out demo/output.json

# Normalize telemetry (collector)
python collector/collect.py --input demo/output.json --out demo/report.json

# Generate HTML report
python reporting/generate_report.py --input demo/report.json --out demo/report.html

# View the report (open demo/report.html in your browser)
