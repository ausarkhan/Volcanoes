import re

class CPSC_event:
    def __init__(self, name, date, location):
        self.name = name
        self.date = date
        self.location = location

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
        self.name = new_name.strip()
        return f"Event name successfully updated to '{self.name}'."
