class RSVP:
    def __init__(self, event, user_id, role):
        self.event = event
        self.user_id = user_id
        self.role = role
        self.created_at = None
        self.status = None