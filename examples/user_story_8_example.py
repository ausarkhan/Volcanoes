"""
Example demonstrating User Story #8: Alert Subscription System
Shows how Xavier students can subscribe to and manage CPSC event alerts.
"""

import sys
sys.path.insert(0, '/workspaces/Volcanoes')

from models.user import User
from models.alert import Alert


def main():
    print("=" * 70)
    print("User Story #8: CPSC Event Alert Subscription System")
    print("=" * 70)
    print()
    
    # Create some CPSC students
    print("--- Creating Students ---")
    student1 = User(
        name="Maria Garcia",
        email="maria.garcia@xavier.edu",
        user_id="student_001",
        role="student"
    )
    print(f"Created: {student1}")
    
    student2 = User(
        name="James Wilson",
        email="james.wilson@xavier.edu",
        user_id="student_002",
        role="student"
    )
    print(f"Created: {student2}")
    print()
    
    # Create alert types for different CPSC events
    print("--- Available CPSC Event Alerts ---")
    
    seminar_alert = Alert(
        alert_id="alert_seminar",
        event_type="seminar",
        description="Get notified about CPSC guest speaker seminars"
    )
    print(f"1. {seminar_alert}")
    
    workshop_alert = Alert(
        alert_id="alert_workshop",
        event_type="workshop",
        description="Get notified about hands-on CPSC workshops"
    )
    print(f"2. {workshop_alert}")
    
    hackathon_alert = Alert(
        alert_id="alert_hackathon",
        event_type="hackathon",
        description="Get notified about CPSC hackathon competitions"
    )
    print(f"3. {hackathon_alert}")
    
    career_fair_alert = Alert(
        alert_id="alert_career_fair",
        event_type="career_fair",
        description="Get notified about CPSC career fair events"
    )
    print(f"4. {career_fair_alert}")
    
    study_group_alert = Alert(
        alert_id="alert_study_group",
        event_type="study_group",
        description="Get notified about CPSC study group sessions"
    )
    print(f"5. {study_group_alert}")
    print()
    
    # Student 1 subscribes to multiple alerts
    print("--- Student 1: Maria subscribes to alerts ---")
    result1 = student1.subscribe_to_alert(seminar_alert)
    print(f"Subscribe to seminars: {result1}")
    
    result2 = student1.subscribe_to_alert(hackathon_alert)
    print(f"Subscribe to hackathons: {result2}")
    
    result3 = student1.subscribe_to_alert(career_fair_alert)
    print(f"Subscribe to career fairs: {result3}")
    
    print(f"\nMaria's status: {student1}")
    print(f"Maria is now receiving alerts for:")
    for alert in student1.alerts:
        print(f"  - {alert.event_type}: {alert.description}")
    print()
    
    # Student 2 subscribes to different alerts
    print("--- Student 2: James subscribes to alerts ---")
    result4 = student2.subscribe_to_alert(workshop_alert)
    print(f"Subscribe to workshops: {result4}")
    
    result5 = student2.subscribe_to_alert(study_group_alert)
    print(f"Subscribe to study groups: {result5}")
    
    result6 = student2.subscribe_to_alert(career_fair_alert)
    print(f"Subscribe to career fairs: {result6}")
    
    print(f"\nJames's status: {student2}")
    print(f"James is now receiving alerts for:")
    for alert in student2.alerts:
        print(f"  - {alert.event_type}: {alert.description}")
    print()
    
    # Demonstrate duplicate prevention
    print("--- Testing Duplicate Prevention ---")
    result = student1.subscribe_to_alert(hackathon_alert)
    print(f"Maria tries to subscribe to hackathons again: {result}")
    print(f"Maria still has {len(student1.alerts)} alerts (no duplicate added)")
    print()
    
    # Student 1 unsubscribes from an alert
    print("--- Student 1: Maria changes her mind ---")
    print(f"Maria is too busy and wants to unsubscribe from career fairs")
    result = student1.unsubscribe_from_alert(career_fair_alert)
    print(f"Unsubscribe result: {result}")
    
    print(f"\nMaria's updated status: {student1}")
    print(f"Maria is now receiving alerts for:")
    for alert in student1.alerts:
        print(f"  - {alert.event_type}: {alert.description}")
    print()
    
    # Try to unsubscribe from something not subscribed to
    print("--- Testing Unsubscribe Error Handling ---")
    result = student2.unsubscribe_from_alert(seminar_alert)
    print(f"James tries to unsubscribe from seminars (never subscribed): {result}")
    print()
    
    # Final summary
    print("=" * 70)
    print("Final Summary")
    print("=" * 70)
    print(f"\nMaria Garcia ({student1.email}):")
    print(f"  Active alert subscriptions: {len(student1.alerts)}")
    for i, alert in enumerate(student1.alerts, 1):
        print(f"    {i}. {alert.event_type}")
    
    print(f"\nJames Wilson ({student2.email}):")
    print(f"  Active alert subscriptions: {len(student2.alerts)}")
    for i, alert in enumerate(student2.alerts, 1):
        print(f"    {i}. {alert.event_type}")
    
    print()
    print("=" * 70)
    print("✓ Alert subscription system working as expected!")
    print("  Students can now stay active in their CPSC major by receiving")
    print("  personalized event alerts based on their interests.")
    print("=" * 70)


if __name__ == "__main__":
    main()
