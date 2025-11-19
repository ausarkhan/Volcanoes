from datetime import datetime
class Events:
    def __init__(self, title, description, start_time, end_time, location):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.created_at = None
        self.updated_at = None
    
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

event1 = Events.create_event("Online Workshop", "Join us for a virtual workshop on Python.", "2023-10-01 10:00", "2023-10-01 12:00", "Zoom")
print(event1.is_event_virtual())  
even2 = Events.create_event("Local Meetup", "Meetup at the community center.", "2023-10-05 18:00", "2023-10-05 20:00", "123 Main St")
print(even2.is_event_virtual())
event3 = Events.create_event("How to win social media", "A lesson on creating an online persona.", "2023-11-15 14:00", "2023-11-15 16:00", "456 Elm St")
print(event3.is_event_virtual())
event4 = Events.create_event("Webinar on Data Science", "An in-depth webinar on data science techniques.", "2023-12-01 09:00", "2023-12-01 11:00", "http://datasciencewebinar.com")
print(event4.is_event_virtual())

