# auto-dialer-scheduler

A Python-based scheduled auto-dialer that reads a contact list and automatically places outbound voice calls at specified times using the [Telnyx](https://telnyx.com) Call Control API. Useful for appointment reminders, notification calls, and automated outreach workflows.

## Features

- Schedule outbound calls from a CSV contact list
- Configurable call time windows (e.g., only call between 9am–8pm)
- Text-to-speech message delivery via Telnyx
- Retry logic for unanswered or failed calls
- Call log with status tracking (answered, no-answer, failed)
- Timezone-aware scheduling
- Simple YAML-based configuration

## Requirements

- Python 3.9+
- A [Telnyx](https://telnyx.com) account with Call Control enabled
- `pip install -r requirements.txt`

## Installation

```bash
git clone https://github.com/Cyber1245-ai/auto-dialer-scheduler.git
cd auto-dialer-scheduler
pip install -r requirements.txt
cp .env.example .env
cp config.example.yaml config.yaml
# Edit both files with your credentials and settings
```

## Configuration

**`.env`** — API credentials:
```
TELNYX_API_KEY=your_api_key_here
TELNYX_PHONE_NUMBER=+1XXXXXXXXXX
TELNYX_CONNECTION_ID=your_connection_id
```

**`config.yaml`** — dialer settings:
```yaml
call_window:
  start: "09:00"
  end:   "20:00"
  timezone: "America/New_York"

message: "Hello, this is a reminder for your appointment tomorrow at 2pm. Press 1 to confirm or 2 to cancel."

retry:
  max_attempts: 3
  delay_minutes: 30

contacts_file: contacts.csv
log_file: call_log.csv
```

## Contacts CSV Format

```csv
name,phone_number,scheduled_time
John Smith,+12025551234,2025-06-01 10:00
Jane Doe,+13105559876,2025-06-01 11:30
```

## Usage

### Run the dialer

```bash
python dialer.py
```

The dialer checks the contact list every minute and places calls when the scheduled time arrives and the current time is within the configured call window.

### Dry run (no calls placed)

```bash
python dialer.py --dry-run
```

### View call log

```bash
python dialer.py --log
```

## Project Structure

```
auto-dialer-scheduler/
├── dialer.py           # Main scheduler loop
├── caller.py           # Telnyx call logic
├── contacts.py         # Contact list loader and tracker
├── logger.py           # Call log writer
├── config.example.yaml
├── contacts.example.csv
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Call Log Fields

| Field | Description |
|---|---|
| `timestamp` | When the call was attempted |
| `name` | Contact name |
| `phone_number` | Dialed number |
| `status` | `answered`, `no-answer`, `failed`, `scheduled` |
| `attempts` | Number of dial attempts made |

## License

MIT License. See [LICENSE](LICENSE) for details.
