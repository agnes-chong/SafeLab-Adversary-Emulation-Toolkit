# 🧠 SafeLab: Adversary Emulation Toolkit (Ethical Red Team / Purple Team)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Category](https://img.shields.io/badge/Security-Red--Team--Simulation-orange)

> ⚠️ **Disclaimer:** This project is strictly for **educational and research use in isolated lab environments.**  
> Never deploy or use these scripts on systems you do not own or have explicit written authorization to test.

---

## 🧩 Overview

**SafeLab** is an **ethical adversary emulation toolkit** designed for cybersecurity students, red teamers, and defenders who want to **simulate and analyze attacker techniques safely**.

It automates benign attack simulations mapped to the **MITRE ATT&CK framework**, collects telemetry, and generates **HTML reports** highlighting detection coverage and gaps.

Unlike offensive tools, **SafeLab is 100% lab-safe** — no real exploitation, credential access, or persistence techniques are executed.  
Everything runs locally with harmless actions such as spawning processes, writing files, or performing local HTTP requests.

---

## 🚀 Key Features

| Category | Description |
|-----------|-------------|
| 🎯 **Adversary Emulation** | Executes harmless, ATT&CK-mapped test scenarios (process creation, file writes, etc.). |
| 📡 **Telemetry Collection** | Parses JSON outputs or Sysmon/auditd data from lab VMs. |
| 📊 **Reporting Engine** | Generates MITRE-mapped HTML reports with success/detection summaries. |
| 🔬 **Analysis Toolkit** | Includes Jupyter/CLI analysis tools for detection gap analysis. |
| 🧱 **Lab Automation** | Optional Vagrantfile for disposable Ubuntu VMs and safe local servers. |
| 🧠 **Purple-Team Focused** | Designed for both offensive simulation and defensive detection verification. |

---

## 🧪 Quick Demo

```bash
# 1️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run a safe emulation scenario
python emulation/run_emulation.py --scenario quick-test --out demo/output.json

# 4️⃣ Normalize telemetry
python collector/collect.py --input demo/output.json --out demo/collected.json

# 5️⃣ Generate a simple HTML report
python reporting/generate_report.py --input demo/collected.json --out demo/report.html
