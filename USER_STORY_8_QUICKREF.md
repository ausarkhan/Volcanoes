# User Story #8: Quick Reference Guide

## Overview
Xavier students can now subscribe to alerts for CPSC events to stay active in their major.

## Quick Start

### 1. Import the Classes
```python
from models.user import User
from models.alert import Alert
```

### 2. Create a Student User
```python
student = User(
    name="John Doe",
    email="john.doe@xavier.edu",
    user_id="student_001",
    role="student"  # or "teacher"
)
```

### 3. Create Alerts
```python
seminar_alert = Alert(
    alert_id="alert_seminar",
    event_type="seminar",
    description="Get notified about CPSC seminars"
)
```

### 4. Subscribe to Alerts
```python
result = student.subscribe_to_alert(seminar_alert)
print(result)  # "Successfully subscribed"
```

### 5. Unsubscribe from Alerts
```python
result = student.unsubscribe_from_alert(seminar_alert)
print(result)  # "No longer subscribed"
```

## User Class API

### Constructor
```python
User(name, email, user_id, role)
```
- **name**: User's full name (str)
- **email**: User's email address (str)
- **user_id**: Unique identifier (str)
- **role**: Must be "student" or "teacher" (str)

### Attributes
- `user.name` - Full name
- `user.email` - Email address
- `user.user_id` - Unique ID
- `user.role` - Role ("student" or "teacher")
- `user.alerts` - List of subscribed Alert objects

### Methods

#### subscribe_to_alert(alert_obj)
Subscribe to an alert for CPSC events.

**Parameters:**
- `alert_obj` (Alert): Alert object to subscribe to

**Returns:**
- `"Successfully subscribed"` - if subscription successful
- `"Already subscribed to alert: ..."` - if already subscribed

**Example:**
```python
result = student.subscribe_to_alert(hackathon_alert)
```

#### unsubscribe_from_alert(alert_obj)
Unsubscribe from an alert.

**Parameters:**
- `alert_obj` (Alert): Alert object to unsubscribe from

**Returns:**
- `"No longer subscribed"` - if unsubscription successful
- `"Not subscribed to this alert"` - if not subscribed

**Example:**
```python
result = student.unsubscribe_from_alert(hackathon_alert)
```

## Alert Class API

### Constructor
```python
Alert(alert_id, event_type, description)
```
- **alert_id**: Unique identifier for the alert (str)
- **event_type**: Type of event (str)
- **description**: Description of the alert (str)

### Attributes
- `alert.alert_id` - Unique identifier
- `alert.event_type` - Event type
- `alert.description` - Alert description

## Common Alert Types

Suggested event types for CPSC alerts:
- `"seminar"` - Guest speaker seminars
- `"workshop"` - Hands-on workshops
- `"hackathon"` - Hackathon competitions
- `"career_fair"` - Career fair events
- `"study_group"` - Study group sessions
- `"networking"` - Networking events
- `"research"` - Research opportunities
- `"internship"` - Internship announcements

## Example Scenarios

### Scenario 1: Student Subscribes to Multiple Alerts
```python
student = User("Alice", "alice@xavier.edu", "s001", "student")

alerts = [
    Alert("a1", "seminar", "Seminar alerts"),
    Alert("a2", "hackathon", "Hackathon alerts"),
    Alert("a3", "career_fair", "Career fair alerts")
]

for alert in alerts:
    result = student.subscribe_to_alert(alert)
    print(result)

print(f"Total subscriptions: {len(student.alerts)}")
```

### Scenario 2: Preventing Duplicate Subscriptions
```python
alert = Alert("a1", "workshop", "Workshop alerts")

# First subscription
student.subscribe_to_alert(alert)  # "Successfully subscribed"

# Attempt duplicate
student.subscribe_to_alert(alert)  # "Already subscribed..."
```

### Scenario 3: Managing Subscriptions
```python
# Check current subscriptions
print(f"Subscribed to {len(student.alerts)} alerts")

# List all subscriptions
for alert in student.alerts:
    print(f"- {alert.event_type}: {alert.description}")

# Unsubscribe from specific alert
student.unsubscribe_from_alert(some_alert)
```

## Testing

Run the comprehensive test suite:
```bash
python tests/test_user_story_8.py
```

Run the interactive demo:
```bash
python examples/user_story_8_example.py
```

## Error Handling

### Invalid Role
```python
try:
    user = User("Bob", "bob@xavier.edu", "u1", "admin")
except ValueError as e:
    print(e)  # "Role must be 'student' or 'teacher'"
```

### Check Before Unsubscribing
```python
result = student.unsubscribe_from_alert(alert)
if result == "Not subscribed to this alert":
    print("User was not subscribed to this alert")
```

## Integration Points

### With Event System
User alerts can be integrated with the existing event system:
```python
from models.event import Event
from models.user import User
from models.alert import Alert

# When an event is created, notify subscribed users
def notify_subscribers(event, alert_type):
    # Get all users subscribed to this alert type
    # Send notifications to those users
    pass
```

### With Notification Service (RP2)
Alert subscriptions can work with the existing notification service:
```python
from utils.notification_utils import send_notification
from services.rsvp_service import RSVPService

def send_alert_notifications(event, alert_type):
    # Get users subscribed to alert_type
    # Send them notifications about the event
    pass
```

## Best Practices

1. **Validate user role** - Always use "student" or "teacher"
2. **Check subscription status** - Use return messages to verify operations
3. **Avoid duplicates** - The system prevents duplicates automatically
4. **Use descriptive alert IDs** - Make alert_id meaningful (e.g., "alert_cpsc_seminars")
5. **Clear descriptions** - Write clear alert descriptions for users
6. **Handle edge cases** - Check return messages for error conditions

## Support

For questions or issues:
- See full documentation: `USER_STORY_8_SUMMARY.md`
- Run tests: `python tests/test_user_story_8.py`
- Run demo: `python examples/user_story_8_example.py`
- Check main README: `README.md`
