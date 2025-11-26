"""
Alert model for Xavier University Event System.
Represents event alerts that users can subscribe to.
"""

class Alert:
    """
    Represents an alert for CPSC events.
    
    Attributes:
        alert_id (str): Unique identifier for the alert
        event_type (str): Type of event (e.g., 'seminar', 'workshop', 'career_fair')
        description (str): Description of what the alert covers
    """
    
    def __init__(self, alert_id, event_type, description):
        """
        Initialize a new Alert.
        
        Args:
            alert_id (str): Unique identifier for the alert
            event_type (str): Type of event this alert covers
            description (str): Description of the alert
        """
        self.alert_id = alert_id
        self.event_type = event_type
        self.description = description
    
    def __repr__(self):
        """
        String representation of the Alert.
        
        Returns:
            str: Formatted alert information
        """
        return (f"Alert(alert_id='{self.alert_id}', "
                f"event_type='{self.event_type}', "
                f"description='{self.description}')")
    
    def __eq__(self, other):
        """
        Check equality based on alert_id.
        
        Args:
            other: Another Alert object
        
        Returns:
            bool: True if alerts have the same alert_id
        """
        if not isinstance(other, Alert):
            return False
        return self.alert_id == other.alert_id
    
    def __hash__(self):
        """
        Make Alert hashable for use in sets and as dict keys.
        
        Returns:
            int: Hash of the alert_id
        """
        return hash(self.alert_id)
