"""
Event Cancellation Manager for Xavier University Event System.
Manages event cancellation with undo functionality.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class CancellationError(Exception):
    """Raised when cancellation operations fail."""
    pass


class EventCancellationManager:
    """
    Manages event cancellation and undo operations.
    
    Requirements (Ausar's requirement):
    - cancel_event(event, user, reason=None): Cancel an event with permission checks
    - undo_cancel(event, user): Undo cancellation within time window
    - Permission checking: Only organizer or teacher can cancel
    - Notifications: Trigger notifications on cancellation
    - Feed management: Remove from feed/search on cancel, restore on undo
    - 10-minute undo window
    """
    
    def __init__(self):
        """Initialize the Event Cancellation Manager."""
        self.cancellation_history = {}  # event_id -> cancellation details
        self.undo_window_minutes = 10
    
    def cancel_event(self, event, user, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel an event with permission checks.
        
        Args:
            event: Event object to cancel
            user: User requesting cancellation
            reason: Optional cancellation reason
            
        Returns:
            Dict with cancellation details
            
        Raises:
            CancellationError: If user lacks permission or event already canceled
        """
        # Check permissions
        if not self._check_permission(event, user):
            raise CancellationError(
                f"User {user.user_id} does not have permission to cancel this event. "
                f"Only the organizer or a teacher can cancel events."
            )
        
        # Check if already canceled
        if hasattr(event, 'status') and event.status == 'CANCELED':
            raise CancellationError(f"Event {event.id} is already canceled")
        
        # Store cancellation details for undo
        cancellation_time = datetime.now()
        self.cancellation_history[event.id] = {
            'event': event,
            'user_id': user.user_id,
            'reason': reason,
            'canceled_at': cancellation_time,
            'original_status': getattr(event, 'status', 'SCHEDULED'),
            'can_undo_until': cancellation_time + timedelta(minutes=self.undo_window_minutes)
        }
        
        # Cancel the event
        event.status = 'CANCELED'
        event.cancellation_reason = reason
        event.canceled_at = cancellation_time
        
        # Trigger notifications (simulated)
        self._trigger_notifications(event, user, reason)
        
        # Remove from feed/search (simulated)
        self._remove_from_feed(event)
        
        return {
            'event_id': event.id,
            'status': 'CANCELED',
            'canceled_by': user.user_id,
            'canceled_at': cancellation_time,
            'reason': reason,
            'can_undo_until': self.cancellation_history[event.id]['can_undo_until'],
            'notifications_sent': True,
            'removed_from_feed': True
        }
    
    def undo_cancel(self, event, user) -> Dict[str, Any]:
        """
        Undo a cancellation within the time window.
        
        Args:
            event: Event to restore
            user: User requesting undo
            
        Returns:
            Dict with undo details
            
        Raises:
            CancellationError: If undo not possible
        """
        # Check if event has cancellation history
        if event.id not in self.cancellation_history:
            raise CancellationError(
                f"No cancellation history found for event {event.id}"
            )
        
        history = self.cancellation_history[event.id]
        
        # Check if event is actually canceled
        if event.status != 'CANCELED':
            raise CancellationError(
                f"Event {event.id} is not currently canceled (status: {event.status})"
            )
        
        # Check if within undo window
        now = datetime.now()
        if now > history['can_undo_until']:
            elapsed = (now - history['canceled_at']).total_seconds() / 60
            raise CancellationError(
                f"Undo window expired. Event was canceled {elapsed:.1f} minutes ago. "
                f"Undo is only available for {self.undo_window_minutes} minutes after cancellation."
            )
        
        # Check permissions
        if not self._check_permission(event, user):
            raise CancellationError(
                f"User {user.user_id} does not have permission to undo cancellation. "
                f"Only the organizer or a teacher can undo cancellations."
            )
        
        # Restore the event
        event.status = history['original_status']
        event.cancellation_reason = None
        event.canceled_at = None
        
        # Restore to feed/search (simulated)
        self._restore_to_feed(event)
        
        # Send restoration notifications (simulated)
        self._trigger_restoration_notifications(event, user)
        
        undo_time = datetime.now()
        
        # Keep history but mark as undone
        self.cancellation_history[event.id]['undone_at'] = undo_time
        self.cancellation_history[event.id]['undone_by'] = user.user_id
        
        return {
            'event_id': event.id,
            'status': event.status,
            'undone_by': user.user_id,
            'undone_at': undo_time,
            'original_cancellation_time': history['canceled_at'],
            'restored_to_feed': True,
            'notifications_sent': True
        }
    
    def can_undo(self, event) -> bool:
        """
        Check if an event cancellation can be undone.
        
        Args:
            event: Event to check
            
        Returns:
            bool: True if undo is possible
        """
        if event.id not in self.cancellation_history:
            return False
        
        history = self.cancellation_history[event.id]
        
        # Check if already undone
        if 'undone_at' in history:
            return False
        
        # Check if within time window
        now = datetime.now()
        return now <= history['can_undo_until']
    
    def _check_permission(self, event, user) -> bool:
        """
        Check if user has permission to cancel/undo event.
        
        Args:
            event: Event object
            user: User object
            
        Returns:
            bool: True if user has permission
        """
        # Teacher can always cancel
        if user.role == 'teacher':
            return True
        
        # Organizer can cancel their own events
        if hasattr(event, 'organizer_id') and event.organizer_id == user.user_id:
            return True
        
        return False
    
    def _trigger_notifications(self, event, user, reason: Optional[str]):
        """Simulate sending cancellation notifications."""
        # In a real system, this would send emails/notifications
        pass
    
    def _remove_from_feed(self, event):
        """Simulate removing event from feed and search."""
        # In a real system, this would update the database
        pass
    
    def _restore_to_feed(self, event):
        """Simulate restoring event to feed and search."""
        # In a real system, this would update the database
        pass
    
    def _trigger_restoration_notifications(self, event, user):
        """Simulate sending restoration notifications."""
        # In a real system, this would send emails/notifications
        pass
