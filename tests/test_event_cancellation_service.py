"""Unit tests for EventCancellationService."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from datetime import datetime, timedelta
from models.event import Event
from models.rsvp import RSVP
from models.feed_service import FeedService
from models.notification_service import NotificationService as FollowerNotificationService
from services.event_cancellation_service import EventCancellationService, ValidationError
from services.rsvp_service import RSVPService
from utils.notification_utils import NotificationService


class TestEventCancellationService(unittest.TestCase):
    """Test cases for EventCancellationService."""
    
    def test_validate_late_cancellation_with_reason(self):
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
    
    self.assertTrue(result['valid'])
    self.assertTrue(result['is_late_cancellation'])
    self.assertLess(result['hours_until_event'], 24)
    
    def test_validate_late_cancellation_without_reason(self):
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
    
    with self.assertRaises(ValidationError) as context:
        result = service.validate_cancellation_reason(event, "")
    
    self.assertIn("Cancellation reason is required", str(context.exception))
    
    def test_notify_rsvp_cancellation_with_rsvps(self):
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
    
    self.assertEqual(result['rsvp_count'], 2)
    self.assertEqual(result['notifications_sent'], 2)
    self.assertTrue(result['urgent'])
    self.assertEqual(len(result['notified_students']), 2)
    
    def test_cancel_event_integration(self):
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
    
    self.assertEqual(result['event_id'], "evt_004")
    self.assertTrue(result['removed_from_feed'])
    self.assertTrue(result['followers_notified'])
    self.assertEqual(len(feed_service.feed), 0)  # Event should be removed from feed
    self.assertEqual(event.status, "CANCELED")


if __name__ == "__main__":
    unittest.main()
