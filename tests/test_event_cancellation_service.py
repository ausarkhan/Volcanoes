"""Unit tests for EventCancellationService."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from models.rsvp import RSVP
from models.feed_service import FeedService
from models.notification_service import NotificationService as FollowerNotificationService
from services.event_cancellation_service import EventCancellationService, ValidationError
from services.rsvp_service import RSVPService
from utils.notification_utils import NotificationService


def test_validate_late_cancellation_with_reason():
    """Test late cancellation (< 24 hours) with valid reason passes validation."""
    service = EventCancellationService()
    
    event = Event(
        id="evt_001",
        title="Test Event",
        description="Test Description",
        starts_at=datetime.now() + timedelta(hours=12),
        ends_at=datetime.now() + timedelta(hours=14),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test"
    )
    
    result = service.validate_cancellation_reason(event, "Emergency situation")
    
    assert result['valid'] == True
    assert result['is_late_cancellation'] == True
    assert result['hours_until_event'] < 24
    print("✓ Test passed: Late cancellation with reason")


def test_validate_late_cancellation_without_reason():
    """Test late cancellation (< 24 hours) without reason fails validation."""
    service = EventCancellationService()
    
    event = Event(
        id="evt_002",
        title="Test Event",
        description="Test Description",
        starts_at=datetime.now() + timedelta(hours=8),
        ends_at=datetime.now() + timedelta(hours=10),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test"
    )
    
    try:
        result = service.validate_cancellation_reason(event, "")
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert "Cancellation reason is required" in str(e)
        print("✓ Test passed: Late cancellation without reason raises error")


def test_notify_rsvp_cancellation_with_rsvps():
    """Test notifying students who RSVP'd to canceled event."""
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    feed_service = FeedService()
    follower_service = FollowerNotificationService()
    cancellation_service = EventCancellationService(
        rsvp_service, 
        notification_service,
        feed_service,
        follower_service
    )
    
    event = Event(
        id="evt_003",
        title="Test Event",
        description="Test Description",
        starts_at=datetime.now() + timedelta(hours=10),
        ends_at=datetime.now() + timedelta(hours=12),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test"
    )
    event.cancel("Test reason", datetime.now())
    
    # Add RSVPs
    rsvp1 = RSVP(
        id="rsvp_001",
        event_id="evt_003",
        student_id="stu_001",
        student_name="Student One",
        student_email="student1@test.edu",
        status="CONFIRMED",
        created_at=datetime.now()
    )
    rsvp2 = RSVP(
        id="rsvp_002",
        event_id="evt_003",
        student_id="stu_002",
        student_name="Student Two",
        student_email="student2@test.edu",
        status="CONFIRMED",
        created_at=datetime.now()
    )
    rsvp_service.add_rsvp(rsvp1)
    rsvp_service.add_rsvp(rsvp2)
    
    result = cancellation_service.notify_rsvp_cancellation(event)
    
    assert result['rsvp_count'] == 2
    assert result['notifications_sent'] == 2
    assert result['urgent'] == True
    assert len(result['notified_students']) == 2
    print("✓ Test passed: Notify RSVP'd students")


def test_cancel_event_integration():
    """Test complete event cancellation with FeedService and NotificationService integration."""
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    feed_service = FeedService()
    follower_service = FollowerNotificationService()
    cancellation_service = EventCancellationService(
        rsvp_service,
        notification_service,
        feed_service,
        follower_service
    )
    
    event = Event(
        id="evt_004",
        title="Test Event",
        description="Test Description",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=50),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test",
        status="SCHEDULED"
    )
    
    # Add event to feed first
    feed_service.add_event(event)
    assert len(feed_service.feed) == 1
    
    # Cancel event
    result = cancellation_service.cancel_event(event, "Rescheduling")
    
    assert result['event_id'] == "evt_004"
    assert result['removed_from_feed'] == True
    assert result['followers_notified'] == True
    assert len(feed_service.feed) == 0  # Event should be removed from feed
    assert event.status == "CANCELED"
    print("✓ Test passed: Complete event cancellation integration")


if __name__ == "__main__":
    print("Running EventCancellationService Tests...")
    print("-" * 50)
    test_validate_late_cancellation_with_reason()
    test_validate_late_cancellation_without_reason()
    test_notify_rsvp_cancellation_with_rsvps()
    test_cancel_event_integration()
    print("-" * 50)
    print("All EventCancellationService tests passed! ✓")
