from rsvp import RSVP
from datetime import datetime
from events import Events
from user import User

# User Story #37: Implement RSVP functionality (create, cancel, list user RSVPs).
# Backfill commit to document feature implementation.

class RSVPService:
    def __init__(self):
        self.rsvps = []

    def __repr__(self):
        if not self.rsvps:
            return "No RSVPs yet."
        return "All current RSVPs:\n" + "\n".join([f"User {r.user_id} is '{r.status}' for event '{r.event.title}'" for r in self.rsvps])
    
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
    
    def get_user_rsvps(self, user):
        user_rsvps = [r for r in self.rsvps if r.user_id == user.user_id and r.status == "going"]
        if not user_rsvps:
            return "You have no active RSVPs."
        return [f"{r.event.title}: {r.status}" for r in user_rsvps]

    
