"""Test suite for Event Cancellation Manager.
Tests cancellation, undo, permissions, and time windows.
"""
import unittest
from datetime import datetime, timedelta
from services.event_cancellation_manager import EventCancellationManager, CancellationError
from models.event import Event
from models.user import User


class TestEventCancellationManager(unittest.TestCase):
    """Test cases for EventCancellationManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = EventCancellationManager()
        
        # Create test users
        self.teacher = User(
            name="Dr. Smith",
            email="smith@xavier.edu",
            user_id="teacher123",
            role="teacher"
        )
        
        self.student_organizer = User(
            name="Alice Johnson",
            email="alice@xavier.edu",
            user_id="student456",
            role="student"
        )
        
        self.other_student = User(
            name="Bob Wilson",
            email="bob@xavier.edu",
            user_id="student789",
            role="student"
        )
        
        # Create test event
        self.event = Event(
            id="event001",
            title="Python Workshop",
            description="Advanced Python programming",
            starts_at=datetime.now() + timedelta(days=2),
            ends_at=datetime.now() + timedelta(days=2, hours=2),
            location="Room 101",
            organizer_id="student456",
            organizer_name="Alice Johnson",
            status="SCHEDULED"
        )
    
    def test_successful_cancellation_by_organizer(self):
        """Test that organizer can cancel their own event."""
        result = self.manager.cancel_event(
            self.event,
            self.student_organizer,
            reason="Instructor unavailable"
        )
        
        self.assertEqual(result['status'], 'CANCELED')
        self.assertEqual(result['canceled_by'], 'student456')
        self.assertEqual(result['reason'], 'Instructor unavailable')
        self.assertTrue(result['notifications_sent'])
        self.assertTrue(result['removed_from_feed'])
        self.assertEqual(self.event.status, 'CANCELED')
        self.assertIsNotNone(result['can_undo_until'])
    
    def test_successful_cancellation_by_teacher(self):
        """Test that teacher can cancel any event."""
        result = self.manager.cancel_event(
            self.event,
            self.teacher,
            reason="De
