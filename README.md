# Xavier University Event Management System

Event management functionality for Xavier University professors and students.

## Features

- **Course Events (P1)**: Professors can create exam review sessions and course-related events
- **Event Cancellation (RP1)**: Require reasons for late cancellations (< 24 hours)
- **RSVP Notifications (RP2)**: Automatic notifications when events are canceled
- **Calendar Sync (RP3)**: Sync canceled events to Google Calendar, Outlook, and iCal
- **Feed Management**: Event feed with automatic filtering of canceled events
- **Notification Service**: Notify followers when events are canceled

## Installation

No external dependencies required. This project uses Python 3.x standard library.

Optional: Install `icalendar` for enhanced calendar functionality:
```bash
pip install icalendar
```

## How to Run

### Run Examples

Each use case has a demo example you can run:

**P1 - Course Event (Professor creates exam review session):**
```bash
python examples/p1_course_event_example.py
```

**RP1 - Validation (Require reason for late cancellations):**
```bash
python examples/rp1_validation_example.py
```

**RP2 - Notifications (RSVP-based cancellation notifications):**
```bash
python examples/rp2_notification_example.py
```

**RP3 - Calendar Sync (Sync cancellations to calendars):**
```bash
python examples/rp3_calendar_sync_example.py
```

### Run Tests

Run all tests:
```bash
python -m unittest discover tests/
```

Run specific test file:
```bash
python -m unittest tests/test_feed_service.py
python -m unittest tests/test_event_cancellation_service.py
python -m unittest tests/test_calendar_sync_service.py
```

## Project Structure

```
models/              # Data models (Event, RSVP, FeedService, NotificationService)
services/            # Business logic services
examples/            # Demo scripts for each use case
tests/               # Unit tests
utils/               # Utility functions
```

## Use Cases Implemented

- **P1**: Course Event (Professor) - SHA: beb62af
- **RP1**: Require Reason for Late Cancellations - SHA: c552fd9
- **RP2**: RSVP-Based Cancellation Notifications - SHA: c552fd9
- **RP3**: Calendar Sync for Cancellations - SHA: c552fd9
- **Feed & Notification Services** - SHA: 9886a0b, c0edce3, dd1fe1a, 003cb3c
