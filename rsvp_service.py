from rsvp import RSVP
from datetime import datetime
from events import Events
from user import User
class RSVPService:
    def __init__(self):
        self.rsvps = []

    def create_rsvp(self, event, user):
        for r in self.rsvps:
            if r.event == event and r.user_id == user.user_id and r.status == "going":
                return "You have already RSVP’d to this event."

        rsvp = RSVP(event, user.user_id, user.role)
        rsvp.status = "going"
        rsvp.created_at = datetime.now()
        self.rsvps.append(rsvp)
        return f"RSVP confirmed for '{event.title}'."
    
    def cancel_rsvp(self, event, user):
        for r in self.rsvps:
            if r.event == event and r.user_id == user.user_id and r.status == "going":
                r.status = "cancelled"
                return f"RSVP for '{event.title}' has been cancelled."
        return "No active RSVP found to cancel."