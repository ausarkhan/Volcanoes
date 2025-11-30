"""Unit tests for FeedService."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from models.feed_service import FeedService


def test_add_event_scheduled():
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
    
    assert len(feed_service.feed) == 1
    assert feed_service.feed[0] == event
    print("✓ Test passed: Add scheduled event to feed")


def test_add_event_canceled():
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
    
    assert len(feed_service.feed) == 0
    print("✓ Test passed: Canceled event not added to feed")


def test_remove_event_existing():
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
    assert len(feed_service.feed) == 1
    
    feed_service.remove_event(event)
    assert len(feed_service.feed) == 0
    print("✓ Test passed: Remove existing event from feed")


def test_remove_event_nonexistent():
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
    
    assert len(feed_service.feed) == 0
    print("✓ Test passed: Remove non-existent event doesn't cause errors")


if __name__ == "__main__":
    print("Running FeedService Tests...")
    print("-" * 50)
    test_add_event_scheduled()
    test_add_event_canceled()
    test_remove_event_existing()
    test_remove_event_nonexistent()
    print("-" * 50)
    print("All FeedService tests passed! ✓")
