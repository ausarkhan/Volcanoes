"""Unit tests for Use Case RP1: Require Reason for Late Cancellations."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from services.event_cancellation_service import EventCancellationService, ValidationError


def test_late_cancellation_with_reason():
    """Test late cancellation (< 24 hours) with valid reason."""
    service = EventCancellationService()
    event = Event(
        id="evt_001",
        title="Database Review",
        description="Test event",
        starts_at=datetime.now() + timedelta(hours=12),
        ends_at=datetime.now() + timedelta(hours=14),
        location="Room 201",
        organizer_id="prof_123",
        organizer_name="Dr. Edwards"
    )
    
    result = service.validate_cancellation_reason(event, "Family emergency")
    assert result['valid'] == True
    assert result['is_late_cancellation'] == True
    print("✓ Test passed: Late cancellation with reason")


def test_late_cancellation_without_reason():
    """Test late cancellation (< 24 hours) without reason - should fail."""
    service = EventCancellationService()
    event = Event(
        id="evt_002",
        title="Algorithm Session",
        description="Test event",
        starts_at=datetime.now() + timedelta(hours=8),
        ends_at=datetime.now() + timedelta(hours=10),
        location="Library",
        organizer_id="prof_456",
        organizer_name="Dr. Chen"
    )
    
    try:
        result = service.validate_cancellation_reason(event, "")
        assert False, "Should have raised ValidationError"
    except ValidationError as e:
        assert "Cancellation reason is required" in str(e)
        print("✓ Test passed: Late cancellation without reason raises error")


def test_early_cancellation_without_reason():
    """Test early cancellation (> 24 hours) without reason - should pass."""
    service = EventCancellationService()
    event = Event(
        id="evt_003",
        title="Web Workshop",
        description="Test event",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=50),
        location="Lab A",
        organizer_id="prof_789",
        organizer_name="Dr. Martinez"
    )
    
    result = service.validate_cancellation_reason(event, "")
    assert result['valid'] == True
    assert result['is_late_cancellation'] == False
    print("✓ Test passed: Early cancellation without reason")


def test_early_cancellation_with_reason():
    """Test early cancellation (> 24 hours) with reason - should pass."""
    service = EventCancellationService()
    event = Event(
        id="evt_004",
        title="Data Structures Review",
        description="Test event",
        starts_at=datetime.now() + timedelta(hours=36),
        ends_at=datetime.now() + timedelta(hours=38),
        location="Room 305",
        organizer_id="prof_123",
        organizer_name="Dr. Edwards"
    )
    
    result = service.validate_cancellation_reason(event, "Rescheduling")
    assert result['valid'] == True
    assert result['is_late_cancellation'] == False
    print("✓ Test passed: Early cancellation with reason")


if __name__ == "__main__":
    print("Running Use Case RP1 Tests...")
    print("-" * 50)
    test_late_cancellation_with_reason()
    test_late_cancellation_without_reason()
    test_early_cancellation_without_reason()
    test_early_cancellation_with_reason()
    print("-" * 50)
    print("All tests passed! ✓")
