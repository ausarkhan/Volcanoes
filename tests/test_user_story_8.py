"""
Test suite for User Story #8: Alert Subscription System
Tests User class with alert subscription functionality.
"""

import sys
sys.path.insert(0, '/workspaces/Volcanoes')

from models.user import User
from models.alert import Alert


def test_user_creation():
    """Test creating a User object."""
    print("\n=== Test 1: User Creation ===")
    
    # Create a student user
    student = User(
        name="John Doe",
        email="john.doe@xavier.edu",
        user_id="student_001",
        role="student"
    )
    
    print(f"Created student: {student}")
    assert student.name == "John Doe"
    assert student.email == "john.doe@xavier.edu"
    assert student.user_id == "student_001"
    assert student.role == "student"
    assert len(student.alerts) == 0
    print("✓ Student user created successfully")
    
    # Create a teacher user
    teacher = User(
        name="Dr. Sarah Edwards",
        email="s.edwards@xavier.edu",
        user_id="teacher_001",
        role="teacher"
    )
    
    print(f"Created teacher: {teacher}")
    assert teacher.role == "teacher"
    print("✓ Teacher user created successfully")
    
    # Test invalid role
    try:
        invalid_user = User("Jane", "jane@xavier.edu", "usr_003", "admin")
        print("✗ Should have raised ValueError for invalid role")
    except ValueError as e:
        print(f"✓ Correctly rejected invalid role: {e}")


def test_subscribe_to_alert():
    """Test subscribing to alerts."""
    print("\n=== Test 2: Subscribe to Alert ===")
    
    student = User(
        name="Alice Smith",
        email="alice.smith@xavier.edu",
        user_id="student_002",
        role="student"
    )
    
    # Create alerts
    alert1 = Alert(
        alert_id="alert_001",
        event_type="seminar",
        description="Alerts for CPSC seminar events"
    )
    
    alert2 = Alert(
        alert_id="alert_002",
        event_type="workshop",
        description="Alerts for CPSC workshop events"
    )
    
    print(f"Alert 1: {alert1}")
    print(f"Alert 2: {alert2}")
    
    # Subscribe to first alert
    result1 = student.subscribe_to_alert(alert1)
    print(f"\nSubscribe to alert1: {result1}")
    assert result1 == "Successfully subscribed"
    assert len(student.alerts) == 1
    assert alert1 in student.alerts
    print("✓ Successfully subscribed to alert1")
    
    # Subscribe to second alert
    result2 = student.subscribe_to_alert(alert2)
    print(f"Subscribe to alert2: {result2}")
    assert result2 == "Successfully subscribed"
    assert len(student.alerts) == 2
    print("✓ Successfully subscribed to alert2")
    
    print(f"\nStudent now subscribed to {len(student.alerts)} alerts")
    print(f"Updated student: {student}")


def test_prevent_duplicate_subscriptions():
    """Test that duplicate subscriptions are prevented."""
    print("\n=== Test 3: Prevent Duplicate Subscriptions ===")
    
    student = User(
        name="Bob Johnson",
        email="bob.johnson@xavier.edu",
        user_id="student_003",
        role="student"
    )
    
    alert = Alert(
        alert_id="alert_003",
        event_type="career_fair",
        description="Alerts for CPSC career fair events"
    )
    
    # First subscription
    result1 = student.subscribe_to_alert(alert)
    print(f"First subscription: {result1}")
    assert result1 == "Successfully subscribed"
    assert len(student.alerts) == 1
    print("✓ First subscription successful")
    
    # Attempt duplicate subscription
    result2 = student.subscribe_to_alert(alert)
    print(f"Duplicate subscription attempt: {result2}")
    assert "Already subscribed" in result2
    assert len(student.alerts) == 1
    print("✓ Duplicate subscription correctly prevented")
    
    print(f"\nStudent still has {len(student.alerts)} alert(s)")


def test_unsubscribe_from_alert():
    """Test unsubscribing from alerts."""
    print("\n=== Test 4: Unsubscribe from Alert ===")
    
    student = User(
        name="Carol White",
        email="carol.white@xavier.edu",
        user_id="student_004",
        role="student"
    )
    
    alert1 = Alert(
        alert_id="alert_004",
        event_type="hackathon",
        description="Alerts for CPSC hackathon events"
    )
    
    alert2 = Alert(
        alert_id="alert_005",
        event_type="guest_lecture",
        description="Alerts for guest lecture events"
    )
    
    # Subscribe to both alerts
    student.subscribe_to_alert(alert1)
    student.subscribe_to_alert(alert2)
    print(f"Subscribed to {len(student.alerts)} alerts")
    print(f"Student: {student}")
    
    # Unsubscribe from first alert
    result1 = student.unsubscribe_from_alert(alert1)
    print(f"\nUnsubscribe from alert1: {result1}")
    assert result1 == "No longer subscribed"
    assert len(student.alerts) == 1
    assert alert1 not in student.alerts
    assert alert2 in student.alerts
    print("✓ Successfully unsubscribed from alert1")
    
    # Unsubscribe from second alert
    result2 = student.unsubscribe_from_alert(alert2)
    print(f"Unsubscribe from alert2: {result2}")
    assert result2 == "No longer subscribed"
    assert len(student.alerts) == 0
    print("✓ Successfully unsubscribed from alert2")
    
    print(f"\nStudent now has {len(student.alerts)} alerts")
    print(f"Updated student: {student}")


def test_unsubscribe_not_subscribed():
    """Test unsubscribing from an alert user isn't subscribed to."""
    print("\n=== Test 5: Unsubscribe from Non-Subscribed Alert ===")
    
    student = User(
        name="David Lee",
        email="david.lee@xavier.edu",
        user_id="student_005",
        role="student"
    )
    
    alert = Alert(
        alert_id="alert_006",
        event_type="study_group",
        description="Alerts for study group events"
    )
    
    # Attempt to unsubscribe without being subscribed
    result = student.unsubscribe_from_alert(alert)
    print(f"Unsubscribe result: {result}")
    assert result == "Not subscribed to this alert"
    assert len(student.alerts) == 0
    print("✓ Correctly handled unsubscribe from non-subscribed alert")


def test_multiple_users_same_alert():
    """Test that multiple users can subscribe to the same alert."""
    print("\n=== Test 6: Multiple Users with Same Alert ===")
    
    student1 = User("Eve Adams", "eve.adams@xavier.edu", "student_006", "student")
    student2 = User("Frank Brown", "frank.brown@xavier.edu", "student_007", "student")
    
    alert = Alert(
        alert_id="alert_007",
        event_type="all_cpsc_events",
        description="Alerts for all CPSC events"
    )
    
    # Both students subscribe to same alert
    result1 = student1.subscribe_to_alert(alert)
    result2 = student2.subscribe_to_alert(alert)
    
    print(f"Student 1: {student1}")
    print(f"Student 2: {student2}")
    
    assert result1 == "Successfully subscribed"
    assert result2 == "Successfully subscribed"
    assert alert in student1.alerts
    assert alert in student2.alerts
    print("✓ Multiple users can subscribe to same alert")


def run_all_tests():
    """Run all test cases for User Story #8."""
    print("=" * 60)
    print("User Story #8: Alert Subscription System - Test Suite")
    print("=" * 60)
    
    try:
        test_user_creation()
        test_subscribe_to_alert()
        test_prevent_duplicate_subscriptions()
        test_unsubscribe_from_alert()
        test_unsubscribe_not_subscribed()
        test_multiple_users_same_alert()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
