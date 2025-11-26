"""
Complete Integration Example - All Use Cases

This demonstrates the full event cancellation workflow combining all three use cases:
RP1: Require Reason for Late Cancellations
RP2: RSVP-Based Cancellation Notifications
RP3: Calendar Sync for Cancellations
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from models.rsvp import RSVP
from services.event_cancellation_service import EventCancellationService, ValidationError
from services.rsvp_service import RSVPService
from services.calendar_sync_service import CalendarSyncService
from utils.notification_utils import NotificationService


def cancel_event_workflow(event: Event, cancellation_reason: str):
    """
    Complete workflow for canceling an event.
    
    This function demonstrates the integration of all three use cases.
    """
    print(f"\n{'=' * 70}")
    print(f"CANCELING EVENT: {event.title}")
    print(f"{'=' * 70}")
    
    # Initialize services
    rsvp_service = RSVPService()
    notification_service = NotificationService()
    cancellation_service = EventCancellationService(rsvp_service, notification_service)
    calendar_service = CalendarSyncService()
    
    # Add some sample RSVPs (in a real system, these would already exist)
    sample_rsvps = [
        RSVP(
            id=f"rsvp_{event.id}_1",
            event_id=event.id,
            student_id="stu_001",
            student_name="Alice Johnson",
            student_email="alice.johnson@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=2)
        ),
        RSVP(
            id=f"rsvp_{event.id}_2",
            event_id=event.id,
            student_id="stu_002",
            student_name="Bob Smith",
            student_email="bob.smith@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(days=1)
        ),
        RSVP(
            id=f"rsvp_{event.id}_3",
            event_id=event.id,
            student_id="stu_003",
            student_name="Carol Williams",
            student_email="carol.williams@xavier.edu",
            status="CONFIRMED",
            created_at=datetime.now() - timedelta(hours=12)
        )
    ]
    
    for rsvp in sample_rsvps:
        rsvp_service.add_rsvp(rsvp)
    
    print(f"\n📋 Event Details:")
    print(f"   ID: {event.id}")
    print(f"   Title: {event.title}")
    print(f"   Start Time: {event.starts_at.strftime('%Y-%m-%d %H:%M')}")
    print(f"   Location: {event.location}")
    print(f"   Organizer: {event.organizer_name}")
    print(f"   RSVPs: {len(sample_rsvps)} students")
    
    try:
        # STEP 1: Validate cancellation reason (Use Case RP1)
        print(f"\n🔍 STEP 1: Validating cancellation reason (Use Case RP1)...")
        validation_result = cancellation_service.validate_cancellation_reason(
            event,
            cancellation_reason
        )
        
        print(f"   ✓ Validation passed!")
        print(f"   - Late cancellation: {validation_result['is_late_cancellation']}")
        print(f"   - Hours until event: {validation_result['hours_until_event']:.1f}")
        print(f"   - Message: {validation_result['message']}")
        
        # Mark event as canceled
        event.cancel(cancellation_reason, datetime.now())
        
        # STEP 2: Notify RSVP'd students (Use Case RP2)
        print(f"\n📧 STEP 2: Notifying RSVP'd students (Use Case RP2)...")
        notification_result = cancellation_service.notify_rsvp_cancellation(event)
        
        print(f"   ✓ Notifications sent!")
        print(f"   - Students notified: {notification_result['notifications_sent']}")
        print(f"   - Urgent flag: {notification_result['urgent']}")
        print(f"   - Notified student IDs: {', '.join(notification_result['notified_students'])}")
        
        # STEP 3: Sync to external calendars (Use Case RP3)
        print(f"\n📅 STEP 3: Syncing to external calendars (Use Case RP3)...")
        sync_result = calendar_service.sync_event(event)
        
        print(f"   ✓ Calendar sync complete!")
        print(f"   - ICS generated: {sync_result['ics_generated']}")
        print(f"   - ICS data size: {sync_result['ics_data_size']} bytes")
        print(f"   - Successful syncs: {sync_result['integrations_synced']}")
        print(f"   - Failed syncs: {sync_result['integrations_failed']}")
        
        for sync_detail in sync_result['sync_results']:
            status = "✓" if sync_detail['success'] else "✗"
            print(f"     {status} {sync_detail['integration']}: {sync_detail['message']}")
        
        # Summary
        print(f"\n{'=' * 70}")
        print(f"✅ EVENT CANCELLATION COMPLETE")
        print(f"{'=' * 70}")
        print(f"Summary:")
        print(f"  - Event '{event.title}' has been successfully canceled")
        print(f"  - {notification_result['notifications_sent']} students were notified")
        print(f"  - {sync_result['integrations_synced']} calendar integrations updated")
        print(f"  - Cancellation reason: {cancellation_reason}")
        print(f"{'=' * 70}\n")
        
        return True
        
    except ValidationError as e:
        print(f"\n❌ CANCELLATION FAILED: {e}")
        print(f"{'=' * 70}\n")
        return False


def main():
    """Run complete integration examples."""
    
    print("\n" + "=" * 70)
    print("XAVIER UNIVERSITY - EVENT CANCELLATION SYSTEM")
    print("Complete Integration Demo: Use Cases RP1, RP2, RP3")
    print("=" * 70)
    
    # Example 1: Urgent cancellation with valid reason
    print("\n\n>>> EXAMPLE 1: Urgent Cancellation (< 24 hours) with Valid Reason <<<")
    event1 = Event(
        id="evt_301",
        title="Advanced Algorithms Review Session",
        description="Final exam preparation",
        starts_at=datetime.now() + timedelta(hours=10),
        ends_at=datetime.now() + timedelta(hours=12),
        location="STEM Building, Room 305",
        organizer_id="prof_edwards",
        organizer_name="Dr. Sarah Edwards"
    )
    
    cancel_event_workflow(
        event1,
        "Professor Edwards has a family emergency and cannot attend"
    )
    
    # Example 2: Non-urgent cancellation
    print("\n\n>>> EXAMPLE 2: Non-Urgent Cancellation (> 24 hours) <<<")
    event2 = Event(
        id="evt_302",
        title="Web Development Workshop",
        description="React and Node.js fundamentals",
        starts_at=datetime.now() + timedelta(hours=72),
        ends_at=datetime.now() + timedelta(hours=75),
        location="Computer Lab A",
        organizer_id="prof_chen",
        organizer_name="Dr. Michael Chen"
    )
    
    cancel_event_workflow(
        event2,
        "Rescheduling to next month due to low enrollment"
    )
    
    # Example 3: Attempted urgent cancellation WITHOUT reason (should fail)
    print("\n\n>>> EXAMPLE 3: Urgent Cancellation WITHOUT Reason (Validation Fails) <<<")
    event3 = Event(
        id="evt_303",
        title="Database Design Lecture",
        description="Normalization and indexing",
        starts_at=datetime.now() + timedelta(hours=8),
        ends_at=datetime.now() + timedelta(hours=10),
        location="STEM Building, Room 201",
        organizer_id="prof_martinez",
        organizer_name="Dr. Jennifer Martinez"
    )
    
    cancel_event_workflow(event3, "")  # Empty reason - should fail validation
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ RP1: Late cancellation validation (24-hour rule)")
    print("  ✓ RP2: RSVP-based notification system")
    print("  ✓ RP3: External calendar synchronization")
    print("  ✓ Complete error handling and validation")
    print("  ✓ Comprehensive logging and audit trails")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
