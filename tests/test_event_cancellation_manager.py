"""
Test suite for Event Cancellation Manager.
Tests cancel_event and undo_cancel functionality.
"""

import sys
sys.path.insert(0, '/workspaces/Volcanoes')

from datetime import datetime, timedelta
from models.event import Event
from models.user import User
from services.event_cancellation_manager import EventCancellationManager, CancellationError


def test_cancel_event_success():
    """Test successful event cancellation."""
    print("\n=== Test 1: Cancel Event Successfully ===")
    
    # Create event and user
    event = Event(
        id="evt_001",
        title="Python Workshop",
        description="Advanced Python techniques",
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, hours=2),
        location="Room 101",
        organizer_id="teacher_001",
        organizer_name="Dr. Smith"
    )
    
    teacher = User(
        name="Dr. Smith",
        email="smith@xavier.edu",
        user_id="teacher_001",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    # Cancel event
    result = manager.cancel_event(event, teacher, reason="Instructor illness")
    
    assert result['success'] == True
    assert event.status == 'CANCELED'
    assert event.canceled_by == "teacher_001"
    assert event.cancellation_reason == "Instructor illness"
    assert event.canceled_at is not None
    print("✓ Event canceled successfully")
    print(f"  Event status: {event.status}")
    print(f"  Canceled by: {event.canceled_by}")
    print(f"  Reason: {event.cancellation_reason}")


def test_cancel_without_reason():
    """Test canceling event without providing reason."""
    print("\n=== Test 2: Cancel Event Without Reason ===")
    
    event = Event(
        id="evt_002",
        title="Study Session",
        description="Midterm prep",
        starts_at=datetime.now() + timedelta(days=2),
        ends_at=datetime.now() + timedelta(days=2, hours=1),
        location="Library",
        organizer_id="teacher_002",
        organizer_name="Prof. Jones"
    )
    
    teacher = User(
        name="Prof. Jones",
        email="jones@xavier.edu",
        user_id="teacher_002",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    result = manager.cancel_event(event, teacher)
    
    assert result['success'] == True
    assert event.status == 'CANCELED'
    assert event.cancellation_reason is None
    print("✓ Event canceled without reason")


def test_cancel_permission_denied():
    """Test cancellation with insufficient permissions."""
    print("\n=== Test 3: Cancel Event - Permission Denied ===")
    
    event = Event(
        id="evt_003",
        title="Guest Lecture",
        description="Industry expert talk",
        starts_at=datetime.now() + timedelta(days=3),
        ends_at=datetime.now() + timedelta(days=3, hours=2),
        location="Auditorium",
        organizer_id="teacher_003",
        organizer_name="Dr. Brown"
    )
    
    # Different user (student) trying to cancel
    student = User(
        name="John Doe",
        email="john@xavier.edu",
        user_id="student_001",
        role="student"
    )
    
    manager = EventCancellationManager()
    
    try:
        manager.cancel_event(event, student, reason="Test")
        print("✗ Should have raised CancellationError")
        assert False
    except CancellationError as e:
        print(f"✓ Permission denied as expected: {e}")
        assert "does not have permission" in str(e)


def test_cancel_already_canceled():
    """Test canceling an already canceled event."""
    print("\n=== Test 4: Cancel Already Canceled Event ===")
    
    event = Event(
        id="evt_004",
        title="Hackathon",
        description="24-hour coding event",
        starts_at=datetime.now() + timedelta(days=5),
        ends_at=datetime.now() + timedelta(days=6),
        location="Tech Lab",
        organizer_id="teacher_004",
        organizer_name="Dr. Lee"
    )
    event.status = 'CANCELED'  # Already canceled
    
    teacher = User(
        name="Dr. Lee",
        email="lee@xavier.edu",
        user_id="teacher_004",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    try:
        manager.cancel_event(event, teacher)
        print("✗ Should have raised CancellationError")
        assert False
    except CancellationError as e:
        print(f"✓ Already canceled error as expected: {e}")
        assert "already canceled" in str(e)


def test_undo_cancel_success():
    """Test successful undo of cancellation."""
    print("\n=== Test 5: Undo Cancellation Successfully ===")
    
    event = Event(
        id="evt_005",
        title="Code Review Session",
        description="Team code review",
        starts_at=datetime.now() + timedelta(days=7),
        ends_at=datetime.now() + timedelta(days=7, hours=1),
        location="Room 202",
        organizer_id="teacher_005",
        organizer_name="Prof. White"
    )
    
    teacher = User(
        name="Prof. White",
        email="white@xavier.edu",
        user_id="teacher_005",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    # Cancel event
    cancel_result = manager.cancel_event(event, teacher, reason="Accidental cancellation")
    assert event.status == 'CANCELED'
    print(f"Event canceled: {event.status}")
    
    # Undo cancellation (within 10 minutes)
    undo_result = manager.undo_cancel(event, teacher)
    
    assert undo_result['success'] == True
    assert event.status == 'SCHEDULED'
    assert event.canceled_at is None
    assert event.canceled_by is None
    assert event.cancellation_reason is None
    print("✓ Cancellation undone successfully")
    print(f"  Restored status: {event.status}")
    print(f"  Time elapsed: {undo_result['time_elapsed_seconds']} seconds")


def test_undo_cancel_not_canceled():
    """Test undo on event that is not canceled."""
    print("\n=== Test 6: Undo Non-Canceled Event ===")
    
    event = Event(
        id="evt_006",
        title="Workshop",
        description="Learning session",
        starts_at=datetime.now() + timedelta(days=8),
        ends_at=datetime.now() + timedelta(days=8, hours=2),
        location="Room 303",
        organizer_id="teacher_006",
        organizer_name="Dr. Green"
    )
    event.status = 'SCHEDULED'  # Not canceled
    
    teacher = User(
        name="Dr. Green",
        email="green@xavier.edu",
        user_id="teacher_006",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    try:
        manager.undo_cancel(event, teacher)
        print("✗ Should have raised CancellationError")
        assert False
    except CancellationError as e:
        print(f"✓ Error as expected: {e}")
        assert "is not canceled" in str(e)


def test_undo_cancel_expired_window():
    """Test undo after 10-minute window has expired."""
    print("\n=== Test 7: Undo After Time Window Expired ===")
    
    event = Event(
        id="evt_007",
        title="Seminar",
        description="Tech talk",
        starts_at=datetime.now() + timedelta(days=10),
        ends_at=datetime.now() + timedelta(days=10, hours=1),
        location="Hall A",
        organizer_id="teacher_007",
        organizer_name="Prof. Black"
    )
    
    teacher = User(
        name="Prof. Black",
        email="black@xavier.edu",
        user_id="teacher_007",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    # Cancel event
    manager.cancel_event(event, teacher, reason="Test reason")
    
    # Manually set canceled_at to 11 minutes ago
    event.canceled_at = datetime.now() - timedelta(minutes=11)
    
    try:
        manager.undo_cancel(event, teacher)
        print("✗ Should have raised CancellationError")
        assert False
    except CancellationError as e:
        print(f"✓ Time window expired as expected: {e}")
        assert "Time window expired" in str(e)


def test_undo_cancel_no_history():
    """Test undo when no cancellation history exists."""
    print("\n=== Test 8: Undo Without Cancellation History ===")
    
    event = Event(
        id="evt_008",
        title="Meeting",
        description="Team meeting",
        starts_at=datetime.now() + timedelta(days=12),
        ends_at=datetime.now() + timedelta(days=12, hours=1),
        location="Conference Room",
        organizer_id="teacher_008",
        organizer_name="Dr. Gray"
    )
    event.status = 'CANCELED'
    event.canceled_at = datetime.now()
    
    teacher = User(
        name="Dr. Gray",
        email="gray@xavier.edu",
        user_id="teacher_008",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    try:
        manager.undo_cancel(event, teacher)
        print("✗ Should have raised CancellationError")
        assert False
    except CancellationError as e:
        print(f"✓ No history error as expected: {e}")
        assert "No cancellation history" in str(e)


def test_can_undo_check():
    """Test can_undo helper method."""
    print("\n=== Test 9: Check If Cancellation Can Be Undone ===")
    
    event = Event(
        id="evt_009",
        title="Lab Session",
        description="Hands-on practice",
        starts_at=datetime.now() + timedelta(days=14),
        ends_at=datetime.now() + timedelta(days=14, hours=2),
        location="Lab 101",
        organizer_id="teacher_009",
        organizer_name="Prof. Blue"
    )
    
    teacher = User(
        name="Prof. Blue",
        email="blue@xavier.edu",
        user_id="teacher_009",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    # Before cancellation
    can_undo, reason = manager.can_undo(event)
    assert can_undo == False
    print(f"Before cancellation - Can undo: {can_undo}, Reason: {reason}")
    
    # After cancellation
    manager.cancel_event(event, teacher, reason="Testing undo")
    can_undo, reason = manager.can_undo(event)
    assert can_undo == True
    print(f"After cancellation - Can undo: {can_undo}, Reason: {reason}")
    
    # After time expires
    event.canceled_at = datetime.now() - timedelta(minutes=15)
    can_undo, reason = manager.can_undo(event)
    assert can_undo == False
    print(f"After time expired - Can undo: {can_undo}, Reason: {reason}")
    print("✓ can_undo checks work correctly")


def test_get_cancellation_history():
    """Test retrieving cancellation history."""
    print("\n=== Test 10: Get Cancellation History ===")
    
    event = Event(
        id="evt_010",
        title="Career Fair",
        description="Job opportunities",
        starts_at=datetime.now() + timedelta(days=20),
        ends_at=datetime.now() + timedelta(days=20, hours=4),
        location="Main Hall",
        organizer_id="teacher_010",
        organizer_name="Dean Yellow"
    )
    
    teacher = User(
        name="Dean Yellow",
        email="yellow@xavier.edu",
        user_id="teacher_010",
        role="teacher"
    )
    
    manager = EventCancellationManager()
    
    # Before cancellation
    history = manager.get_cancellation_history("evt_010")
    assert history is None
    print("Before cancellation - No history")
    
    # After cancellation
    manager.cancel_event(event, teacher, reason="Venue unavailable")
    history = manager.get_cancellation_history("evt_010")
    assert history is not None
    assert history['status'] == 'SCHEDULED'
    print(f"After cancellation - History exists: {history['status']}")
    print("✓ Cancellation history retrieved successfully")


def run_all_tests():
    """Run all test cases for Event Cancellation Manager."""
    print("=" * 70)
    print("Event Cancellation Manager - Test Suite")
    print("=" * 70)
    
    try:
        test_cancel_event_success()
        test_cancel_without_reason()
        test_cancel_permission_denied()
        test_cancel_already_canceled()
        test_undo_cancel_success()
        test_undo_cancel_not_canceled()
        test_undo_cancel_expired_window()
        test_undo_cancel_no_history()
        test_can_undo_check()
        test_get_cancellation_history()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED")
        print("=" * 70)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
