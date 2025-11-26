"""
Example demonstrating Event Cancellation Manager.
Shows cancel_event and undo_cancel functionality.
"""

import sys
sys.path.insert(0, '/workspaces/Volcanoes')

from datetime import datetime, timedelta
from models.event import Event
from models.user import User
from services.event_cancellation_manager import EventCancellationManager, CancellationError
import time


def main():
    print("=" * 80)
    print("Event Cancellation Manager - Demo")
    print("=" * 80)
    print()
    
    # Create users
    print("--- Creating Users ---")
    teacher = User(
        name="Dr. Sarah Edwards",
        email="s.edwards@xavier.edu",
        user_id="teacher_001",
        role="teacher"
    )
    print(f"Teacher: {teacher}")
    
    student = User(
        name="John Doe",
        email="john.doe@xavier.edu",
        user_id="student_001",
        role="student"
    )
    print(f"Student: {student}")
    print()
    
    # Create event
    print("--- Creating Event ---")
    event = Event(
        id="evt_python_workshop",
        title="Advanced Python Workshop",
        description="Deep dive into Python decorators and metaclasses",
        starts_at=datetime.now() + timedelta(days=7),
        ends_at=datetime.now() + timedelta(days=7, hours=3),
        location="STEM Building, Room 301",
        organizer_id="teacher_001",
        organizer_name="Dr. Sarah Edwards"
    )
    print(f"Event: {event.title}")
    print(f"  ID: {event.id}")
    print(f"  Organizer: {event.organizer_name}")
    print(f"  Status: {event.status}")
    print(f"  Location: {event.location}")
    print()
    
    # Initialize manager
    manager = EventCancellationManager()
    
    # Scenario 1: Student tries to cancel (should fail)
    print("=" * 80)
    print("Scenario 1: Student Attempts to Cancel Event")
    print("=" * 80)
    try:
        manager.cancel_event(event, student, reason="I don't want to attend")
    except CancellationError as e:
        print(f"✗ Cancellation failed (as expected): {e}")
    print()
    
    # Scenario 2: Teacher cancels event successfully
    print("=" * 80)
    print("Scenario 2: Teacher Cancels Event")
    print("=" * 80)
    result = manager.cancel_event(
        event, 
        teacher, 
        reason="Instructor has a family emergency"
    )
    print(f"\nCancellation Result:")
    print(f"  Success: {result['success']}")
    print(f"  Canceled by: {result['canceled_by']}")
    print(f"  Reason: {result['reason']}")
    print(f"  Notifications sent: {result['notifications_sent']}")
    print(f"\nEvent Status After Cancellation:")
    print(f"  Status: {event.status}")
    print(f"  Canceled by: {event.canceled_by}")
    print(f"  Canceled at: {event.canceled_at}")
    print(f"  Reason: {event.cancellation_reason}")
    print()
    
    # Scenario 3: Try to cancel again (should fail)
    print("=" * 80)
    print("Scenario 3: Attempt to Cancel Already Canceled Event")
    print("=" * 80)
    try:
        manager.cancel_event(event, teacher, reason="Another reason")
    except CancellationError as e:
        print(f"✗ Cancellation failed (as expected): {e}")
    print()
    
    # Scenario 4: Check if can undo
    print("=" * 80)
    print("Scenario 4: Check If Cancellation Can Be Undone")
    print("=" * 80)
    can_undo, reason = manager.can_undo(event)
    print(f"Can undo: {can_undo}")
    print(f"Reason: {reason}")
    print()
    
    # Scenario 5: Teacher undoes cancellation
    print("=" * 80)
    print("Scenario 5: Teacher Undoes Cancellation (Within 10 Minutes)")
    print("=" * 80)
    print("Waiting 2 seconds to simulate time passage...")
    time.sleep(2)
    
    undo_result = manager.undo_cancel(event, teacher)
    print(f"\nUndo Result:")
    print(f"  Success: {undo_result['success']}")
    print(f"  Restored by: {undo_result['restored_by']}")
    print(f"  Restored status: {undo_result['restored_status']}")
    print(f"  Time elapsed: {undo_result['time_elapsed_seconds']} seconds")
    print(f"  Notifications sent: {undo_result['notifications_sent']}")
    print(f"\nEvent Status After Undo:")
    print(f"  Status: {event.status}")
    print(f"  Canceled at: {event.canceled_at}")
    print(f"  Canceled by: {event.canceled_by}")
    print(f"  Reason: {event.cancellation_reason}")
    print()
    
    # Scenario 6: Create another event and test expired window
    print("=" * 80)
    print("Scenario 6: Undo After Time Window Expires")
    print("=" * 80)
    event2 = Event(
        id="evt_database_review",
        title="Database Systems Review",
        description="Midterm preparation",
        starts_at=datetime.now() + timedelta(days=3),
        ends_at=datetime.now() + timedelta(days=3, hours=2),
        location="Library Study Room B",
        organizer_id="teacher_001",
        organizer_name="Dr. Sarah Edwards"
    )
    print(f"New Event: {event2.title}")
    
    # Cancel the event
    manager.cancel_event(event2, teacher, reason="Testing time window")
    print(f"Event canceled: {event2.status}")
    
    # Manually set canceled_at to 11 minutes ago (simulate expired window)
    event2.canceled_at = datetime.now() - timedelta(minutes=11)
    print("Simulating 11 minutes have passed...")
    
    try:
        manager.undo_cancel(event2, teacher)
    except CancellationError as e:
        print(f"✗ Undo failed (as expected): {e}")
    print()
    
    # Scenario 7: Check cancellation history
    print("=" * 80)
    print("Scenario 7: Cancellation History")
    print("=" * 80)
    history = manager.get_cancellation_history(event2.id)
    if history:
        print(f"History for event {event2.id}:")
        print(f"  Previous status: {history['status']}")
        print(f"  Canceled at: {history['timestamp']}")
    else:
        print("No history found (undo was successful for first event)")
    print()
    
    # Final summary
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"\nEvent 1 ({event.id}):")
    print(f"  Current Status: {event.status}")
    print(f"  Action: Canceled and then undone")
    
    print(f"\nEvent 2 ({event2.id}):")
    print(f"  Current Status: {event2.status}")
    print(f"  Action: Canceled (undo window expired)")
    
    print("\n" + "=" * 80)
    print("✓ Event Cancellation Manager Demo Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
