"""Unit tests for FeedService."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from datetime import datetime, timedelta
from models.event import Event
from models.feed_service import FeedService


class TestFeedService(unittest.TestCase):
    """Test cases for FeedService."""
    
    def test_add_event_scheduled(self):
        """Test adding a scheduled event successfully adds it to the feed."""
        feed_service = FeedService()
        
        event = Event(
            id="evt_001",
            title="Test Event",
            description="Test Description",
            starts_at=datetime.now() + timedelta(hours=24),
            ends_at=datetime.now() + timedelta(hours=26),
            location="Test Location",
            organizer_id="prof_123",
            organizer_name="Dr. Test",
            status="SCHEDULED"
        )
        
        feed_service.add_event(event)
        
        self.assertEqual(len(feed_service.feed), 1)
        self.assertEqual(feed_service.feed[0], event)
    
    def test_add_event_canceled(self):
        """Test adding a canceled event does NOT add it to the feed."""
        feed_service = FeedService()
        
        event = Event(
            id="evt_002",
            title="Canceled Event",
            description="Test Description",
            starts_at=datetime.now() + timedelta(hours=24),
            ends_at=datetime.now() + timedelta(hours=26),
            location="Test Location",
            organizer_id="prof_123",
            organizer_name="Dr. Test",
            status="CANCELED"
        )
        
        feed_service.add_event(event)
        
        self.assertEqual(len(feed_service.feed), 0)
    
    def test_remove_event_existing(self):
        """Test removing an existing event successfully removes it from the feed."""
        feed_service = FeedService()
        
        event = Event(
            id="evt_003",
            title="Test Event",
            description="Test Description",
            starts_at=datetime.now() + timedelta(hours=24),
            ends_at=datetime.now() + timedelta(hours=26),
            location="Test Location",
            organizer_id="prof_123",
            organizer_name="Dr. Test",
            status="SCHEDULED"
        )
        
        feed_service.add_event(event)
        self.assertEqual(len(feed_service.feed), 1)
        
        feed_service.remove_event(event)
        self.assertEqual(len(feed_service.feed), 0)
    
    def test_remove_event_nonexistent(self):
        """Test removing a non-existent event doesn't cause errors."""
        feed_service = FeedService()
        
        event = Event(
            id="evt_004",
            title="Test Event",
            description="Test Description",
            starts_at=datetime.now() + timedelta(hours=24),
            ends_at=datetime.now() + timedelta(hours=26),
            location="Test Location",
            organizer_id="prof_123",
            organizer_name="Dr. Test",
            status="SCHEDULED"
        )
        
        # Try to remove event that was never added
        feed_service.remove_event(event)
        
        self.assertEqual(len(feed_service.feed), 0)


if __name__ == "__main__":
    unittest.main()
