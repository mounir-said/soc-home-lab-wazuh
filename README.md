# 🛡️ SOC Home Lab — Log Monitoring & Alert Analysis

![Platform](https://img.shields.io/badge/Platform-Wazuh%20SIEM-blue)
![OS](https://img.shields.io/badge/OS-Ubuntu%2022.04%20%7C%20Windows%2010-informational)
![Status](https://img.shields.io/badge/Status-Active-success)
![Author](https://img.shields.io/badge/Author-Mounir%20Said-blueviolet)

A fully functional simulated Security Operations Center (SOC) environment built to practice real-world alert triage, log analysis, and incident response workflows using **Wazuh SIEM**.

---

## 📌 Objective

Simulate a production-like SOC environment to:
- Monitor endpoint activity across Windows and Linux systems
- Detect suspicious behavior using custom Wazuh detection rules
- Practice alert triage and incident documentation following SOC workflows
- Develop hands-on experience with SIEM dashboards and log correlation

---

## 🏗️ Lab Architecture

```
┌─────────────────────────────────────────────────────┐
│                    VirtualBox Host                   │
│                                                     │
│  ┌─────────────────────┐   ┌─────────────────────┐  │
│  │   Wazuh Manager     │   │  Windows 10 Agent   │  │
│  │   Ubuntu 22.04      │◄──│  + Sysmon           │  │
│  │   192.168.56.10     │   │  192.168.56.20      │  │
│  └─────────┬───────────┘   └─────────────────────┘  │
│            │                                        │
│            │               ┌─────────────────────┐  │
│            └───────────────│  Ubuntu Linux Agent │  │
│                            │  192.168.56.30      │  │
│                            └─────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 🧰 Tools & Technologies

| Tool | Role |
|------|------|
| **Wazuh SIEM** | Central log collection, correlation, and alerting |
| **Sysmon** | Deep Windows endpoint telemetry |
| **VirtualBox** | Virtualization of all lab nodes |
| **Windows 10** | Endpoint agent (attack target) |
| **Ubuntu 22.04** | Wazuh Manager + Linux agent |
| **Python** | Attack simulation scripts |

---

## 📁 Repository Structure

```
soc-home-lab/
├── README.md
├── rules/
│   ├── custom_brute_force.xml        # Custom Wazuh rule — brute force detection
│   ├── custom_suspicious_login.xml   # Custom Wazuh rule — off-hours login
│   └── custom_lateral_movement.xml   # Custom Wazuh rule — lateral movement indicator
├── scripts/
│   ├── simulate_brute_force.py       # Simulates SSH/RDP brute-force attack
│   └── simulate_suspicious_login.py  # Simulates off-hours login activity
├── dashboards/
│   └── soc_dashboard_export.json     # Wazuh dashboard export (importable)
├── reports/
│   └── incident_report_template.md   # SOC incident report template
└── screenshots/
    └── (Wazuh dashboard screenshots)
```

---

## ⚙️ Setup Guide

### Prerequisites
- VirtualBox 7.x
- Ubuntu 22.04 ISO
- Windows 10 ISO
- Minimum 8GB RAM on host

### Step 1 — Install Wazuh Manager (Ubuntu)
```bash
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
sudo bash wazuh-install.sh -a
```

### Step 2 — Deploy Sysmon on Windows Agent
```powershell
# Download Sysmon + SwiftOnSecurity config
Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Sysmon.zip" -OutFile "Sysmon.zip"
Expand-Archive Sysmon.zip
.\Sysmon64.exe -accepteula -i sysmonconfig.xml
```

### Step 3 — Install Wazuh Agent on Windows
```powershell
Invoke-WebRequest -Uri "https://packages.wazuh.com/4.x/windows/wazuh-agent-4.7.0-1.msi" -OutFile wazuh-agent.msi
msiexec.exe /i wazuh-agent.msi /q WAZUH_MANAGER="192.168.56.10"
NET START WazuhSvc
```

### Step 4 — Deploy Custom Rules
```bash
# Copy custom rules to Wazuh manager
sudo cp rules/custom_brute_force.xml /var/ossec/etc/rules/
sudo cp rules/custom_suspicious_login.xml /var/ossec/etc/rules/
sudo systemctl restart wazuh-manager
```

---

## 🔍 Detection Scenarios

### Scenario 1 — SSH Brute Force
```bash
# Run simulation
python3 scripts/simulate_brute_force.py --target 192.168.56.30 --users wordlists/users.txt
```
**Expected Alert:** Rule 100001 — `Multiple failed SSH login attempts detected`

### Scenario 2 — Off-Hours Login
```bash
python3 scripts/simulate_suspicious_login.py --user testuser --hour 03
```
**Expected Alert:** Rule 100002 — `Suspicious login outside business hours`

---

## 📊 Key Findings (Sample Run)

| Event | Count | Severity |
|-------|-------|----------|
| Failed SSH logins | 47 | High |
| Off-hours logins | 3 | Medium |
| Privilege escalation attempts | 2 | Critical |
| Successful brute-force | 1 | Critical |

---

## 📄 Incident Report

See [`reports/incident_report_template.md`](reports/incident_report_template.md) for the structured SOC incident report produced from this lab exercise.

---

## 👤 Author

**Mounir Said** — Aspiring SOC Analyst  
[LinkedIn](https://www.linkedin.com/in/said-mounir) | [GitHub](https://github.com/mounir-said)
