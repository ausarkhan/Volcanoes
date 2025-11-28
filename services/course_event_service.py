"""Course Event Service for Xavier course management system.

This service handles creation of course-related events such as exam review sessions.
"""
from datetime import datetime
from typing import Dict, Any, Optional
from models.event import Event
from models.override_request import OverrideRequest


class CourseEventService:
    """Service for managing course events."""
    
    def __init__(self):
        """Initialize CourseEventService."""
        self._events = {}  # In-memory storage for events
        self._override_requests = {}  # In-memory storage for override requests
        self._event_counter = 0
        self._request_counter = 0
    
    def get_sections_for_user(self, user_id: str) -> list:
        """
        Get all course sections where the user is a professor.
        
        In a real system, this would query the CourseService.
        For now, returns mock data.
        
        Args:
            user_id: The professor's user ID
            
        Returns:
            List of course sections with course_code
        """
        # Mock data - in production this would call CourseService
        return [
            {"id": "cs101_fall2025", "course_code": "CS101", "name": "Intro to Computer Science"},
            {"id": "cs201_fall2025", "course_code": "CS201", "name": "Data Structures"},
            {"id": "cs301_fall2025", "course_code": "CS301", "name": "Algorithms"}
        ]
    
    def verify_course_code_belongs_to_professor(
        self, 
        course_code: str, 
        user_id: str
    ) -> bool:
        """
        Verify that the given course_code belongs to the professor.
        
        Uses CourseService to check if course_code is in professor's sections.
        
        Args:
            course_code: The course code to verify
            user_id: The professor's user ID
            
        Returns:
            True if course belongs to professor, False otherwise
        """
        sections = self.get_sections_for_user(user_id)
        return any(section["course_code"] == course_code for section in sections)
    
    def create_request(
        self,
        event_draft: Dict[str, Any],
        conflict_reason: str,
        created_at: datetime,
        updated_at: datetime
    ) -> OverrideRequest:
        """
        Create an OverrideRequest for event with conflict.
        
        Args:
            event_draft: Proposed event data (pending status)
            conflict_reason: Reason for the conflict
            created_at: Timestamp when request was created
            updated_at: Timestamp when request was last updated
            
        Returns:
            OverrideRequest object with status "pending"
        """
        self._request_counter += 1
        request_id = f"override_req_{self._request_counter:04d}"
        
        override_request = OverrideRequest(
            id=request_id,
            event_draft=event_draft,
            conflict_reason=conflict_reason,
            created_at=created_at,
            updated_at=updated_at,
            status="pending"
        )
        
        # Store override request
        self._override_requests[request_id] = override_request
        
        return override_request
    
    def approve_request(
        self,
        override_id: str,
        deny_reason: Optional[str] = None
    ) -> OverrideRequest:
        """
        Approve or deny an OverrideRequest.
        
        If approved, creates an Event from event_draft.
        If denied, updates deny_reason.
        
        Args:
            override_id: The ID of the override request
            deny_reason: Reason for denial (if denying)
            
        Returns:
            Updated override request
            
        Raises:
            ValueError: If override request not found
        """
        override_request = self._override_requests.get(override_id)
        
        if not override_request:
            raise ValueError(f"Override request {override_id} not found")
        
        if deny_reason:
            # Deny the request
            override_request.deny(deny_reason)
        else:
            # Approve the request and create event
            override_request.approve()
            
            # Create the actual event from draft
            event_draft = override_request.event_draft
            self._event_counter += 1
            event_id = f"evt_{self._event_counter:04d}"
            
            event = Event(
                id=event_id,
                title=event_draft["title"],
                description=event_draft["description"],
                starts_at=event_draft["starts_at"],
                ends_at=event_draft["ends_at"],
                location=event_draft["location"],
                organizer_id=event_draft["organizer_id"],
                organizer_name=event_draft["organizer_name"],
                status="SCHEDULED"
            )
            
            # Store event
            self._events[event_id] = {
                "event": event,
                "course_code": event_draft.get("course_code", "")
            }
        
        return override_request
    
    def create_course_event(
        self,
        professor_id: str,
        professor_name: str,
        course_code: str,
        title: str,
        description: str,
        starts_at: datetime,
        ends_at: datetime,
        location: str
    ) -> Event:
        """
        Create a course event (e.g., exam review session).
        
        Use Case P1: Course Event (Professor)
        - Verifies course_code belongs to professor using CourseService
        - Creates a CourseEvent class with get_sections_for_user method
        - Updates EventService with create_professor_event method
        - Constructs an Event object
        
        Args:
            professor_id: ID of the professor creating the event
            professor_name: Name of the professor
            course_code: Course code (e.g., "CS101")
            title: Event title
            description: Event description
            starts_at: Event start time
            ends_at: Event end time
            location: Event location
            
        Returns:
            Created Event object
            
        Raises:
            ValueError: If course_code doesn't belong to professor
        """
        # Verify professor owns this course
        if not self.verify_course_code_belongs_to_professor(course_code, professor_id):
            raise ValueError(
                f"Course code '{course_code}' does not belong to professor {professor_id}"
            )
        
        # Generate event ID
        self._event_counter += 1
        event_id = f"evt_{self._event_counter:04d}"
        
        # Create the event
        event = Event(
            id=event_id,
            title=title,
            description=description,
            starts_at=starts_at,
            ends_at=ends_at,
            location=location,
            organizer_id=professor_id,
            organizer_name=professor_name,
            status="SCHEDULED"
        )
        
        # Store event
        self._events[event_id] = {
            "event": event,
            "course_code": course_code
        }
        
        return event
    
    def get_event(self, event_id: str) -> Optional[Event]:
        """
        Retrieve an event by ID.
        
        Args:
            event_id: The event ID
            
        Returns:
            Event object if found, None otherwise
        """
        event_data = self._events.get(event_id)
        return event_data["event"] if event_data else None
    
    def get_all_events(self) -> list:
        """
        Get all events.
        
        Returns:
            List of all Event objects
        """
        return [data["event"] for data in self._events.values()]
