from events import Events
from datetime import datetime

class FilterEvents:
    def __init__(self, events):
        self.events = events
    
    def __repr__(self):
        virtual_events = self.view_virtual_events()
        if  virtual_events == []:
            return  "No upcoming virtual events."
        return "Upcoming Virtual Events:\n" + "\n".join([f"{event.title} at {event.start_time} ({event.location})" for event in virtual_events])
    
    def view_virtual_events(self):
        virtual_events = []
        for event in self.events:
            if event.is_event_virtual():
                virtual_events.append(event)
        return virtual_events
    