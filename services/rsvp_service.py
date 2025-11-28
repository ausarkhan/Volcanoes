"""RSVP Service for managing event RSVPs."""
from typing import List
from datetime import datetime
from models.rsvp import RSVP


class RSVPService:
    """Service for managing RSVPs to events."""
    
    def __init__(self):
        # In a real application, this would query a database
        # For now, we'll use an in-memory store
        self._rsvps: List[RSVP] = []
    
    def add_rsvp(self, rsvp: RSVP) -> None:
        """Add an RSVP to the system."""
        self._rsvps.append(rsvp)
    
    def get_event_rsvps(self, event_id: str) -> List[RSVP]:
        """
        Retrieve all RSVPs for a specific event.
        
        Args:
            event_id: The ID of the event
            
        Returns:
            List of RSVP objects for the event (only CONFIRMED status)
        """
        return [
            rsvp for rsvp in self._rsvps 
            if rsvp.event_id == event_id and rsvp.status == "CONFIRMED"
        ]
    
    def get_rsvp_count(self, event_id: str) -> int:
        """Get count of confirmed RSVPs for an event."""
        return len(self.get_event_rsvps(event_id))
