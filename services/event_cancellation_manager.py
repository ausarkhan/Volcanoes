"""
Event Cancellation Service with cancel and undo functionality.
Handles permission checks, status updates, and notifications.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class CancellationError(Exception):
    """Raised when cancellation operation fails."""
    pass


class EventCancellationManager:
    """
    Manages event cancellation and undo operations.
    Handles permissions, notifications, and feed management.
    """
    
    def __init__(self, permission_service=None, notification_service=None, feed_service=None):
        """
        Initialize the Event Cancellation Manager.
        
        Args:
            permission_service: Service to check user permissions
            notification_service: Service to send notifications
            feed_service: Service to manage event feed/search
        """
        self.permission_service = permission_service
        self.notification_service = notification_service
        self.feed_service = feed_service
        self._cancellation_history = {}  # Track cancellations for undo
    
    def cancel_event(self, event, user, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancel an event with permission checks and notifications.
        
        Args:
            event: Event object to cancel
            user: User attempting to cancel
            reason: Optional reason for cancellation
        
        Returns:
            Dict containing cancellation details
        
        Raises:
            CancellationError: If cancellation fails
        """
        # Step 1: Permission check
        if not self._check_permission(event, user):
            raise CancellationError(
                f"User {user.user_id} does not have permission to cancel event {event.id}"
            )
        
        # Step 2: Check if already canceled
        if hasattr(event, 'status') and event.status == 'CANCELED':
            raise CancellationError(f"Event {event.id} is already canceled")
        
        # Step 3: Store previous state for potential undo
        previous_state = {
            'status': getattr(event, 'status', 'SCHEDULED'),
            'canceled_at': None,
            'canceled_by': None,
            'cancellation_reason': None,
            'timestamp': datetime.now()
        }
        self._cancellation_history[event.id] = previous_state
        
        # Step 4: Set canceled status
        event.status = 'CANCELED'
        event.canceled_at = datetime.now()
        event.canceled_by = user.user_id
        event.cancellation_reason = reason
        
        # Step 5: Trigger notifications
        notification_result = self._trigger_notifications(event, user, reason)
        
        # Step 6: Remove from feed/search
        feed_result = self._remove_from_feed(event)
        
        result = {
            'success': True,
            'event_id': event.id,
            'canceled_by': user.user_id,
            'canceled_at': event.canceled_at,
            'reason': reason,
            'notifications_sent': notification_result.get('count', 0),
            'removed_from_feed': feed_result.get('success', False),
            'message': f"Event {event.id} has been successfully canceled"
        }
        
        print(f"✓ Event {event.id} canceled by {user.name} ({user.user_id})")
        if reason:
            print(f"  Reason: {reason}")
        print(f"  Notifications sent: {result['notifications_sent']}")
        
        return result
    
    def undo_cancel(self, event, user) -> Dict[str, Any]:
        """
        Undo a recent event cancellation (within 10 minutes).
        
        Args:
            event: Event object to restore
            user: User attempting to undo
        
        Returns:
            Dict containing undo operation details
        
        Raises:
            CancellationError: If undo fails
        """
        # Step 1: Verify event is currently canceled
        if not hasattr(event, 'status') or event.status != 'CANCELED':
            raise CancellationError(
                f"Event {event.id} is not canceled. Cannot undo cancellation."
            )
        
        # Step 2: Check if cancellation history exists
        if event.id not in self._cancellation_history:
            raise CancellationError(
                f"No cancellation history found for event {event.id}"
            )
        
        # Step 3: Check time window (within 10 minutes)
        cancellation_time = event.canceled_at
        current_time = datetime.now()
        time_elapsed = current_time - cancellation_time
        
        if time_elapsed > timedelta(minutes=10):
            raise CancellationError(
                f"Cannot undo cancellation. Time window expired "
                f"({time_elapsed.seconds // 60} minutes elapsed, limit is 10 minutes)"
            )
        
        # Step 4: Permission check
        if not self._check_permission(event, user):
            raise CancellationError(
                f"User {user.user_id} does not have permission to undo cancellation"
            )
        
        # Step 5: Restore old status
        previous_state = self._cancellation_history[event.id]
        event.status = previous_state['status']
        
        # Clear cancellation metadata
        old_reason = event.cancellation_reason
        event.canceled_at = None
        event.canceled_by = None
        event.cancellation_reason = None
        
        # Step 6: Re-add to feed/search
        feed_result = self._add_to_feed(event)
        
        # Step 7: Notify subscribers about restoration
        notification_result = self._notify_restoration(event, user, old_reason)
        
        # Step 8: Remove from history
        del self._cancellation_history[event.id]
        
        result = {
            'success': True,
            'event_id': event.id,
            'restored_by': user.user_id,
            'restored_at': current_time,
            'restored_status': event.status,
            'time_elapsed_seconds': time_elapsed.seconds,
            'notifications_sent': notification_result.get('count', 0),
            'added_to_feed': feed_result.get('success', False),
            'message': f"Event {event.id} cancellation has been undone"
        }
        
        print(f"✓ Cancellation undone for event {event.id} by {user.name}")
        print(f"  Restored to status: {event.status}")
        print(f"  Time elapsed: {time_elapsed.seconds} seconds")
        print(f"  Notifications sent: {result['notifications_sent']}")
        
        return result
    
    def _check_permission(self, event, user) -> bool:
        """
        Check if user has permission to cancel/undo event.
        
        Args:
            event: Event object
            user: User object
        
        Returns:
            bool: True if user has permission
        """
        # Use permission service if available
        if self.permission_service:
            return self.permission_service.can_manage_event(user, event)
        
        # Default: Check if user is organizer or teacher
        if hasattr(event, 'organizer_id') and event.organizer_id == user.user_id:
            return True
        
        if hasattr(user, 'role') and user.role == 'teacher':
            return True
        
        return False
    
    def _trigger_notifications(self, event, user, reason: Optional[str]) -> Dict[str, Any]:
        """
        Send cancellation notifications to subscribers.
        
        Args:
            event: Canceled event
            user: User who canceled
            reason: Cancellation reason
        
        Returns:
            Dict with notification results
        """
        if self.notification_service:
            return self.notification_service.notify_cancellation(
                event=event,
                canceled_by=user,
                reason=reason
            )
        
        # Simulated notification
        print(f"  → Sending cancellation notifications for event {event.id}")
        return {
            'success': True,
            'count': 0,  # Would be actual count in production
            'message': 'Notifications queued (simulated)'
        }
    
    def _notify_restoration(self, event, user, previous_reason: Optional[str]) -> Dict[str, Any]:
        """
        Notify subscribers that event cancellation was undone.
        
        Args:
            event: Restored event
            user: User who restored
            previous_reason: Previous cancellation reason
        
        Returns:
            Dict with notification results
        """
        if self.notification_service:
            return self.notification_service.notify_restoration(
                event=event,
                restored_by=user,
                previous_reason=previous_reason
            )
        
        # Simulated notification
        print(f"  → Sending restoration notifications for event {event.id}")
        return {
            'success': True,
            'count': 0,
            'message': 'Restoration notifications queued (simulated)'
        }
    
    def _remove_from_feed(self, event) -> Dict[str, Any]:
        """
        Remove canceled event from feed and search results.
        
        Args:
            event: Event to remove
        
        Returns:
            Dict with removal results
        """
        if self.feed_service:
            return self.feed_service.remove_event(event)
        
        # Simulated feed removal
        print(f"  → Removing event {event.id} from feed and search")
        return {
            'success': True,
            'message': 'Event removed from feed (simulated)'
        }
    
    def _add_to_feed(self, event) -> Dict[str, Any]:
        """
        Re-add restored event to feed and search results.
        
        Args:
            event: Event to add
        
        Returns:
            Dict with addition results
        """
        if self.feed_service:
            return self.feed_service.add_event(event)
        
        # Simulated feed addition
        print(f"  → Re-adding event {event.id} to feed and search")
        return {
            'success': True,
            'message': 'Event added to feed (simulated)'
        }
    
    def get_cancellation_history(self, event_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cancellation history for an event.
        
        Args:
            event_id: Event ID
        
        Returns:
            Cancellation history dict or None
        """
        return self._cancellation_history.get(event_id)
    
    def can_undo(self, event) -> tuple[bool, str]:
        """
        Check if an event cancellation can be undone.
        
        Args:
            event: Event object
        
        Returns:
            Tuple of (can_undo: bool, reason: str)
        """
        if not hasattr(event, 'status') or event.status != 'CANCELED':
            return False, "Event is not canceled"
        
        if event.id not in self._cancellation_history:
            return False, "No cancellation history found"
        
        if not hasattr(event, 'canceled_at') or event.canceled_at is None:
            return False, "Cancellation timestamp not found"
        
        time_elapsed = datetime.now() - event.canceled_at
        if time_elapsed > timedelta(minutes=10):
            return False, f"Time window expired ({time_elapsed.seconds // 60} minutes)"
        
        return True, "Can be undone"
