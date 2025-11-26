"""
Event Cancellation Manager Example
Demonstrates event cancellation and undo functionality.
"""
from datetime import datetime, timedelta
from services.event_cancellation_manager import EventCancellationManager, CancellationError
from models.event import Event
from models.user import User


def main():
    print("=" * 70)
    print("Event Cancellation Manager Demo")
    print("=" * 70)
    
    # Initialize the manager
    manager = EventCancellationManager()
    
    # Create users
    teacher = User(
        name="Dr. Sarah Williams",
        email="swilliams@xavier.edu",
        user_id="prof001",
        role="teacher"
    )
    
    student_organizer = User(
        name="Marcus Johnson",
        email="mjohnson@xavier.edu",
        user_id="stu001",
        role="student"
    )
    
    unauthorized_student = User(
        name="Emily Chen",
        email="echen@xavier.edu",
        user_id="stu002",
        role="student"
    )
    
    # Create an event
    event = Event(
        id="evt123",
        title="Advanced Python Workshop",
        description="Deep dive into Python async programming",
        starts_at=datetime.now() + timedelta(days=3),
        ends_at=datetime.now() + timedelta(days=3, hours=2),
        location="Computer Lab 204",
        organizer_id="stu001",
        organizer_name="Marcus Johnson",
        status="SCHEDULED"
    )
    
    print(f"\nEvent Created:")
    print(f"  ID: {event.id}")
    print(f"  Title: {event.title}")
    print(f"  Status: {event.status}")
    print(f"  Organizer: {event.organizer_name}")
    print(f"  Starts: {event.starts_at.strftime('%Y-%m-%d %H:%M')}")
    
    # Example 1: Successful cancellation by organizer
    print("\n" + "-" * 70)
    print("Example 1: Organizer cancels event")
    print("-" * 70)
    
    try:
        result = manager.cancel_event(
            event,
            student_organizer,
            reason="Lab equipment maintenance scheduled"
        )
        print(f"✓ Cancellation successful!")
        print(f"  Event Status: {result['status']}")
        print(f"  Canceled By: {result['canceled_by']}")
        print(f"  Reason: {result['reason']}")
        print(f"  Can Undo Until: {result['can_undo_until'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Notifications Sent: {result['notifications_sent']}")
    except CancellationError as e:
        print(f"✗ Cancellation failed: {e}")
    
    # Example 2: Check if can undo
    print("\n" + "-" * 70)
    print("Example 2: Check if cancellation can be undone")
    print("-" * 70)
    
    can_undo = manager.can_undo(event)
    print(f"Can undo cancellation: {can_undo}")
    
    # Example 3: Successful undo
    print("\n" + "-" * 70)
    print("Example 3: Undo the cancellation")
    print("-" * 70)
    
    try:
        result = manager.undo_cancel(event, student_organizer)
        print(f"✓ Undo successful!")
        print(f"  Event Status: {result['status']}")
        print(f"  Undone By: {result['undone_by']}")
        print(f"  Restored to Feed: {result['restored_to_feed']}")
    except CancellationError as e:
        print(f"✗ Undo failed: {e}")
    
    print(f"\nCurrent Event Status: {event.status}")
    
    # Example 4: Re-cancel and try unauthorized undo
    print("\n" + "-" * 70)
    print("Example 4: Teacher cancels, unauthorized student tries to undo")
    print("-" * 70)
    
    try:
        # Teacher cancels
        manager.cancel_event(event, teacher, reason="Department policy change")
        print(f"✓ Teacher canceled event")
        print(f"  Event Status: {event.status}")
        
        # Unauthorized student tries to undo
        print(f"\n  Unauthorized student attempts undo...")
        manager.undo_cancel(event, unauthorized_student)
        print(f"✗ This should not appear!")
    except CancellationError as e:
        print(f"✓ Undo correctly blocked: {e}")
    
    # Example 5: Permission denied for cancellation
    print("\n" + "-" * 70)
    print("Example 5: Unauthorized student tries to cancel")
    print("-" * 70)
    
    # First restore event for this test
    event.status = "SCHEDULED"
    
    try:
        manager.cancel_event(
            event,
            unauthorized_student,
            reason="I want to cancel it"
        )
        print(f"✗ This should not appear!")
    except CancellationError as e:
        print(f"✓ Cancellation correctly blocked: {e}")
        print(f"  Event Status: {event.status}")
    
    # Example 6: Teacher can cancel any event
    print("\n" + "-" * 70)
    print("Example 6: Teacher cancels event they didn't organize")
    print("-" * 70)
    
    try:
        result = manager.cancel_event(
            event,
            teacher,
            reason="Building closure for renovations"
        )
        print(f"✓ Teacher successfully canceled event")
        print(f"  Event Status: {result['status']}")
        print(f"  Canceled By: {result['canceled_by']}")
        print(f"  Reason: {result['reason']}")
    except CancellationError as e:
        print(f"✗ Cancellation failed: {e}")
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
