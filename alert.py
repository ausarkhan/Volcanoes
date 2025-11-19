class Alert:
    """
    Alert class for managing CPSC event notifications for Xavier students.
    
    Attributes:
        alert_type (str): Type of alert - 'reminder', 'new event', or 'site maintenance'
        recipient (Student): The student receiving the alert
        event (CSClubEvent): The CS club event associated with the alert
        are_alerts_on (bool): Whether alerts are enabled for this recipient
    """
    
    def __init__(self, alert_type, recipient, event, are_alerts_on=True):
        """
        Initialize an Alert instance.
        
        Args:
            alert_type (str): Type of alert ('reminder', 'new event', 'site maintenance')
            recipient (Student): The student who will receive the alert
            event (CSClubEvent): The event associated with this alert
            are_alerts_on (bool): Whether alerts are enabled (default: True)
        """
        self.alert_type = alert_type
        self.recipient = recipient
        self.event = event
        self.are_alerts_on = are_alerts_on
    
    def __repr__(self):
        """
        Return a string representation of the Alert.
        
        Returns:
            str: Formatted string showing alert information
        """
        status = "ON" if self.are_alerts_on else "OFF"
        return (f"Alert(type='{self.alert_type}', "
                f"recipient={self.recipient}, "
                f"event={self.event}, "
                f"alerts={status})")
    
    def send_alert(self):
        """
        Deliver the notification to the recipient.
        
        Returns:
            bool: True if alert was sent successfully, False otherwise
        """
        if not self.are_alerts_on:
            print(f"Alert not sent: Notifications are turned off for {self.recipient}")
            return False
        
        if self.alert_type == "reminder":
            message = f"Reminder: {self.event} is coming up!"
        elif self.alert_type == "new event":
            message = f"New CPSC Event: {self.event} has been added!"
        elif self.alert_type == "site maintenance":
            message = f"Site Maintenance: Event system will be down. {self.event} details may be temporarily unavailable."
        else:
            message = f"Alert: {self.event}"
        
        print(f"📧 Sending alert to {self.recipient}:")
        print(f"   {message}")
        return True
    
    def update_preferences(self, turn_on):
        """
        Allow users to turn notifications on or off.
        
        Args:
            turn_on (bool): True to enable alerts, False to disable
        
        Returns:
            str: Confirmation message of the preference update
        """
        self.are_alerts_on = turn_on
        status = "enabled" if turn_on else "disabled"
        message = f"Alerts have been {status} for {self.recipient}"
        print(message)
        return message
