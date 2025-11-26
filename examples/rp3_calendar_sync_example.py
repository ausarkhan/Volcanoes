"""
Example usage of CalendarSyncService - Use Case RP3

This demonstrates calendar synchronization for event cancellations.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from services.calendar_sync_service import CalendarSyncService


def example_rp3_calendar_sync():
    """Demonstrate Use Case RP3: Calendar Sync for Cancellations."""
    
    sync_service = CalendarSyncService()
    
    print("=" * 70)
    print("Use Case RP3: Calendar Sync for Cancellations")
    print("=" * 70)
    
    # Scenario 1: Sync canceled event to all integrations
    print("\n--- Scenario 1: Sync canceled event to all integrations ---")
    
    event1 = Event(
        id="evt_201",
        title="Database Systems Lecture",
        description="Advanced query optimization techniques",
        starts_at=datetime.now() + timedelta(hours=24),
        ends_at=datetime.now() + timedelta(hours=26),
        location="STEM Building, Room 401",
        organizer_id="prof_edwards",
        organizer_name="Dr. Sarah Edwards"
    )
    event1.cancel("Instructor illness - will be rescheduled", datetime.now())
    
    # Generate and display ICS data
    ics_data = sync_service.generate_ics_data(event1)
    print(f"\nGenerated ICS data ({len(ics_data)} bytes):")
    print("-" * 70)
    print(ics_data[:500] + "..." if len(ics_data) > 500 else ics_data)
    print("-" * 70)
    
    # Sync to calendars
    result1 = sync_service.sync_event(event1)
    
    print(f"\n✓ Sync Results:")
    print(f"  - Event: {result1['event_title']}")
    print(f"  - Status: {result1['event_status']}")
    print(f"  - ICS Generated: {result1['ics_generated']}")
    print(f"  - ICS Data Size: {result1['ics_data_size']} bytes")
    print(f"  - Successful Syncs: {result1['integrations_synced']}")
    print(f"  - Failed Syncs: {result1['integrations_failed']}")
    print(f"  - Timestamp: {result1['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n  Integration Details:")
    for sync_result in result1['sync_results']:
        status = "✓" if sync_result['success'] else "✗"
        print(f"    {status} {sync_result['integration']}: {sync_result['message']}")
    
    # Scenario 2: Sync to specific integration only
    print("\n--- Scenario 2: Sync to Google Calendar only ---")
    
    event2 = Event(
        id="evt_202",
        title="Software Engineering Workshop",
        description="Agile methodologies and Scrum",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=51),
        location="Conference Room A",
        organizer_id="prof_chen",
        organizer_name="Dr. Michael Chen"
    )
    event2.cancel("Low enrollment - merging with next week's session", datetime.now())
    
    result2 = sync_service.sync_event(event2, integrations=['google_calendar'])
    
    print(f"\n✓ Sync Results:")
    print(f"  - Event: {result2['event_title']}")
    print(f"  - Status: {result2['event_status']}")
    print(f"  - Successful Syncs: {result2['integrations_synced']}")
    print(f"  - Failed Syncs: {result2['integrations_failed']}")
    
    print(f"\n  Integration Details:")
    for sync_result in result2['sync_results']:
        status = "✓" if sync_result['success'] else "✗"
        print(f"    {status} {sync_result['integration']}: {sync_result['message']}")
    
    # Scenario 3: Sync active (non-canceled) event
    print("\n--- Scenario 3: Sync active event (CONFIRMED status) ---")
    
    event3 = Event(
        id="evt_203",
        title="Python Programming Lab",
        description="Hands-on coding exercises",
        starts_at=datetime.now() + timedelta(hours=72),
        ends_at=datetime.now() + timedelta(hours=75),
        location="Computer Lab C",
        organizer_id="prof_martinez",
        organizer_name="Dr. Jennifer Martinez",
        status="SCHEDULED"  # Not canceled
    )
    
    result3 = sync_service.sync_event(event3)
    
    print(f"\n✓ Sync Results:")
    print(f"  - Event: {result3['event_title']}")
    print(f"  - Status: {result3['event_status']} (not canceled)")
    print(f"  - ICS Generated: {result3['ics_generated']}")
    print(f"  - Successful Syncs: {result3['integrations_synced']}")
    
    # Show sync history
    print("\n--- Sync History Summary ---")
    all_syncs = sync_service.get_sync_history()
    print(f"Total sync operations: {len(all_syncs)}")
    
    for i, sync_result in enumerate(all_syncs, 1):
        status = "✓" if sync_result.success else "✗"
        print(
            f"{i}. {status} Event {sync_result.event_id} -> {sync_result.integration} "
            f"at {sync_result.timestamp.strftime('%H:%M:%S')}"
        )
    
    # Filter sync history by event
    print(f"\n--- Sync History for Event: {event1.id} ---")
    event1_syncs = sync_service.get_sync_history(event_id=event1.id)
    for sync_result in event1_syncs:
        status = "✓ Success" if sync_result.success else "✗ Failed"
        print(f"  {sync_result.integration}: {status} - {sync_result.message}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_rp3_calendar_sync()
