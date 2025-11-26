"""
Test suite for Event Cancellation Manager.
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
            reason="Department scheduling conflict"
        )
        
        self.assertEqual(result['status'], 'CANCELED')
        self.assertEqual(result['canceled_by'], 'teacher123')
        self.assertEqual(self.event.status, 'CANCELED')
    
    def test_cancellation_permission_denied(self):
        """Test that non-organizer student cannot cancel event."""
        with self.assertRaises(CancellationError) as context:
            self.manager.cancel_event(
                self.event,
                self.other_student,
                reason="I don't like it"
            )
        
        self.assertIn("does not have permission", str(context.exception))
        self.assertEqual(self.event.status, 'SCHEDULED')  # Event unchanged
    
    def test_cannot_cancel_already_canceled_event(self):
        """Test that already canceled event cannot be canceled again."""
        # First cancellation
        self.manager.cancel_event(self.event, self.teacher)
        
        # Try to cancel again
        with self.assertRaises(CancellationError) as context:
            self.manager.cancel_event(self.event, self.teacher)
        
        self.assertIn("already canceled", str(context.exception))
    
    def test_successful_undo_within_window(self):
        """Test that cancellation can be undone within time window."""
        # Cancel the event
        cancel_result = self.manager.cancel_event(
            self.event,
            self.student_organizer,
            reason="Made a mistake"
        )
        
        self.assertEqual(self.event.status, 'CANCELED')
        
        # Undo the cancellation
        undo_result = self.manager.undo_cancel(self.event, self.student_organizer)
        
        self.assertEqual(undo_result['status'], 'SCHEDULED')
        self.assertEqual(undo_result['undone_by'], 'student456')
        self.assertTrue(undo_result['restored_to_feed'])
        self.assertTrue(undo_result['notifications_sent'])
        self.assertEqual(self.event.status, 'SCHEDULED')
        self.assertIsNone(self.event.cancellation_reason)
    
    def test_undo_expired_window(self):
        """Test that undo fails after time window expires."""
        # Cancel the event
        self.manager.cancel_event(self.event, self.teacher)
        
        # Manually expire the undo window
        history = self.manager.cancellation_history[self.event.id]
        history['can_undo_until'] = datetime.now() - timedelta(minutes=1)
        
        # Try to undo
        with self.assertRaises(CancellationError) as context:
            self.manager.undo_cancel(self.event, self.teacher)
        
        self.assertIn("Undo window expired", str(context.exception))
        self.assertEqual(self.event.status, 'CANCELED')  # Still canceled
    
    def test_undo_no_history(self):
        """Test that undo fails if no cancellation history exists."""
        with self.assertRaises(CancellationError) as context:
            self.manager.undo_cancel(self.event, self.teacher)
        
        self.assertIn("No cancellation history", str(context.exception))
    
    def test_undo_permission_denied(self):
        """Test that non-authorized user cannot undo cancellation."""
        # Teacher cancels event
        self.manager.cancel_event(self.event, self.teacher)
        
        # Non-organizer student tries to undo
        with self.assertRaises(CancellationError) as context:
            self.manager.undo_cancel(self.event, self.other_student)
        
        self.assertIn("does not have permission", str(context.exception))
    
    def test_can_undo_within_window(self):
        """Test can_undo returns True within time window."""
        self.manager.cancel_event(self.event, self.teacher)
        
        self.assertTrue(self.manager.can_undo(self.event))
    
    def test_can_undo_expired_window(self):
        """Test can_undo returns False after window expires."""
        self.manager.cancel_event(self.event, self.teacher)
        
        # Expire the window
        history = self.manager.cancellation_history[self.event.id]
        history['can_undo_until'] = datetime.now() - timedelta(minutes=1)
        
        self.assertFalse(self.manager.can_undo(self.event))
    
    def test_can_undo_no_history(self):
        """Test can_undo returns False with no history."""
        self.assertFalse(self.manager.can_undo(self.event))
    
    def test_can_undo_after_undo(self):
        """Test can_undo returns False after event already undone."""
        # Cancel and undo
        self.manager.cancel_event(self.event, self.teacher)
        self.manager.undo_cancel(self.event, self.teacher)
        
        # Re-cancel for testing
        self.event.status = 'CANCELED'
        
        # Should not be able to undo again
        self.assertFalse(self.manager.can_undo(self.event))


if __name__ == '__main__':
    unittest.main()
