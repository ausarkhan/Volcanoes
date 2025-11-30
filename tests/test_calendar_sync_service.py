"""Unit tests for CalendarSyncService."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from models.event import Event
from services.calendar_sync_service import CalendarSyncService


def test_generate_ics_canceled_event():
    """Test ICS generation for canceled event includes CANCELLED status."""
    sync_service = CalendarSyncService()
    
    event = Event(
        id="evt_001",
        title="Test Event",
        description="Test Description",
        starts_at=datetime.now() + timedelta(hours=24),
        ends_at=datetime.now() + timedelta(hours=26),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test",
        status="SCHEDULED"
    )
    event.cancel("Test cancellation", datetime.now())
    
    ics_data = sync_service.generate_ics_data(event)
    
    assert 'STATUS:CANCELLED' in ics_data
    assert 'Test Event' in ics_data
    assert 'Test cancellation' in ics_data
    print("✓ Test passed: ICS generation for canceled event")


def test_generate_ics_active_event():
    """Test ICS generation for active event includes CONFIRMED status."""
    sync_service = CalendarSyncService()
    
    event = Event(
        id="evt_002",
        title="Active Event",
        description="Active Description",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=50),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test",
        status="SCHEDULED"
    )
    
    ics_data = sync_service.generate_ics_data(event)
    
    assert 'STATUS:CONFIRMED' in ics_data
    assert 'Active Event' in ics_data
    assert 'STATUS:CANCELLED' not in ics_data
    print("✓ Test passed: ICS generation for active event")


def test_sync_to_all_integrations():
    """Test syncing event to all default integrations."""
    sync_service = CalendarSyncService()
    
    event = Event(
        id="evt_003",
        title="Test Event",
        description="Test Description",
        starts_at=datetime.now() + timedelta(hours=24),
        ends_at=datetime.now() + timedelta(hours=26),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test",
        status="SCHEDULED"
    )
    event.cancel("Test reason", datetime.now())
    
    result = sync_service.sync_event(event)
    
    assert result['ics_generated'] == True
    assert result['integrations_synced'] == 2  # Google + Outlook
    assert result['integrations_failed'] == 0
    assert len(result['sync_results']) == 2
    print("✓ Test passed: Sync to all integrations")


def test_sync_to_specific_integration():
    """Test syncing event to specific integration only."""
    sync_service = CalendarSyncService()
    
    event = Event(
        id="evt_004",
        title="Test Event",
        description="Test Description",
        starts_at=datetime.now() + timedelta(hours=24),
        ends_at=datetime.now() + timedelta(hours=26),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test",
        status="SCHEDULED"
    )
    event.cancel("Test reason", datetime.now())
    
    result = sync_service.sync_event(event, integrations=['google_calendar'])
    
    assert result['ics_generated'] == True
    assert result['integrations_synced'] == 1
    assert result['integrations_failed'] == 0
    assert len(result['sync_results']) == 1
    assert result['sync_results'][0]['integration'] == 'google_calendar'
    print("✓ Test passed: Sync to specific integration")


def test_sync_history_tracking():
    """Test sync history is properly tracked and can be filtered."""
    sync_service = CalendarSyncService()
    
    event1 = Event(
        id="evt_005",
        title="Event 1",
        description="Test",
        starts_at=datetime.now() + timedelta(hours=24),
        ends_at=datetime.now() + timedelta(hours=26),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test",
        status="SCHEDULED"
    )
    event1.cancel("Test reason", datetime.now())
    
    event2 = Event(
        id="evt_006",
        title="Event 2",
        description="Test",
        starts_at=datetime.now() + timedelta(hours=48),
        ends_at=datetime.now() + timedelta(hours=50),
        location="Test Location",
        organizer_id="prof_123",
        organizer_name="Dr. Test",
        status="SCHEDULED"
    )
    event2.cancel("Test reason", datetime.now())
    
    # Sync both events
    sync_service.sync_event(event1)
    sync_service.sync_event(event2)
    
    # Check total history
    all_history = sync_service.get_sync_history()
    assert len(all_history) >= 4  # At least 2 events × 2 integrations
    
    # Check filtered history
    event1_history = sync_service.get_sync_history(event_id="evt_005")
    assert len(event1_history) == 2
    assert all(h.event_id == "evt_005" for h in event1_history)
    
    google_history = sync_service.get_sync_history(integration="google_calendar")
    assert all(h.integration == "google_calendar" for h in google_history)
    
    print("✓ Test passed: Sync history tracking")


if __name__ == "__main__":
    print("Running CalendarSyncService Tests...")
    print("-" * 50)
    test_generate_ics_canceled_event()
    test_generate_ics_active_event()
    test_sync_to_all_integrations()
    test_sync_to_specific_integration()
    test_sync_history_tracking()
    print("-" * 50)
    print("All CalendarSyncService tests passed! ✓")
