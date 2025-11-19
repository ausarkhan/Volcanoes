class Events:
    def __init__(self, title, description, start_time, end_time, location):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.created_at = None
        self.updated_at = None
