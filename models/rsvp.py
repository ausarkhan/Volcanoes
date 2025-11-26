"""RSVP model for event attendance tracking."""
from datetime import datetime


class RSVP:
    """Represents a student's RSVP to an event."""
    
    def __init__(
        self,
        id: str,
        event_id: str,
        student_id: str,
        student_name: str,
        student_email: str,
        status: str,
        created_at: datetime
    ):
        self.id = id
        self.event_id = event_id
        self.student_id = student_id
        self.student_name = student_name
        self.student_email = student_email
        self.status = status  # CONFIRMED, CANCELED, etc.
        self.created_at = created_at
