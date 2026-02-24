import csv
import os
from datetime import datetime


LOG_FIELDS = ["timestamp", "name", "phone_number", "status", "attempts"]


def log_call(log_file: str, contact: dict, status: str):
    """
    Append a call attempt record to the log CSV.

    Args:
        log_file: Path to the log CSV file
        contact: Contact dict with name, phone_number, attempts
        status: Result status string
    """
    file_exists = os.path.exists(log_file)

    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),
            "name": contact.get("name", ""),
            "phone_number": contact.get("phone_number", ""),
            "status": status,
            "attempts": contact.get("attempts", 1),
        })
