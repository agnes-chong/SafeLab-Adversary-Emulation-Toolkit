# Purple-Team Playbook (SafeLab Quick Playbook)

This playbook describes a simple purple-team exercise workflow you can run in a lab using SafeLab.

## Objective
Validate detection coverage for a small set of attacker techniques (execution, file writes, exfil simulation) and identify detection gaps.

## Pre-exercise Setup
1. Provision two disposable VMs (attacker & defender) or a single multi-role VM using `lab-setup/Vagrantfile`.  
2. Snapshot both VMs.  
3. Ensure the defender VM has local telemetry capture enabled (e.g., Sysmon on Windows, auditd/rsyslog on Linux).  
4. Install SafeLab in a project folder on the attacker VM or the single VM. Create a Python venv and `pip install -r requirements.txt`.

## Scenario Selection
- Start with `quick-test` (process spawn, file create, localhost POST).
- Later add more scenarios (e.g., simulated persistence via registry keys inside snapshots, sudo activity on Linux).

## Exercise Steps
1. **Start telemetry collection** on defender (e.g., start Sysmon and export baseline logs).  
2. **Run the emulation**:
    ```bash
    python emulation/run_emulation.py --scenario quick-test --out demo/output.json
    ```
3. **Collect & Normalize**:
    ```bash
    python collector/collect.py --input demo/output.json --out demo/report.json
    ```
4. **Report**:
    ```bash
    python reporting/generate_report.py --input demo/report.json --out demo/report.html
    ```
5. **Analyze** (Jupyter or script):
    ```bash
    python analysis/analysis_stub.py demo/report.json
    ```
6. **Discuss**:
   - For each technique, review evidence and detection flag (detected: true/false).
   - Note missed detections and hypothesize improvements (Sysmon config, rule tuning).
   - Document mitigations and playbook changes.

## Post-Exercise
- Revert VMs to snapshots.
- Upload sanitized reports/artifacts to a secure location for team review.

## Example Questions for Retrospective
- Which techniques were detected reliably? Which were missed?
- Did telemetry include sufficient context (command line, parent process, hashes)?
- What changes to telemetry configuration or detection rules would reduce false negatives?
- How to operationalize the detection rule (SIEM rule, EDR policy, endpoint IOC)?

## Extensions (Optional)
- Integrate with Atomic Red Team playbooks (strictly in lab).  
- Feed telemetry into ELK/Elastic or Splunk for realistic detection testing.  
- Add timing/latency measurement for detection (time between execution and alert).

## Notes
- This playbook is intentionally high-level — adapt steps to your class, lab, or hiring-test constraints.
- Always follow the ETHICS & LAB RULES in `docs/ETHICS.md`.
