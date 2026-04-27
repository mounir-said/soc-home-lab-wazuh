#!/usr/bin/env python3
"""
simulate_brute_force.py
========================
SOC Home Lab — Brute Force Attack Simulator
Author: Mounir Said

Purpose:
    Simulate an SSH brute-force attack against a target host to generate
    realistic security events in Wazuh SIEM for alert triage practice.

Usage:
    python3 simulate_brute_force.py --target 192.168.56.30 --users wordlists/users.txt
    python3 simulate_brute_force.py --target 192.168.56.30 --user root --count 20

WARNING:
    Use ONLY in isolated lab environments. Never run against systems
    you do not own or have explicit written permission to test.
"""

import argparse
import socket
import time
import random
import logging
from datetime import datetime
from typing import Optional

# ── Configure logging ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"brute_force_sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    ]
)
log = logging.getLogger(__name__)

# ── Common weak passwords for simulation ──────────────────────────
WEAK_PASSWORDS = [
    "123456", "password", "admin", "root", "letmein",
    "qwerty", "abc123", "monkey", "master", "dragon",
    "pass123", "welcome", "login", "hello", "admin123",
    "test", "12345678", "iloveyou", "sunshine", "princess",
]


def check_port_open(host: str, port: int = 22, timeout: float = 2.0) -> bool:
    """Verify the target port is reachable before starting simulation."""
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False


def simulate_failed_attempt(
    target: str,
    port: int,
    username: str,
    password: str,
    attempt_num: int,
    delay: float = 0.3
) -> dict:
    """
    Simulate a single failed SSH authentication attempt.
    In a real lab with paramiko installed, this would attempt actual SSH.
    Here we generate the event log entry for SIEM ingestion practice.
    """
    timestamp = datetime.now().isoformat()

    event = {
        "timestamp": timestamp,
        "attempt": attempt_num,
        "target": f"{target}:{port}",
        "username": username,
        "password_tried": "*" * len(password),  # never log real passwords
        "result": "FAILED",
        "mitre_technique": "T1110 - Brute Force",
    }

    log.warning(
        f"[Attempt #{attempt_num:03d}] SSH login FAILED | "
        f"Target: {target}:{port} | User: {username} | "
        f"Password length: {len(password)}"
    )

    time.sleep(delay + random.uniform(0, 0.1))  # randomize timing
    return event


def load_usernames(filepath: Optional[str], single_user: Optional[str]) -> list:
    """Load usernames from file or use single provided username."""
    if single_user:
        return [single_user]
    if filepath:
        try:
            with open(filepath, "r") as f:
                users = [line.strip() for line in f if line.strip()]
            log.info(f"Loaded {len(users)} usernames from {filepath}")
            return users
        except FileNotFoundError:
            log.error(f"User file not found: {filepath}")
            return ["root", "admin", "user", "test"]
    return ["root", "admin", "ubuntu"]


def run_simulation(
    target: str,
    port: int,
    usernames: list,
    count: int,
    delay: float
) -> list:
    """Execute the brute force simulation and return all event records."""

    print("\n" + "="*60)
    print("  SOC HOME LAB — Brute Force Simulation")
    print("="*60)
    print(f"  Target   : {target}:{port}")
    print(f"  Users    : {usernames}")
    print(f"  Attempts : {count}")
    print(f"  Delay    : {delay}s between attempts")
    print("="*60 + "\n")

    # Verify target reachability
    log.info(f"Checking if {target}:{port} is reachable...")
    if not check_port_open(target, port):
        log.warning(
            f"Port {port} on {target} appears closed. "
            "Continuing simulation for log generation purposes."
        )

    events = []
    attempt = 1

    for username in usernames:
        passwords = random.sample(WEAK_PASSWORDS, min(count, len(WEAK_PASSWORDS)))
        for password in passwords:
            if attempt > count:
                break
            event = simulate_failed_attempt(
                target, port, username, password, attempt, delay
            )
            events.append(event)
            attempt += 1

    # Summary
    print("\n" + "="*60)
    print("  SIMULATION COMPLETE — Summary")
    print("="*60)
    print(f"  Total attempts   : {len(events)}")
    print(f"  Unique usernames : {len(set(e['username'] for e in events))}")
    print(f"  Duration         : ~{len(events) * delay:.1f}s")
    print(f"  MITRE Technique  : T1110 — Brute Force")
    print("\n  ✅ Check Wazuh for Rule 100001 alerts")
    print("="*60 + "\n")

    log.info(f"Simulation complete. {len(events)} events generated.")
    return events


def main():
    parser = argparse.ArgumentParser(
        description="SOC Lab — SSH Brute Force Simulator (for SIEM testing only)"
    )
    parser.add_argument("--target", required=True, help="Target IP address")
    parser.add_argument("--port", type=int, default=22, help="SSH port (default: 22)")
    parser.add_argument("--user", help="Single username to test")
    parser.add_argument("--users", help="Path to username wordlist file")
    parser.add_argument("--count", type=int, default=15, help="Number of attempts (default: 15)")
    parser.add_argument("--delay", type=float, default=0.3, help="Delay between attempts in seconds")
    args = parser.parse_args()

    usernames = load_usernames(args.users, args.user)
    run_simulation(args.target, args.port, usernames, args.count, args.delay)


if __name__ == "__main__":
    main()
