# Team Volcanoes

## Team members: 
Designer - Jon Johnson(john205)
SWE - Ausar Khan(akhan5)
Lead - Ja'Nya Ward(jward12)

### Project Priority (high-low):
1. CPSC Events
2. CPSC Core Curriculum Recommender
3. CPSC Friends
4. CPSC Help Desk
5. CPSC Study Buddies
6. CPSC Course Offering

### NOTE: *Get Dr. Edwards written approval before using any API or package*

---

## Xavier University Event Cancellation System

This system implements event cancellation functionality for Xavier University professors, with three key use cases:

### Use Cases Implemented

#### RP1: Require Reason for Late Cancellations
- Validates cancellation requests based on timing (24-hour rule)
- Requires reason for events starting in less than 24 hours
- Returns detailed validation results or raises errors

#### RP2: RSVP-Based Cancellation Notifications
- Retrieves all RSVPs for canceled events
- Sends cancellation notices only to students who RSVP'd
- Computes urgent flag for events < 24 hours away
- Logs all notifications with timestamps

#### RP3: Calendar Sync for Cancellations
- Generates ICS data with STATUS:CANCELLED
- Syncs to external calendars (Google Calendar, Outlook)
- Records sync results with timestamps
- Maintains audit trail of all sync operations

#### User Story #8: CPSC Event Alert Subscriptions
- Students can subscribe to alerts for CPSC events
- User class with name, email, user_id, role, and alerts list
- Subscribe/unsubscribe functionality with duplicate prevention
- Support for multiple alert types (seminars, workshops, hackathons, etc.)
- Enables students to stay active and engaged in their major

---

## How to Build This Workspace

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd Volcanoes
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `python-dateutil>=2.8.2` - Date/time utilities
   - `icalendar>=5.0.0` - ICS calendar generation

### Project Structure

```
Volcanoes/
├── models/
│   ├── __init__.py
│   ├── event.py              # Event model
│   ├── rsvp.py               # RSVP model
│   ├── user.py               # User model (User Story #8)
│   └── alert.py              # Alert model (User Story #8)
├── services/
│   ├── __init__.py
│   ├── event_cancellation_service.py  # RP1 & RP2 implementation
│   ├── rsvp_service.py                # RSVP management
│   └── calendar_sync_service.py       # RP3 implementation
├── utils/
│   └── notification_utils.py          # Email notifications
├── tests/
│   ├── test_rp1_validation.py         # RP1 tests
│   ├── test_rp2_notifications.py      # RP2 tests
│   ├── test_rp3_calendar_sync.py      # RP3 tests
│   └── test_user_story_8.py           # User Story #8 tests
├── examples/
│   ├── rp1_validation_example.py      # RP1 demo
│   ├── rp2_notification_example.py    # RP2 demo
│   ├── rp3_calendar_sync_example.py   # RP3 demo
│   ├── complete_integration_demo.py   # Full workflow demo
│   └── user_story_8_example.py        # User Story #8 demo
├── requirements.txt
└── README.md
```

---

## Running the System

### Run All Tests

Test each use case independently:

```bash
# Test Use Case RP1 - Validation
python tests/test_rp1_validation.py

# Test Use Case RP2 - Notifications
python tests/test_rp2_notifications.py

# Test Use Case RP3 - Calendar Sync
python tests/test_rp3_calendar_sync.py

# Test User Story #8 - Alert Subscriptions
python tests/test_user_story_8.py
```

### Run Examples

See demonstrations of each use case:

```bash
# Demo Use Case RP1
python examples/rp1_validation_example.py

# Demo Use Case RP2
python examples/rp2_notification_example.py

# Demo Use Case RP3
python examples/rp3_calendar_sync_example.py

# Demo Complete Integration (All Use Cases)
python examples/complete_integration_demo.py

# Demo User Story #8 - Alert Subscriptions
python examples/user_story_8_example.py
```

### Usage in Your Code

```python
from datetime import datetime, timedelta
from models.event import Event
from services.event_cancellation_service import EventCancellationService
from services.calendar_sync_service import CalendarSyncService

# Create an event
event = Event(
    id="evt_001",
    title="Database Review Session",
    description="Final exam prep",
    starts_at=datetime.now() + timedelta(hours=10),
    ends_at=datetime.now() + timedelta(hours=12),
    location="STEM Building, Room 201",
    organizer_id="prof_123",
    organizer_name="Dr. Sarah Edwards"
)

# Initialize services
cancellation_service = EventCancellationService()
calendar_service = CalendarSyncService()

# Validate cancellation (RP1)
validation = cancellation_service.validate_cancellation_reason(
    event,
    "Family emergency"
)

# Cancel the event
event.cancel("Family emergency", datetime.now())

# Notify RSVP'd students (RP2)
notification_result = cancellation_service.notify_rsvp_cancellation(event)

# Sync to external calendars (RP3)
sync_result = calendar_service.sync_event(event)
```

---

## API Reference

### EventCancellationService

#### `validate_cancellation_reason(event, reason) -> Dict`
Validates cancellation based on 24-hour rule.

**Parameters:**
- `event` (Event): The event being canceled
- `reason` (str): Cancellation reason

**Returns:** Dictionary with validation results

**Raises:** `ValidationError` if validation fails

#### `notify_rsvp_cancellation(event) -> Dict`
Sends notifications to all RSVP'd students.

**Parameters:**
- `event` (Event): The canceled event

**Returns:** Dictionary with notification results

### CalendarSyncService

#### `sync_event(event, integrations=None) -> Dict`
Syncs event to external calendars.

**Parameters:**
- `event` (Event): The event to sync
- `integrations` (List[str], optional): Calendar systems to sync to

**Returns:** Dictionary with sync results

---

## Development Notes

- All services include comprehensive logging
- Notification and calendar sync are simulated (would use real APIs in production)
- RSVP service uses in-memory storage (would use database in production)
- Full audit trails maintained for compliance

---

## Testing

All use cases have been tested with:
- ✓ Late cancellations with/without reasons
- ✓ Early cancellations with/without reasons
- ✓ Multiple RSVP scenarios
- ✓ Calendar sync to multiple platforms
- ✓ Error handling and validation

---

## Future Enhancements

- Integrate with real email service (SendGrid, AWS SES)
- Connect to actual calendar APIs (Google Calendar API, Microsoft Graph API)
- Add database persistence (PostgreSQL, MongoDB)
- Implement web interface for professors
- Add SMS notifications for urgent cancellations
- Support for recurring event cancellations