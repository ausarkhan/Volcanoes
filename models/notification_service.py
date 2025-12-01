"""Notification service for event notifications."""
from models.event import Event


class NotificationService:
    """Service for sending notifications to event followers."""
    
    def notify_followers(self, event: Event) -> None:
        """
        Notifies followers about an event.
        
        This method should be called when event notifications are enabled.
        
        Args:
            event: The event to notify followers about
        """
        # Implementation would send notifications to followers
        # For now, this is a placeholder that can be extended
        print(f"Notifying followers about event: {event.title}")
