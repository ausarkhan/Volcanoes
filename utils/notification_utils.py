"""Notification utilities for sending event updates."""
from datetime import datetime
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationLog:
    """Represents a notification log entry."""
    
    def __init__(
        self,
        student_id: str,
        student_name: str,
        student_email: str,
        event_id: str,
        event_title: str,
        notification_type: str,
        sent_at: datetime,
        urgent: bool = False
    ):
        self.student_id = student_id
        self.student_name = student_name
        self.student_email = student_email
        self.event_id = event_id
        self.event_title = event_title
        self.notification_type = notification_type
        self.sent_at = sent_at
        self.urgent = urgent


class NotificationService:
    """Service for sending notifications to students."""
    
    def __init__(self):
        self._notification_logs: List[NotificationLog] = []
    
    def send_cancellation_email(
        self,
        student_email: str,
        student_name: str,
        event_title: str,
        event_starts_at: datetime,
        cancellation_reason: str,
        urgent: bool = False
    ) -> bool:
        """
        Send a cancellation notification email.
        
        Args:
            student_email: Student's email address
            student_name: Student's name
            event_title: Title of the canceled event
            event_starts_at: When the event was scheduled to start
            cancellation_reason: Reason for cancellation
            urgent: Whether this is an urgent notification
            
        Returns:
            bool indicating success
        """
        # In a real application, this would send an actual email
        # For now, we'll simulate it with logging
        urgency_flag = "[URGENT] " if urgent else ""
        
        logger.info(
            f"{urgency_flag}Sending cancellation email to {student_name} <{student_email}>:\n"
            f"  Event: {event_title}\n"
            f"  Scheduled for: {event_starts_at.strftime('%Y-%m-%d %H:%M')}\n"
            f"  Reason: {cancellation_reason}\n"
        )
        
        return True
    
    def log_notification(self, log_entry: NotificationLog) -> None:
        """Record a notification in the log."""
        self._notification_logs.append(log_entry)
        
        logger.info(
            f"Notification logged: {log_entry.notification_type} sent to "
            f"{log_entry.student_name} ({log_entry.student_id}) at "
            f"{log_entry.sent_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    
    def get_notification_logs(
        self,
        event_id: str = None,
        student_id: str = None
    ) -> List[NotificationLog]:
        """Retrieve notification logs, optionally filtered."""
        logs = self._notification_logs
        
        if event_id:
            logs = [log for log in logs if log.event_id == event_id]
        
        if student_id:
            logs = [log for log in logs if log.student_id == student_id]
        
        return logs
