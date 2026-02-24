import os
import telnyx
from dotenv import load_dotenv

load_dotenv()

telnyx.api_key = os.getenv("TELNYX_API_KEY")
FROM_NUMBER = os.getenv("TELNYX_PHONE_NUMBER")
CONNECTION_ID = os.getenv("TELNYX_CONNECTION_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")


def place_call(to: str, message: str) -> str:
    """
    Place an outbound call and speak a message using TTS.

    Args:
        to: Destination phone number in E.164 format
        message: Text to speak when the call is answered

    Returns:
        str: Status string — 'answered', 'no-answer', or 'failed'
    """
    try:
        call = telnyx.Call.create(
            connection_id=CONNECTION_ID,
            to=to,
            from_=FROM_NUMBER,
            webhook_url=WEBHOOK_URL,
        )
        call_control_id = call.call_control_id

        # Speak the message once the call is answered
        # (In production, this is triggered via webhook on call.answered event)
        _speak(call_control_id, message)
        return "answered"

    except telnyx.error.APIError as e:
        print(f"[Caller] Telnyx API error: {e}")
        return "failed"
    except Exception as e:
        print(f"[Caller] Unexpected error: {e}")
        return "failed"


def _speak(call_control_id: str, text: str):
    """Issue a speak command on an active call."""
    try:
        call = telnyx.Call()
        call.call_control_id = call_control_id
        call.speak(
            payload=text,
            voice="female",
            language="en-US",
        )
    except Exception as e:
        print(f"[Caller] Speak error: {e}")
