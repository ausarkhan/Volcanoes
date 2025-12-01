"""Override Request model for Xavier course management system."""
from datetime import datetime
from typing import Optional, Dict, Any


class OverrideRequest:
    """
    Represents an override request for event conflicts.
    
    When an event has a conflict, an OverrideRequest is created
    with proposed event data and can be approved or denied.
    """
    
    def __init__(
        self,
        id: str,
        event_draft: Dict[str, Any],
        conflict_reason: str,
        created_at: datetime,
        updated_at: datetime,
        status: str = "pending"
    ):
        """
        Initialize an OverrideRequest.
        
        Args:
            id: Unique identifier for the override request
            event_draft: Proposed event data (Dict with event details)
            conflict_reason: Description of the conflict
            created_at: Timestamp when request was created
            updated_at: Timestamp when request was last updated
            status: Request status ("pending", "approved", "denied")
        """
        self.id = id
        self.event_draft = event_draft
        self.conflict_reason = conflict_reason
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status
        self.deny_reason: Optional[str] = None
    
    def approve(self) -> None:
        """Approve the override request."""
        self.status = "approved"
        self.updated_at = datetime.now()
    
    def deny(self, reason: str) -> None:
        """
        Deny the override request.
        
        Args:
            reason: Explanation for denial
        """
        self.status = "denied"
        self.deny_reason = reason
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert override request to dictionary.
        
        Returns:
            Dictionary representation of the override request
        """
        return {
            "id": self.id,
            "event_draft": self.event_draft,
            "conflict_reason": self.conflict_reason,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deny_reason": self.deny_reason
        }
