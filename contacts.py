import csv
import os


FIELDNAMES = ["name", "phone_number", "scheduled_time", "status", "attempts"]


def load_contacts(filepath: str) -> list[dict]:
    """Load contacts from a CSV file, adding default status fields if missing."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Contacts file not found: {filepath}")

    contacts = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row.setdefault("status", "scheduled")
            row.setdefault("attempts", "0")
            contacts.append(dict(row))
    return contacts


def save_contacts(filepath: str, contacts: list[dict]):
    """Write updated contact list back to CSV."""
    all_fields = list({k for c in contacts for k in c.keys()})
    # Ensure standard fields come first
    ordered = [f for f in FIELDNAMES if f in all_fields]
    ordered += [f for f in all_fields if f not in ordered]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ordered)
        writer.writeheader()
        writer.writerows(contacts)
