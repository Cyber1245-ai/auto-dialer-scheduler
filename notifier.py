"""
notifier.py — Send SMS confirmation messages after call attempts.
Uses the Telnyx Messaging API to notify contacts of call outcomes.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELNYX_API_KEY = os.getenv("TELNYX_API_KEY")
FROM_NUMBER = os.getenv("TELNYX_PHONE_NUMBER")


def send_confirmation(to: str, name: str, status: str):
    """
    Send an SMS to a contact confirming the outcome of a call attempt.

    Args:
        to: Recipient phone number in E.164 format
        name: Contact's name
        status: Call outcome ('answered', 'no-answer', 'failed')
    """
    messages = {
        "answered": f"Hi {name}, thanks for taking our call. Have a great day!",
        "no-answer": f"Hi {name}, we tried to reach you but couldn't connect. We'll try again shortly.",
        "failed": f"Hi {name}, we were unable to complete your call. Please contact us directly.",
    }
    text = messages.get(status, f"Hi {name}, we attempted to reach you.")

    url = "https://api.telnyx.com/v2/messages"
    headers = {
        "Authorization": f"Bearer {TELNYX_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "from": FROM_NUMBER,
        "to": to,
        "text": text,
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        resp.raise_for_status()
        print(f"[Notifier] SMS sent to {to}: {text}")
    except requests.RequestException as e:
        print(f"[Notifier] Failed to send SMS to {to}: {e}")
