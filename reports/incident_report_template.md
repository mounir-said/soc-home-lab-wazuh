# SOC Incident Report

| Field | Value |
|-------|-------|
| **Report ID** | IR-2024-001 |
| **Date** | YYYY-MM-DD |
| **Analyst** | Mounir Said |
| **Severity** | High |
| **Status** | Closed |
| **MITRE Technique** | T1110 — Brute Force |

---

## 1. Executive Summary

A brute-force attack was detected against endpoint `192.168.56.30` (Ubuntu Linux Agent).
Wazuh Rule **100001** triggered after **47 failed SSH login attempts** within 60 seconds
from source IP `192.168.56.1`. One successful authentication was subsequently observed,
triggering Rule **100003** (Critical — Possible Compromise).

---

## 2. Timeline of Events

| Time (UTC) | Event | Rule ID | Severity |
|------------|-------|---------|----------|
| 03:14:02 | First failed SSH attempt — user: root | 5716 | Low |
| 03:14:07 | Brute force threshold exceeded (5 attempts/60s) | 100001 | High |
| 03:15:44 | 47 total failed attempts recorded | 100001 | High |
| 03:16:01 | Successful SSH login from same source IP | 5715 | — |
| 03:16:01 | Critical alert: login after brute force | 100003 | Critical |

---

## 3. Technical Details

### Source of Attack
- **Source IP:** 192.168.56.1 (Host machine — simulation)
- **Target:** 192.168.56.30:22 (Ubuntu Linux Agent)
- **Protocol:** SSH (TCP/22)
- **Method:** Dictionary attack using common weak passwords

### Indicators of Compromise (IOCs)
- Source IP: `192.168.56.1`
- Usernames attempted: `root`, `admin`, `ubuntu`, `user`, `test`
- High frequency of Event ID 5716 (SSH auth failure) in short timeframe

### Wazuh Alert Details
```json
{
  "rule": {
    "id": "100001",
    "level": 10,
    "description": "Multiple failed SSH login attempts - Possible brute force"
  },
  "agent": { "name": "ubuntu-agent", "ip": "192.168.56.30" },
  "data": {
    "srcip": "192.168.56.1",
    "dstuser": "root",
    "program_name": "sshd"
  },
  "mitre": { "technique": ["Brute Force"], "id": ["T1110"] }
}
```

---

## 4. Impact Assessment

| Category | Assessment |
|----------|------------|
| Confidentiality | **High risk** — credentials may be compromised |
| Integrity | Under investigation |
| Availability | Not impacted |
| Affected Systems | 1 (ubuntu-agent — 192.168.56.30) |

---

## 5. Containment Actions Taken

1. ✅ Source IP `192.168.56.1` isolated (firewall rule applied)
2. ✅ Compromised user session terminated
3. ✅ User `root` SSH access disabled (`PermitRootLogin no`)
4. ✅ SSH key-based authentication enforced

---

## 6. Root Cause

Weak password policy allowed dictionary attack to succeed.
SSH exposed with root login enabled and no rate-limiting configured.

---

## 7. Recommendations

1. Enforce strong password policy (min 12 chars, complexity required)
2. Disable root SSH login (`PermitRootLogin no` in `/etc/ssh/sshd_config`)
3. Implement SSH rate limiting using `fail2ban`
4. Enable MFA for all remote access
5. Restrict SSH access to known IP ranges via firewall rules

---

## 8. Lessons Learned

This incident demonstrated the effectiveness of Wazuh's correlation rules
in detecting brute-force patterns early. The custom Rule 100003 (successful
login after brute force) proved critical in escalating severity from High to Critical.

---

*Report prepared by: Mounir Said | SOC Home Lab Exercise*
