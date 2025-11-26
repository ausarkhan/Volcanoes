"""Event model for Xavier course management system."""
from datetime import datetime
from typing import Optional


class Event:
    """Represents a scheduled event (e.g., review session, class)."""
    
    def __init__(
        self,
        id: str,
        title: str,
        description: str,
        starts_at: datetime,
        ends_at: datetime,
        location: str,
        organizer_id: str,
        organizer_name: str,
        status: str = "SCHEDULED"
    ):
        self.id = id
        self.title = title
        self.description = description
        self.starts_at = starts_at
        self.ends_at = ends_at
        self.location = location
        self.organizer_id = organizer_id
        self.organizer_name = organizer_name
        self.status = status  # SCHEDULED, CANCELED, etc.
        self.cancellation_reason: Optional[str] = None
        self.canceled_at: Optional[datetime] = None
    
    def cancel(self, reason: str, canceled_at: datetime):
        """Mark event as canceled."""
        self.status = "CANCELED"
        self.cancellation_reason = reason
        self.canceled_at = canceled_at
