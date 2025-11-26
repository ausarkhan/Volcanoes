# User Story #37: RSVP model for event attendance.
# Backfill commit to provide documentation and clarity.

class RSVP:
    def __init__(self, event, user_id, role):
        self.event = event
        self.user_id = user_id
        self.role = role
        self.created_at = None
        self.status = None

    def __repr__(self):
        return (f"RSVP(user_id={self.user_id}, role={self.role}, status={self.status}, event_title='{self.event.title}')")