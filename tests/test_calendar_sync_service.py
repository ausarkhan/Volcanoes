"""Unit tests for CalendarSyncService."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from datetime import datetime, timedelta
from models.event import Event
from services.calendar_sync_service import CalendarSyncService


class TestCalendarSyncService(unittest.TestCase):
    """Test cases for CalendarSyncService."""
    
    def test_generate_ics_canceled_event(self):
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
    
    self.assertIn('STATUS:CANCELLED', ics_data)
    self.assertIn('Test Event', ics_data)
    self.assertIn('Test cancellation', ics_data)
    
    def test_generate_ics_active_event(self):
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
    
    self.assertIn('STATUS:CONFIRMED', ics_data)
    self.assertIn('Active Event', ics_data)
    self.assertNotIn('STATUS:CANCELLED', ics_data)
    
    def test_sync_to_all_integrations(self):
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
    
    self.assertTrue(result['ics_generated'])
    self.assertEqual(result['integrations_synced'], 2)  # Google + Outlook
    self.assertEqual(result['integrations_failed'], 0)
    self.assertEqual(len(result['sync_results']), 2)
    
    def test_sync_to_specific_integration(self):
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
    
    self.assertTrue(result['ics_generated'])
    self.assertEqual(result['integrations_synced'], 1)
    self.assertEqual(result['integrations_failed'], 0)
    self.assertEqual(len(result['sync_results']), 1)
    self.assertEqual(result['sync_results'][0]['integration'], 'google_calendar')
    
    def test_sync_history_tracking(self):
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
    self.assertGreaterEqual(len(all_history), 4)  # At least 2 events × 2 integrations
    
    # Check filtered history
    event1_history = sync_service.get_sync_history(event_id="evt_005")
    self.assertEqual(len(event1_history), 2)
    self.assertTrue(all(h.event_id == "evt_005" for h in event1_history))
    
    google_history = sync_service.get_sync_history(integration="google_calendar")
    self.assertTrue(all(h.integration == "google_calendar" for h in google_history))


if __name__ == "__main__":
    unittest.main()
