"""Feed service for managing event feeds."""
from typing import List
from models.event import Event


class FeedService:
    """Service for managing the event feed shown to users."""
    
    def __init__(self):
        self.feed: List[Event] = []
    
    def add_event(self, event: Event) -> None:
        """
        Adds the event to the feed (unless canceled).
        
        Args:
            event: The event to add to the feed
        """
        if event.status != "CANCELED":
            self.feed.append(event)
    
    def remove_event(self, event: Event) -> None:
        """
        Removes an event from the feed (when canceled).
        
        Args:
            event: The event to remove from the feed
        """
        if event in self.feed:
            self.feed.remove(event)
