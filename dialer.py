#!/usr/bin/env python3
"""
auto-dialer-scheduler
Main scheduling loop — checks contacts and fires calls at the right time.
"""

import time
import argparse
from datetime import datetime
import pytz
import yaml
from contacts import load_contacts, save_contacts
from caller import place_call
from logger import log_call
from notifier import send_confirmation


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def in_call_window(config: dict) -> bool:
    """Return True if the current time is within the configured call window."""
    tz = pytz.timezone(config["call_window"]["timezone"])
    now = datetime.now(tz)
    start = datetime.strptime(config["call_window"]["start"], "%H:%M").time()
    end = datetime.strptime(config["call_window"]["end"], "%H:%M").time()
    return start <= now.time() <= end


def run(dry_run: bool = False, notify: bool = True):
    config = load_config()
    print(f"[Dialer] Starting. Dry run: {dry_run} | SMS notifications: {notify}")

    while True:
        contacts = load_contacts(config["contacts_file"])
        now = datetime.utcnow()

        for contact in contacts:
            if contact["status"] not in ("scheduled", "no-answer"):
                continue

            attempts = int(contact.get("attempts", 0))
            max_attempts = config["retry"]["max_attempts"]

            if attempts >= max_attempts:
                continue

            scheduled = datetime.fromisoformat(contact["scheduled_time"])
            if now < scheduled:
                continue

            if not in_call_window(config):
                print(f"[Dialer] Outside call window, skipping {contact['name']}")
                continue

            print(f"[Dialer] Calling {contact['name']} at {contact['phone_number']}...")

            if dry_run:
                status = "dry-run"
            else:
                status = place_call(
                    to=contact["phone_number"],
                    message=config["message"],
                )
                if notify and status in ("answered", "no-answer", "failed"):
                    send_confirmation(
                        to=contact["phone_number"],
                        name=contact["name"],
                        status=status,
                    )

            contact["attempts"] = attempts + 1
            contact["status"] = status
            log_call(config["log_file"], contact, status)

        save_contacts(config["contacts_file"], contacts)
        time.sleep(60)


def show_log(config: dict):
    import csv
    try:
        with open(config["log_file"], newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print("No call log found yet.")


def main():
    parser = argparse.ArgumentParser(description="Auto-dialer scheduler")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without placing calls")
    parser.add_argument("--no-notify", action="store_true", help="Disable SMS confirmations")
    parser.add_argument("--log", action="store_true", help="Print call log and exit")
    args = parser.parse_args()

    config = load_config()

    if args.log:
        show_log(config)
    else:
        run(dry_run=args.dry_run, notify=not args.no_notify)


if __name__ == "__main__":
    main()
