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
