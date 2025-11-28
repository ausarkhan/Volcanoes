"""Event Cancellation Service for Xavier course management system.

This service handles event cancellation logic including validation
for late cancellations that require a reason.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List
from models.event import Event
from services.rsvp_service import RSVPService
from utils.notification_utils import NotificationService, NotificationLog


class ValidationError(Exception):
    """Raised when cancellation validation fails."""
    pass


class EventCancellationService:
    """Service for managing event cancellations."""
    
    def __init__(
        self,
        rsvp_service: RSVPService = None,
        notification_service: NotificationService = None
    ):
        """
        Initialize EventCancellationService.
        
        Args:
            rsvp_service: Service for retrieving RSVPs (optional, will create if not provided)
            notification_service: Service for sending notifications (optional, will create if not provided)
        """
        self.rsvp_service = rsvp_service or RSVPService()
        self.notification_service = notification_service or NotificationService()
    
    def validate_cancellation_reason(self, event: Event, reason: str) -> Dict[str, Any]:
        """
        Validate cancellation reason based on timing.
        
        Use Case RP1: Require Reason for Late Cancellations
        - Calculates time difference between now and event start time
        - If event starts in less than 24 hours, ensures reason is not empty
        - Returns validation result or raises an error
        
        Args:
            event: The event being canceled
            reason: The cancellation reason provided
            
        Returns:
            Dict containing:
                - valid: bool indicating if validation passed
                - is_late_cancellation: bool indicating if within 24 hours
                - hours_until_event: float hours until event starts
                - message: str validation message
                
        Raises:
            ValidationError: If validation fails (late cancellation without reason)
        """
        now = datetime.now()
        time_until_event = event.starts_at - now
        hours_until_event = time_until_event.total_seconds() / 3600
        
        # Check if this is a late cancellation (less than 24 hours notice)
        is_late_cancellation = hours_until_event < 24
        
        validation_result = {
            'valid': True,
            'is_late_cancellation': is_late_cancellation,
            'hours_until_event': hours_until_event,
            'message': 'Validation passed'
        }
        
        # If event starts in less than 24 hours, reason must be provided
        if is_late_cancellation:
            if not reason or reason.strip() == '':
                validation_result['valid'] = False
                validation_result['message'] = (
                    f"Cancellation reason is required for events starting in less than 24 hours. "
                    f"This event starts in {hours_until_event:.1f} hours."
                )
                raise ValidationError(validation_result['message'])
            else:
                validation_result['message'] = (
                    f"Late cancellation validated. Event starts in {hours_until_event:.1f} hours. "
                    f"Reason provided: {reason[:50]}..."
                )
        else:
            if reason and reason.strip():
                validation_result['message'] = (
                    f"Cancellation validated. Event starts in {hours_until_event:.1f} hours. "
                    f"Reason: {reason[:50]}..."
                )
            else:
                validation_result['message'] = (
                    f"Cancellation validated. Event starts in {hours_until_event:.1f} hours. "
                    f"No reason required (more than 24 hours notice)."
                )
        
        return validation_result
    
    def notify_rsvp_cancellation(self, event: Event) -> Dict[str, Any]:
        """
        Notify students who RSVP'd to the event about its cancellation.
        
        Use Case RP2: RSVP-Based Cancellation Notifications
        - Retrieves all RSVPs using RSVPService.get_event_rsvps(event.id)
        - Sends cancellation notices only to students who RSVP'd
        - Computes urgent_flag based on how soon the event was scheduled to start
        - Logs which students received the notification along with timestamps
        
        Args:
            event: The event being canceled
            
        Returns:
            Dict containing:
                - event_id: str the event ID
                - event_title: str the event title
                - rsvp_count: int number of students who had RSVP'd
                - notifications_sent: int number of notifications sent
                - urgent: bool whether this was an urgent cancellation
                - hours_until_event: float hours until event start
                - notified_students: List of student IDs who were notified
                - timestamp: datetime when notifications were sent
        """
        now = datetime.now()
        time_until_event = event.starts_at - now
        hours_until_event = time_until_event.total_seconds() / 3600
        
        # Determine if this is urgent (less than 24 hours notice)
        urgent_flag = hours_until_event < 24
        
        # Retrieve all confirmed RSVPs for this event
        rsvps = self.rsvp_service.get_event_rsvps(event.id)
        
        notified_students = []
        notifications_sent = 0
        
        # Send cancellation notification to each student who RSVP'd
        for rsvp in rsvps:
            success = self.notification_service.send_cancellation_email(
                student_email=rsvp.student_email,
                student_name=rsvp.student_name,
                event_title=event.title,
                event_starts_at=event.starts_at,
                cancellation_reason=event.cancellation_reason or "No reason provided",
                urgent=urgent_flag
            )
            
            if success:
                # Log the notification
                log_entry = NotificationLog(
                    student_id=rsvp.student_id,
                    student_name=rsvp.student_name,
                    student_email=rsvp.student_email,
                    event_id=event.id,
                    event_title=event.title,
                    notification_type="CANCELLATION",
                    sent_at=now,
                    urgent=urgent_flag
                )
                self.notification_service.log_notification(log_entry)
                
                notified_students.append(rsvp.student_id)
                notifications_sent += 1
        
        return {
            'event_id': event.id,
            'event_title': event.title,
            'rsvp_count': len(rsvps),
            'notifications_sent': notifications_sent,
            'urgent': urgent_flag,
            'hours_until_event': hours_until_event,
            'notified_students': notified_students,
            'timestamp': now
        }
