"""
Example: Creating an Exam Review Session Event

Use Case P1: Course Event (Professor)
Demonstrates how a Xavier professor creates an exam review session
so that students have a clear time and place to attend.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from services.course_event_service import CourseEventService


def main():
    """Demonstrate creating an exam review session event."""
    
    print("\n" + "=" * 70)
    print("XAVIER UNIVERSITY - CREATE EXAM REVIEW SESSION")
    print("Use Case P1: Course Event (Professor)")
    print("=" * 70)
    
    # Initialize service
    course_event_service = CourseEventService()
    
    # Professor details
    professor_id = "prof_edwards"
    professor_name = "Dr. Sarah Edwards"
    
    print(f"\n👤 Professor: {professor_name} ({professor_id})")
    
    # Show professor's courses
    print(f"\n📚 Professor's Course Sections:")
    sections = course_event_service.get_sections_for_user(professor_id)
    for section in sections:
        print(f"   - {section['course_code']}: {section['name']}")
    
    # Create exam review session
    print(f"\n📝 Creating Exam Review Session...")
    
    try:
        event = course_event_service.create_course_event(
            professor_id=professor_id,
            professor_name=professor_name,
            course_code="CS101",
            title="CS101 Final Exam Review Session",
            description="Comprehensive review for the final exam covering all topics from the semester",
            starts_at=datetime.now() + timedelta(days=3, hours=2),
            ends_at=datetime.now() + timedelta(days=3, hours=4),
            location="STEM Building, Room 201"
        )
        
        print(f"\n✅ Event Created Successfully!")
        print(f"\n📋 Event Details:")
        print(f"   Event ID: {event.id}")
        print(f"   Title: {event.title}")
        print(f"   Course: CS101")
        print(f"   Description: {event.description}")
        print(f"   Start Time: {event.starts_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   End Time: {event.ends_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Location: {event.location}")
        print(f"   Organizer: {event.organizer_name}")
        print(f"   Status: {event.status}")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    
    # Try to create event for course professor doesn't own
    print(f"\n\n{'=' * 70}")
    print("EXAMPLE: Attempting to Create Event for Wrong Course")
    print("=" * 70)
    
    print(f"\n📝 Attempting to create event for CS999 (not professor's course)...")
    
    try:
        event = course_event_service.create_course_event(
            professor_id=professor_id,
            professor_name=professor_name,
            course_code="CS999",  # Professor doesn't teach this
            title="CS999 Review Session",
            description="Review session",
            starts_at=datetime.now() + timedelta(days=3),
            ends_at=datetime.now() + timedelta(days=3, hours=2),
            location="Room 101"
        )
        
        print(f"\n✅ Event Created Successfully!")
        
    except ValueError as e:
        print(f"\n❌ Validation Failed: {e}")
        print(f"   ℹ️  The system verified that CS999 is not in professor's course list")
    
    # Create another review session for a different course
    print(f"\n\n{'=' * 70}")
    print("EXAMPLE: Creating Another Review Session")
    print("=" * 70)
    
    print(f"\n📝 Creating review session for CS201...")
    
    try:
        event2 = course_event_service.create_course_event(
            professor_id=professor_id,
            professor_name=professor_name,
            course_code="CS201",
            title="CS201 Midterm Review - Data Structures",
            description="Review of linked lists, stacks, queues, and trees",
            starts_at=datetime.now() + timedelta(days=5, hours=3),
            ends_at=datetime.now() + timedelta(days=5, hours=5),
            location="Computer Lab B"
        )
        
        print(f"\n✅ Event Created Successfully!")
        print(f"\n📋 Event Details:")
        print(f"   Event ID: {event2.id}")
        print(f"   Title: {event2.title}")
        print(f"   Course: CS201")
        print(f"   Start Time: {event2.starts_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Location: {event2.location}")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    
    # Show all created events
    print(f"\n\n{'=' * 70}")
    print("ALL CREATED EVENTS")
    print("=" * 70)
    
    all_events = course_event_service.get_all_events()
    print(f"\nTotal Events Created: {len(all_events)}\n")
    
    for evt in all_events:
        print(f"📅 {evt.id}: {evt.title}")
        print(f"   Start: {evt.starts_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Location: {evt.location}")
        print()
    
    print("=" * 70)
    print("✅ DEMO COMPLETE")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Professor creates exam review session event")
    print("  ✓ System verifies course_code belongs to professor")
    print("  ✓ Event provides clear time and place for students")
    print("  ✓ Validation prevents unauthorized course events")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
