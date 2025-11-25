from datetime import datetime
import re
class Events:
    def __init__(self, title, description, start_time, end_time, location):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.created_at = None
        self.updated_at = None

    def __repr__(self):
        return f"title: {self.title}, \ndescription: {self.description}, \nstart_time: {self.start_time}, \nend_time: {self.end_time}, location: {self.location}"
    
    @staticmethod
    def create_event(title, description, start_time, end_time, location):
        event = Events(title, description, start_time, end_time, location)
        event.created_at = datetime.now()
        return event
    

    def is_event_virtual(self):
        virtual_keywords = ["online", "webinar", "virtual", "google meet", "zoom", "microsoft teams", "webex", "slack"]
        url_indicators = ["http://", "https://", "www."]
    
        if any(keyword in self.location.lower() for keyword in virtual_keywords):
            return True

        if any(keyword in self.location.lower() for keyword in url_indicators):
            return True
        return False
    
    def validate_event_name(self, new_name: str) -> None:
            """
            Validates the new event name.

            Raises:
                ValueError if any of the rules are violated.
            """
            errors = []
            cleaned = new_name.strip()

            if not cleaned:
                errors.append("Event name cannot be empty.")

            if len(cleaned) < 5 or len(cleaned) > 100:
                errors.append("Event name must be between 5 and 100 characters.")

            
            if not re.match(r"^[A-Za-z0-9 '&:\-]+$", cleaned):
                errors.append("Event name contains invalid characters.")

            banned_words = ["inappropriate", "test event", "dummy"]
            lower_name = cleaned.lower()
            for word in banned_words:
                if word in lower_name:
                    errors.append(f"Event name cannot contain '{word}'.")

            if cleaned == getattr(self, "name", None):
                errors.append("New event name must be different from the current name.")

            if errors:
                raise ValueError("Invalid event name: " + "; ".join(errors))

    def update_event_name(self, new_name: str) -> str:
        """
        Validates and updates the event name.

        Returns:
            A confirmation message if successful.

        Raises:
            ValueError if validation fails.
        """
        self.validate_event_name(new_name)
        self.title = new_name.strip()
        return f"Event name successfully updated to '{self.title}'."


event1 = Events.create_event("Online Workshop", "Join us for a virtual workshop on Python.", "2023-10-01 10:00am", "2023-10-01 12:00pm", "Zoom")
#print(event1.is_event_virtual())  
event2 = Events.create_event("Local Meetup", "Meetup at the community center.", "2023-10-05 06:00pm", "2023-10-05 08:00pm", "123 Main St")
#print(event2.is_event_virtual())
event3 = Events.create_event("How to win social media", "A lesson on creating an online persona.", "2023-11-15 02:00pm", "2023-11-15 04:00pm", "456 Elm St")
#print(event3.is_event_virtual())
event4 = Events.create_event("Webinar on Data Science", "An in-depth webinar on data science techniques.", "2023-12-01 09:00am", "2023-12-01 11:00am", "http://datasciencewebinar.com")
#print(event4.is_event_virtual())
#print(event1)
print(event1.update_event_name("Advanced Python Workshop"))
print(event1)
print(event1.update_event_name("Online Workshop dummy"))
print(event1.update_event_name("  "))  
print(event1.update_event_name("Test Event&!"))
