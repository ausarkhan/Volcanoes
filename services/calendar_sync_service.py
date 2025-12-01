"""Calendar Sync Service for external calendar integrations."""
from datetime import datetime
from typing import Dict, Any, List
from icalendar import Calendar, Event as ICSEvent
from events import Events
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SyncResult:
    """Represents a calendar sync operation result."""
    
    def __init__(
        self,
        event_id: str,
        integration: str,
        success: bool,
        timestamp: datetime,
        message: str = ""
    ):
        self.event_id = event_id
        self.integration = integration
        self.success = success
        self.timestamp = timestamp
        self.message = message


class CalendarSyncService:
    """Service for syncing events to external calendar systems."""
    
    def __init__(self):
        self._sync_results: List[SyncResult] = []
    
    def generate_ics_data(self, event: Events) -> str:
        """
        Generate ICS (iCalendar) data for an event.
        
        Args:
            event: The event to generate ICS data for
            
        Returns:
            String containing the ICS data
        """
        cal = Calendar()
        cal.add('prodid', '-//Xavier University Event System//EN')
        cal.add('version', '2.0')
        
        ics_event = ICSEvent()
        ics_event.add('uid', f'{event.id}@xavier.edu')
        ics_event.add('summary', event.title)
        ics_event.add('description', event.description)
        ics_event.add('dtstart', event.starts_at)
        ics_event.add('dtend', event.ends_at)
        ics_event.add('location', event.location)
        ics_event.add('organizer', f'mailto:{event.organizer_id}@xavier.edu')
        
        # Set status to CANCELED if event is canceled
        if event.status == "CANCELED":
            ics_event.add('status', 'CANCELLED')  # Note: iCalendar uses CANCELLED
            if event.cancellation_reason:
                # Add cancellation reason to description
                full_description = f"{event.description}\n\nCANCELED: {event.cancellation_reason}"
                ics_event['description'] = full_description
        else:
            ics_event.add('status', 'CONFIRMED')
        
        cal.add_component(ics_event)
        
        return cal.to_ical().decode('utf-8')
    
    def sync_to_google_calendar(self, event: Events, ics_data: str) -> bool:
        """
        Sync event to Google Calendar.
        
        In a real implementation, this would use the Google Calendar API.
        For now, this is a simulation.
        
        Args:
            event: The event to sync
            ics_data: The ICS data to send
            
        Returns:
            bool indicating success
        """
        # Simulate Google Calendar API call
        logger.info(
            f"Syncing to Google Calendar: {event.title} (ID: {event.id})\n"
            f"  Status: {event.status}\n"
            f"  ICS Data Length: {len(ics_data)} bytes"
        )
        
        # In a real implementation, would make API call here
        # For simulation, assume success
        return True
    
    def sync_to_outlook(self, event: Events, ics_data: str) -> bool:
        """
        Sync event to Outlook/Office 365.
        
        In a real implementation, this would use the Microsoft Graph API.
        For now, this is a simulation.
        
        Args:
            event: The event to sync
            ics_data: The ICS data to send
            
        Returns:
            bool indicating success
        """
        # Simulate Outlook API call
        logger.info(
            f"Syncing to Outlook: {event.title} (ID: {event.id})\n"
            f"  Status: {event.status}\n"
            f"  ICS Data Length: {len(ics_data)} bytes"
        )
        
        # In a real implementation, would make API call here
        # For simulation, assume success
        return True
    
    def sync_event(
        self,
        event: Events,
        integrations: List[str] = None
    ) -> Dict[str, Any]:
        """
        Sync event to external calendar integrations.
        
        Use Case RP3: Calendar Sync for Cancellations
        - Generates updated ICS data with STATUS: CANCELED
        - Sends updated ICS to external calendar integrations (e.g., Google Calendar)
        - Records sync results (success, failure, timestamps)
        
        Args:
            event: The event to sync
            integrations: List of calendar integrations to sync to
                         (default: ['google_calendar', 'outlook'])
            
        Returns:
            Dict containing:
                - event_id: str the event ID
                - event_title: str the event title
                - event_status: str the event status
                - ics_generated: bool whether ICS was successfully generated
                - ics_data_size: int size of ICS data in bytes
                - integrations_synced: int number of successful syncs
                - integrations_failed: int number of failed syncs
                - sync_results: List of sync result details
                - timestamp: datetime when sync was performed
        """
        now = datetime.now()
        
        # Default integrations if none specified
        if integrations is None:
            integrations = ['google_calendar', 'outlook']
        
        # Generate ICS data
        try:
            ics_data = self.generate_ics_data(event)
            ics_generated = True
            ics_size = len(ics_data)
        except Exception as e:
            logger.error(f"Failed to generate ICS data: {e}")
            return {
                'event_id': event.id,
                'event_title': event.title,
                'event_status': event.status,
                'ics_generated': False,
                'error': str(e),
                'timestamp': now
            }
        
        # Sync to each integration
        sync_results = []
        successes = 0
        failures = 0
        
        for integration in integrations:
            try:
                if integration == 'google_calendar':
                    success = self.sync_to_google_calendar(event, ics_data)
                elif integration == 'outlook':
                    success = self.sync_to_outlook(event, ics_data)
                else:
                    logger.warning(f"Unknown integration: {integration}")
                    success = False
                
                message = "Successfully synced" if success else "Sync failed"
                
                result = SyncResult(
                    event_id=event.id,
                    integration=integration,
                    success=success,
                    timestamp=now,
                    message=message
                )
                
                self._sync_results.append(result)
                sync_results.append({
                    'integration': integration,
                    'success': success,
                    'message': message
                })
                
                if success:
                    successes += 1
                else:
                    failures += 1
                    
            except Exception as e:
                logger.error(f"Failed to sync to {integration}: {e}")
                result = SyncResult(
                    event_id=event.id,
                    integration=integration,
                    success=False,
                    timestamp=now,
                    message=str(e)
                )
                self._sync_results.append(result)
                sync_results.append({
                    'integration': integration,
                    'success': False,
                    'message': str(e)
                })
                failures += 1
        
        return {
            'event_id': event.id,
            'event_title': event.title,
            'event_status': event.status,
            'ics_generated': ics_generated,
            'ics_data_size': ics_size,
            'integrations_synced': successes,
            'integrations_failed': failures,
            'sync_results': sync_results,
            'timestamp': now
        }
    
    def get_sync_history(
        self,
        event_id: str = None,
        integration: str = None
    ) -> List[SyncResult]:
        """Retrieve sync history, optionally filtered."""
        results = self._sync_results
        
        if event_id:
            results = [r for r in results if r.event_id == event_id]
        
        if integration:
            results = [r for r in results if r.integration == integration]
        
        return results
