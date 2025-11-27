# Xavier University Event Cancellation System

Event cancellation functionality for Xavier University professors.

## Usage

```python
from datetime import datetime, timedelta
from models.event import Event
from services.event_cancellation_service import EventCancellationService

event = Event(
    id="evt_001",
    title="Database Review Session",
    starts_at=datetime.now() + timedelta(hours=10),
    ends_at=datetime.now() + timedelta(hours=12)
)

service = EventCancellationService()
validation = service.validate_cancellation_reason(event, "Family emergency")
event.cancel("Family emergency", datetime.now())
notification_result = service.notify_rsvp_cancellation(event)
```
