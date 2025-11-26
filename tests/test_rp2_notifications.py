"""Unit tests for Use Case RP2: RSVP-Based Cancellation Notifications."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from models.rsvp import RSVP
from services.event_cancellation_service import EventCancellationService
from services.rsvp_service import RSVPService
from utils.notification_utils import NotificationService


def test_urgent_cancellation_with_rsvps():
    """Test urgent cancellation (< 24 hours) with multiple RSVPs."""
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    cancellation_service = EventCancellationService(rsvp_service, notification_service)
    
    event = Event(
        id="evt_test_001",
        title="Test Event",
        description="Test",
        starts_at=datetime.now() + timedelta(hours=10),
        ends_at=datetime.now() + timedelta(hours=12),
        location="Test Location",
        organizer_id="prof_test",
        organizer_name="Test Prof"
    )
    event.cancel("Test reason", datetime.now())
    
    # Add 2 RSVPs
    rsvp1 = RSVP("rsvp1", "evt_test_001", "stu1", "Student One", "s1@test.edu", "CONFIRMED", datetime.now())
    rsvp2 = RSVP("rsvp2", "evt_test_001", "stu2", "Student Two", "s2@test.edu", "CONFIRMED", datetime.now())
    rsvp_service.add_rsvp(rsvp1)
    rsvp_service.add_rsvp(rsvp2)
    
    result = cancellation_service.notify_rsvp_cancellation(event)
    
    assert result['rsvp_count'] == 2
    assert result['notifications_sent'] == 2
    assert result['urgent'] == True
    assert len(result['notified_students']) == 2
    print("✓ Test passed: Urgent cancellation with RSVPs")


def test_non_urgent_cancellation_with_rsvps():
    """Test non-urgent cancellation (> 24 hours) with RSVPs."""
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    cancellation_service = EventCancellationService(rsvp_service, notification_service)
    
    event = Event(
        id="evt_test_002",
        title="Test Event 2",
        description="Test",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=50),
        location="Test Location",
        organizer_id="prof_test",
        organizer_name="Test Prof"
    )
    event.cancel("Test reason", datetime.now())
    
    # Add 1 RSVP
    rsvp1 = RSVP("rsvp3", "evt_test_002", "stu3", "Student Three", "s3@test.edu", "CONFIRMED", datetime.now())
    rsvp_service.add_rsvp(rsvp1)
    
    result = cancellation_service.notify_rsvp_cancellation(event)
    
    assert result['rsvp_count'] == 1
    assert result['notifications_sent'] == 1
    assert result['urgent'] == False
    assert len(result['notified_students']) == 1
    print("✓ Test passed: Non-urgent cancellation with RSVPs")


def test_cancellation_with_no_rsvps():
    """Test cancellation with no RSVPs - no notifications sent."""
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    cancellation_service = EventCancellationService(rsvp_service, notification_service)
    
    event = Event(
        id="evt_test_003",
        title="Test Event 3",
        description="Test",
        starts_at=datetime.now() + timedelta(hours=12),
        ends_at=datetime.now() + timedelta(hours=14),
        location="Test Location",
        organizer_id="prof_test",
        organizer_name="Test Prof"
    )
    event.cancel("Test reason", datetime.now())
    
    # No RSVPs added
    
    result = cancellation_service.notify_rsvp_cancellation(event)
    
    assert result['rsvp_count'] == 0
    assert result['notifications_sent'] == 0
    assert len(result['notified_students']) == 0
    print("✓ Test passed: Cancellation with no RSVPs")


def test_notification_logging():
    """Test that notifications are properly logged."""
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    cancellation_service = EventCancellationService(rsvp_service, notification_service)
    
    event = Event(
        id="evt_test_004",
        title="Test Event 4",
        description="Test",
        starts_at=datetime.now() + timedelta(hours=15),
        ends_at=datetime.now() + timedelta(hours=17),
        location="Test Location",
        organizer_id="prof_test",
        organizer_name="Test Prof"
    )
    event.cancel("Test reason", datetime.now())
    
    # Add RSVP
    rsvp1 = RSVP("rsvp4", "evt_test_004", "stu4", "Student Four", "s4@test.edu", "CONFIRMED", datetime.now())
    rsvp_service.add_rsvp(rsvp1)
    
    # Send notifications
    result = cancellation_service.notify_rsvp_cancellation(event)
    
    # Check logs
    logs = notification_service.get_notification_logs(event_id="evt_test_004")
    assert len(logs) == 1
    assert logs[0].student_id == "stu4"
    assert logs[0].notification_type == "CANCELLATION"
    print("✓ Test passed: Notification logging")


if __name__ == "__main__":
    print("Running Use Case RP2 Tests...")
    print("-" * 50)
    test_urgent_cancellation_with_rsvps()
    test_non_urgent_cancellation_with_rsvps()
    test_cancellation_with_no_rsvps()
    test_notification_logging()
    print("-" * 50)
    print("All tests passed! ✓")
