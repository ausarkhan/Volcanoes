"""
Xavier University Event Management System - Main Driver

This driver demonstrates all implemented features:
- P1: Course Event Creation (Professor)
- RP1: Event Cancellation with Validation
- RP2: RSVP-Based Notifications
- RP3: Calendar Synchronization
- Feed Service: Event feed management
- Notification Service: Follower notifications
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta

from events import Events as Event
from models.rsvp import RSVP
from models.feed_service import FeedService
from models.notification_service import NotificationService
from services.course_event_service import CourseEventService
from services.event_cancellation_service import EventCancellationService, ValidationError
from services.rsvp_service import RSVPService
from services.calendar_sync_service import CalendarSyncService
from utils.notification_utils import NotificationService as NotificationUtils


def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"{title:^80}")
    print("=" * 80)


def print_subheader(title):
    """Print a formatted subsection header."""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")


def demo_p1_course_events():
    """Demonstrate P1: Course Event (Professor creates exam review session)."""
    print_header("USE CASE P1: COURSE EVENT (PROFESSOR)")
    
    course_event_service = CourseEventService()
    
    professor_id = "prof_edwards"
    professor_name = "Dr. Sarah Edwards"
    
    print(f"\n👤 Professor: {professor_name} ({professor_id})")
    
    # Show professor's courses
    print(f"\n📚 Professor's Course Sections:")
    sections = course_event_service.get_sections_for_user(professor_id)
    for section in sections:
        print(f"   - {section['course_code']}: {section['name']}")
    
    # Create exam review session
    print(f"\n📝 Creating CS101 Final Exam Review Session...")
    
    try:
        event = course_event_service.create_course_event(
            professor_id=professor_id,
            professor_name=professor_name,
            course_code="CS101",
            title="CS101 Final Exam Review Session",
            description="Comprehensive review for the final exam",
            starts_at=datetime.now() + timedelta(days=3, hours=2),
            ends_at=datetime.now() + timedelta(days=3, hours=4),
            location="STEM Building, Room 201"
        )
        
        print(f"\n✅ Event Created Successfully!")
        print(f"   Event ID: {event.id}")
        print(f"   Title: {event.title}")
        print(f"   Start: {event.starts_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Location: {event.location}")
        
        return event
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        return None


def demo_feed_service(event):
    """Demonstrate Feed Service functionality."""
    print_header("FEED SERVICE: EVENT FEED MANAGEMENT")
    
    feed_service = FeedService()
    
    print("\n📋 Adding event to feed...")
    feed_service.add_event(event)
    print(f"✅ Feed now contains {len(feed_service.feed)} event(s)")
    
    # Show feed contents
    print("\n📰 Current Feed:")
    for evt in feed_service.feed:
        print(f"   - {evt.title} ({evt.status})")
    
    # Simulate cancellation and removal
    print("\n🚫 Canceling event...")
    event.cancel("Instructor illness", datetime.now())
    
    print("📋 Removing canceled event from feed...")
    feed_service.remove_event(event)
    print(f"✅ Feed now contains {len(feed_service.feed)} event(s)")
    
    return feed_service


def demo_notification_service(event):
    """Demonstrate Notification Service functionality."""
    print_header("NOTIFICATION SERVICE: FOLLOWER NOTIFICATIONS")
    
    notification_service = NotificationService()
    
    print(f"\n📢 Notifying followers about: {event.title}")
    notification_service.notify_followers(event)
    print("✅ Notification sent to all followers")
    
    return notification_service


def demo_rp1_validation():
    """Demonstrate RP1: Event Cancellation Validation."""
    print_header("USE CASE RP1: REQUIRE REASON FOR LATE CANCELLATIONS")
    
    cancellation_service = EventCancellationService()
    
    # Scenario 1: Late cancellation WITH reason
    print_subheader("Scenario 1: Late cancellation (12 hours) WITH reason")
    
    event1 = Event(
        id="evt_rp1_001",
        title="Database Design Review",
        description="Review session",
        starts_at=datetime.now() + timedelta(hours=12),
        ends_at=datetime.now() + timedelta(hours=14),
        location="STEM 201",
        organizer_id="prof_123",
        organizer_name="Dr. Sarah Edwards"
    )
    
    try:
        result = cancellation_service.validate_cancellation_reason(
            event1,
            "Unexpected family emergency"
        )
        print(f"✅ Validation passed: {result['message']}")
        print(f"   Late cancellation: {result['is_late_cancellation']}")
        print(f"   Hours until event: {result['hours_until_event']:.1f}")
    except ValidationError as e:
        print(f"❌ Validation failed: {e}")
    
    # Scenario 2: Late cancellation WITHOUT reason
    print_subheader("Scenario 2: Late cancellation (8 hours) WITHOUT reason")
    
    event2 = Event(
        id="evt_rp1_002",
        title="Algorithm Study Session",
        description="Practice problems",
        starts_at=datetime.now() + timedelta(hours=8),
        ends_at=datetime.now() + timedelta(hours=10),
        location="Library",
        organizer_id="prof_456",
        organizer_name="Dr. Michael Chen"
    )
    
    try:
        result = cancellation_service.validate_cancellation_reason(event2, "")
        print(f"✅ Validation passed: {result['message']}")
    except ValidationError as e:
        print(f"❌ Validation failed: {e}")


def demo_rp2_notifications():
    """Demonstrate RP2: RSVP-Based Cancellation Notifications."""
    print_header("USE CASE RP2: RSVP-BASED CANCELLATION NOTIFICATIONS")
    
    rsvp_service = RSVPService()
    notification_utils = NotificationUtils()
    cancellation_service = EventCancellationService(rsvp_service, notification_utils)
    
    print_subheader("Creating event with RSVPs")
    
    event = Event(
        id="evt_rp2_001",
        title="Machine Learning Workshop",
        description="Introduction to neural networks",
        starts_at=datetime.now() + timedelta(hours=10),
        ends_at=datetime.now() + timedelta(hours=12),
        location="Computer Lab B",
        organizer_id="prof_123",
        organizer_name="Dr. Sarah Edwards"
    )
    
    # Add RSVPs
    rsvps = [
        RSVP(
            id="rsvp_001",
            event_id=event.id,
            student_id="stu_001",
            student_name="Alice Johnson",
            student_email="alice.johnson@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=2)
        ),
        RSVP(
            id="rsvp_002",
            event_id=event.id,
            student_id="stu_002",
            student_name="Bob Smith",
            student_email="bob.smith@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=1)
        ),
        RSVP(
            id="rsvp_003",
            event_id=event.id,
            student_id="stu_003",
            student_name="Carol Williams",
            student_email="carol.williams@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(hours=12)
        )
    ]
    
    for rsvp in rsvps:
        rsvp_service.add_rsvp(rsvp)
    
    print(f"✅ Added {len(rsvps)} RSVPs to the event")
    
    # Cancel event and notify
    print("\n🚫 Canceling event and notifying RSVPs...")
    event.cancel("Presenter has fallen ill", datetime.now())
    
    result = cancellation_service.notify_rsvp_cancellation(event)
    
    print(f"\n✅ Notification Results:")
    print(f"   Event: {result['event_title']}")
    print(f"   RSVP Count: {result['rsvp_count']}")
    print(f"   Notifications Sent: {result['notifications_sent']}")
    print(f"   Urgent: {result['urgent']}")
    print(f"   Hours until event: {result['hours_until_event']:.1f}")
    print(f"   Notified: {', '.join(result['notified_students'])}")


def demo_rp3_calendar_sync():
    """Demonstrate RP3: Calendar Synchronization."""
    print_header("USE CASE RP3: CALENDAR SYNC FOR CANCELLATIONS")
    
    sync_service = CalendarSyncService()
    
    print_subheader("Creating and syncing canceled event")
    
    event = Event(
        id="evt_rp3_001",
        title="Database Systems Lecture",
        description="Advanced query optimization",
        starts_at=datetime.now() + timedelta(hours=24),
        ends_at=datetime.now() + timedelta(hours=26),
        location="STEM 401",
        organizer_id="prof_edwards",
        organizer_name="Dr. Sarah Edwards"
    )
    event.cancel("Instructor illness - will be rescheduled", datetime.now())
    
    print(f"🚫 Event canceled: {event.title}")
    
    # Generate ICS
    print("\n📅 Generating ICS calendar data...")
    ics_data = sync_service.generate_ics_data(event)
    print(f"✅ Generated {len(ics_data)} bytes of ICS data")
    
    # Sync to calendars
    print("\n🔄 Syncing to calendar integrations...")
    result = sync_service.sync_event(event)
    
    print(f"\n✅ Sync Results:")
    print(f"   Event: {result['event_title']}")
    print(f"   Status: {result['event_status']}")
    print(f"   ICS Generated: {result['ics_generated']}")
    print(f"   Successful Syncs: {result['integrations_synced']}")
    print(f"   Failed Syncs: {result['integrations_failed']}")
    
    print(f"\n   Integration Details:")
    for sync_result in result['sync_results']:
        status = "✅" if sync_result['success'] else "❌"
        print(f"    {status} {sync_result['integration']}: {sync_result['message']}")


def demo_integrated_workflow():
    """Demonstrate complete integrated workflow."""
    print_header("INTEGRATED WORKFLOW: COMPLETE EVENT LIFECYCLE")
    
    # Initialize all services
    feed_service = FeedService()
    notification_service = NotificationService()
    course_event_service = CourseEventService()
    rsvp_service = RSVPService()
    cancellation_service = EventCancellationService(rsvp_service)
    sync_service = CalendarSyncService()
    
    print_subheader("Step 1: Professor creates event")
    
    event = course_event_service.create_course_event(
        professor_id="prof_edwards",
        professor_name="Dr. Sarah Edwards",
        course_code="CS201",
        title="CS201 Midterm Review - Data Structures",
        description="Review of trees, graphs, and algorithms",
        starts_at=datetime.now() + timedelta(days=2),
        ends_at=datetime.now() + timedelta(days=2, hours=2),
        location="STEM 305"
    )
    
    print(f"✅ Event created: {event.title}")
    
    print_subheader("Step 2: Add event to feed")
    feed_service.add_event(event)
    print(f"✅ Event added to feed ({len(feed_service.feed)} events)")
    
    print_subheader("Step 3: Students RSVP")
    rsvp = RSVP(
        id="integrated_rsvp_001",
        event_id=event.id,
        student_id="stu_999",
        student_name="David Lee",
        student_email="david.lee@xavier.edu",
        status="CONFIRMED",
        created_at=datetime.now()
    )
    rsvp_service.add_rsvp(rsvp)
    print(f"✅ Student RSVP registered: {rsvp.student_name}")
    
    print_subheader("Step 4: Cancel event (integrated workflow)")
    
    # Validate cancellation
    try:
        validation = cancellation_service.validate_cancellation_reason(
            event,
            "Unexpected scheduling conflict"
        )
        print(f"✅ Cancellation validated: {validation['message']}")
    except ValidationError as e:
        print(f"❌ Validation failed: {e}")
        return
    
    # Cancel event
    event.cancel("Unexpected scheduling conflict", datetime.now())
    print(f"✅ Event status: {event.status}")
    
    # Remove from feed
    feed_service.remove_event(event)
    print(f"✅ Removed from feed ({len(feed_service.feed)} events)")
    
    # Notify followers
    notification_service.notify_followers(event)
    print(f"✅ Followers notified")
    
    # Notify RSVPs
    notification_result = cancellation_service.notify_rsvp_cancellation(event)
    print(f"✅ {notification_result['notifications_sent']} RSVP notifications sent")
    
    # Sync to calendars
    sync_result = sync_service.sync_event(event)
    print(f"✅ Synced to {sync_result['integrations_synced']} calendar(s)")
    
    print(f"\n🎉 Complete workflow executed successfully!")

def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "XAVIER UNIVERSITY EVENT MANAGEMENT SYSTEM".center(78) + "║")
    print("║" + "Comprehensive Feature Demonstration".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    
    # Run all demos
    event = demo_p1_course_events()
    
    if event:
        # Reset event status for feed demo
        event.status = "SCHEDULED"
        demo_feed_service(event)
        
        # Reset for notification demo
        event.status = "SCHEDULED"
        demo_notification_service(event)
    
    demo_rp1_validation()
    demo_rp2_notifications()
    demo_rp3_calendar_sync()
    demo_integrated_workflow()
    
    # Final summary
    print_header("DEMONSTRATION COMPLETE")
    print("\n✅ All use cases demonstrated successfully!")
    print("\nImplemented Features:")
    print("  ✓ P1: Course Event Creation (Professor)")
    print("  ✓ RP1: Event Cancellation Validation")
    print("  ✓ RP2: RSVP-Based Notifications")
    print("  ✓ RP3: Calendar Synchronization")
    print("  ✓ Feed Service: Event feed management")
    print("  ✓ Notification Service: Follower notifications")
    print("  ✓ Integrated Workflow: Complete lifecycle")
    
    print("\n" + "=" * 80)
    print("\nTo run individual examples:")
    print("  - python examples/p1_course_event_example.py")
    print("  - python examples/rp1_validation_example.py")
    print("  - python examples/rp2_notification_example.py")
    print("  - python examples/rp3_calendar_sync_example.py")
    print("\nTo run tests:")
    print("  - python -m unittest discover tests/")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
