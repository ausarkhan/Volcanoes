"""
Example usage of EventCancellationService - Use Case RP1

This demonstrates validating cancellation reasons for late cancellations.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from services.event_cancellation_service import EventCancellationService, ValidationError


def example_rp1_validation():
    """Demonstrate Use Case RP1: Require Reason for Late Cancellations."""
    
    service = EventCancellationService()
    
    print("=" * 70)
    print("Use Case RP1: Require Reason for Late Cancellations")
    print("=" * 70)
    
    # Scenario 1: Late cancellation (12 hours) WITH reason - should pass
    print("\n--- Scenario 1: Late cancellation WITH reason ---")
    event1 = Event(
        id="evt_001",
        title="Database Design Review Session",
        description="Review for upcoming exam",
        starts_at=datetime.now() + timedelta(hours=12),
        ends_at=datetime.now() + timedelta(hours=14),
        location="STEM Building, Room 201",
        organizer_id="prof_123",
        organizer_name="Dr. Sarah Edwards"
    )
    
    try:
        result = service.validate_cancellation_reason(
            event1,
            "Unexpected family emergency requires immediate attention"
        )
        print(f"✓ Validation passed: {result['message']}")
        print(f"  - Late cancellation: {result['is_late_cancellation']}")
        print(f"  - Hours until event: {result['hours_until_event']:.1f}")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    # Scenario 2: Late cancellation (8 hours) WITHOUT reason - should fail
    print("\n--- Scenario 2: Late cancellation WITHOUT reason ---")
    event2 = Event(
        id="evt_002",
        title="Algorithm Study Session",
        description="Practice problems",
        starts_at=datetime.now() + timedelta(hours=8),
        ends_at=datetime.now() + timedelta(hours=10),
        location="Library Conference Room",
        organizer_id="prof_456",
        organizer_name="Dr. Michael Chen"
    )
    
    try:
        result = service.validate_cancellation_reason(event2, "")
        print(f"✓ Validation passed: {result['message']}")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    # Scenario 3: Early cancellation (48 hours) WITHOUT reason - should pass
    print("\n--- Scenario 3: Early cancellation WITHOUT reason ---")
    event3 = Event(
        id="evt_003",
        title="Web Development Workshop",
        description="React fundamentals",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=50),
        location="Computer Lab A",
        organizer_id="prof_789",
        organizer_name="Dr. Jennifer Martinez"
    )
    
    try:
        result = service.validate_cancellation_reason(event3, "")
        print(f"✓ Validation passed: {result['message']}")
        print(f"  - Late cancellation: {result['is_late_cancellation']}")
        print(f"  - Hours until event: {result['hours_until_event']:.1f}")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    # Scenario 4: Early cancellation (36 hours) WITH reason - should pass
    print("\n--- Scenario 4: Early cancellation WITH reason ---")
    event4 = Event(
        id="evt_004",
        title="Data Structures Review",
        description="Final exam prep",
        starts_at=datetime.now() + timedelta(hours=36),
        ends_at=datetime.now() + timedelta(hours=38),
        location="STEM Building, Room 305",
        organizer_id="prof_123",
        organizer_name="Dr. Sarah Edwards"
    )
    
    try:
        result = service.validate_cancellation_reason(
            event4,
            "Rescheduling to accommodate more students"
        )
        print(f"✓ Validation passed: {result['message']}")
        print(f"  - Late cancellation: {result['is_late_cancellation']}")
        print(f"  - Hours until event: {result['hours_until_event']:.1f}")
    except ValidationError as e:
        print(f"✗ Validation failed: {e}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_rp1_validation()
