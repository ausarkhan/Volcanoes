"""
User model for Xavier University Event System.
Supports alert subscriptions for CPSC events.
"""

class User:
    """
    Represents a user in the Xavier University system.
    
    Attributes:
        name (str): User's full name
        email (str): User's email address
        user_id (str): Unique identifier for the user
        role (str): User's role - 'student' or 'teacher'
        alerts (list): List of Alert objects the user is subscribed to
    """
    
    def __init__(self, name, email, user_id, role):
        """
        Initialize a new User.
        
        Args:
            name (str): User's full name
            email (str): User's email address
            user_id (str): Unique identifier for the user
            role (str): User's role - must be 'student' or 'teacher'
        
        Raises:
            ValueError: If role is not 'student' or 'teacher'
        """
        if role not in ['student', 'teacher']:
            raise ValueError("Role must be 'student' or 'teacher'")
        
        self.name = name
        self.email = email
        self.user_id = user_id
        self.role = role
        self.alerts = []
    
    def subscribe_to_alert(self, alert_obj):
        """
        Subscribe the user to an alert.
        
        Args:
            alert_obj: Alert object to subscribe to
        
        Returns:
            str: Confirmation message
        """
        # Check if user is already subscribed
        if alert_obj in self.alerts:
            return f"Already subscribed to alert: {alert_obj}"
        
        # Add alert to user's subscription list
        self.alerts.append(alert_obj)
        return "Successfully subscribed"
    
    def unsubscribe_from_alert(self, alert_obj):
        """
        Unsubscribe the user from an alert.
        
        Args:
            alert_obj: Alert object to unsubscribe from
        
        Returns:
            str: Confirmation message
        """
        if alert_obj in self.alerts:
            self.alerts.remove(alert_obj)
            return "No longer subscribed"
        
        return "Not subscribed to this alert"
    
    def __repr__(self):
        """
        String representation of the User.
        
        Returns:
            str: Formatted user information
        """
        return (f"User(user_id='{self.user_id}', name='{self.name}', "
                f"email='{self.email}', role='{self.role}', "
                f"subscribed_alerts={len(self.alerts)})")
