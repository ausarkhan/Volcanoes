"""
Example usage of EventCancellationService - Use Case RP2

This demonstrates RSVP-based cancellation notifications.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from models.rsvp import RSVP
from services.event_cancellation_service import EventCancellationService
from services.rsvp_service import RSVPService
from utils.notification_utils import NotificationService


def example_rp2_notifications():
    """Demonstrate Use Case RP2: RSVP-Based Cancellation Notifications."""
    
    # Set up services
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    cancellation_service = EventCancellationService(rsvp_service, notification_service)
    
    print("=" * 70)
    print("Use Case RP2: RSVP-Based Cancellation Notifications")
    print("=" * 70)
    
    # Scenario 1: Urgent cancellation with multiple RSVPs
    print("\n--- Scenario 1: Urgent cancellation (10 hours) with 3 RSVPs ---")
    
    event1 = Event(
        id="evt_101",
        title="Machine Learning Workshop",
        description="Introduction to neural networks",
        starts_at=datetime.now() + timedelta(hours=10),
        ends_at=datetime.now() + timedelta(hours=12),
        location="Computer Lab B",
        organizer_id="prof_123",
        organizer_name="Dr. Sarah Edwards"
    )
    event1.cancel("Presenter has fallen ill", datetime.now())
    
    # Add RSVPs for this event
    rsvps_event1 = [
        RSVP(
            id="rsvp_001",
            event_id="evt_101",
            student_id="stu_001",
            student_name="Alice Johnson",
            student_email="alice.johnson@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=2)
        ),
        RSVP(
            id="rsvp_002",
            event_id="evt_101",
            student_id="stu_002",
            student_name="Bob Smith",
            student_email="bob.smith@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=1)
        ),
        RSVP(
            id="rsvp_003",
            event_id="evt_101",
            student_id="stu_003",
            student_name="Carol Williams",
            student_email="carol.williams@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(hours=12)
        )
    ]
    
    for rsvp in rsvps_event1:
        rsvp_service.add_rsvp(rsvp)
    
    # Send notifications
    result1 = cancellation_service.notify_rsvp_cancellation(event1)
    
    print(f"\n✓ Notification Results:")
    print(f"  - Event: {result1['event_title']}")
    print(f"  - RSVP Count: {result1['rsvp_count']}")
    print(f"  - Notifications Sent: {result1['notifications_sent']}")
    print(f"  - Urgent: {result1['urgent']}")
    print(f"  - Hours until event: {result1['hours_until_event']:.1f}")
    print(f"  - Notified Students: {', '.join(result1['notified_students'])}")
    print(f"  - Timestamp: {result1['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Scenario 2: Non-urgent cancellation with RSVPs
    print("\n--- Scenario 2: Non-urgent cancellation (48 hours) with 2 RSVPs ---")
    
    event2 = Event(
        id="evt_102",
        title="Python Study Group",
        description="Practice coding problems",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=50),
        location="Library Room 301",
        organizer_id="prof_456",
        organizer_name="Dr. Michael Chen"
    )
    event2.cancel("Venue double-booked, rescheduling next week", datetime.now())
    
    # Add RSVPs for this event
    rsvps_event2 = [
        RSVP(
            id="rsvp_004",
            event_id="evt_102",
            student_id="stu_004",
            student_name="David Brown",
            student_email="david.brown@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=3)
        ),
        RSVP(
            id="rsvp_005",
            event_id="evt_102",
            student_id="stu_005",
            student_name="Emma Davis",
            student_email="emma.davis@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=1)
        )
    ]
    
    for rsvp in rsvps_event2:
        rsvp_service.add_rsvp(rsvp)
    
    # Send notifications
    result2 = cancellation_service.notify_rsvp_cancellation(event2)
    
    print(f"\n✓ Notification Results:")
    print(f"  - Event: {result2['event_title']}")
    print(f"  - RSVP Count: {result2['rsvp_count']}")
    print(f"  - Notifications Sent: {result2['notifications_sent']}")
    print(f"  - Urgent: {result2['urgent']}")
    print(f"  - Hours until event: {result2['hours_until_event']:.1f}")
    print(f"  - Notified Students: {', '.join(result2['notified_students'])}")
    print(f"  - Timestamp: {result2['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Scenario 3: Event with no RSVPs
    print("\n--- Scenario 3: Cancellation with no RSVPs ---")
    
    event3 = Event(
        id="evt_103",
        title="Optional Office Hours",
        description="Drop-in Q&A session",
        starts_at=datetime.now() + timedelta(hours=6),
        ends_at=datetime.now() + timedelta(hours=7),
        location="Office 205",
        organizer_id="prof_789",
        organizer_name="Dr. Jennifer Martinez"
    )
    event3.cancel("Professor called away for emergency", datetime.now())
    
    # No RSVPs added for this event
    
    # Send notifications
    result3 = cancellation_service.notify_rsvp_cancellation(event3)
    
    print(f"\n✓ Notification Results:")
    print(f"  - Event: {result3['event_title']}")
    print(f"  - RSVP Count: {result3['rsvp_count']}")
    print(f"  - Notifications Sent: {result3['notifications_sent']}")
    print(f"  - Urgent: {result3['urgent']}")
    print(f"  - Hours until event: {result3['hours_until_event']:.1f}")
    print(f"  - Message: No students to notify (no RSVPs)")
    
    # Show notification logs
    print("\n--- Notification Logs Summary ---")
    all_logs = notification_service.get_notification_logs()
    print(f"Total notifications logged: {len(all_logs)}")
    
    for i, log in enumerate(all_logs, 1):
        urgency = "[URGENT] " if log.urgent else ""
        print(f"{i}. {urgency}{log.student_name} notified about '{log.event_title}' at {log.sent_at.strftime('%H:%M:%S')}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_rp2_notifications()
