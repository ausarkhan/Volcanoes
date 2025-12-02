import unittest
from datetime import datetime
from rsvp_service import RSVPService
from rsvp import RSVP
from events import Events
from user import User


class TestRSVPService(unittest.TestCase):

    def setUp(self):
        self.rsvp_service = RSVPService()
        self.event1 = Events("Hackathon", "Coding event", "2:00pm", "5:00pm", "Science Building")
        self.event2 = Events("Workshop", "Python workshop", "3:00pm", "4:00pm", "Library")

        self.user1 = User("Alice", "alice@example.com", 1, "student")
        self.user2 = User("Bob", "bob@example.com", 2, "student")

    # Test create_rsvp()
    def test_create_rsvp_success(self):
        msg = self.rsvp_service.create_rsvp(self.event1, self.user1)
        self.assertEqual(msg, "RSVP confirmed for 'Hackathon'.")
        self.assertEqual(len(self.rsvp_service.rsvps), 1)
        self.assertEqual(self.rsvp_service.rsvps[0].status, "going")

    def test_create_rsvp_duplicate(self):
        self.rsvp_service.create_rsvp(self.event1, self.user1)
        msg = self.rsvp_service.create_rsvp(self.event1, self.user1)
        self.assertEqual(msg, "You have already RSVP’d to this event.")
        self.assertEqual(len(self.rsvp_service.rsvps), 1)
    
    # Test cancel_rsvp()
    def test_cancel_rsvp_success(self):
        self.rsvp_service.create_rsvp(self.event1, self.user1)
        msg = self.rsvp_service.cancel_rsvp(self.event1, self.user1)

        self.assertEqual(msg, "RSVP for 'Hackathon' has been cancelled.")
        self.assertEqual(self.rsvp_service.rsvps[0].status, "cancelled")

    def test_cancel_rsvp_not_found(self):
        msg = self.rsvp_service.cancel_rsvp(self.event1, self.user1)
        self.assertEqual(msg, "No active RSVP found to cancel.")

     # Test get_user_rsvps()
    def test_get_user_rsvps_with_results(self):
        self.rsvp_service.create_rsvp(self.event1, self.user1)
        self.rsvp_service.create_rsvp(self.event2, self.user1)

        result = self.rsvp_service.get_user_rsvps(self.user1)

        self.assertEqual(len(result), 2)
        self.assertIn("Hackathon: going", result)
        self.assertIn("Workshop: going", result)

    def test_get_user_rsvps_none(self):
        result = self.rsvp_service.get_user_rsvps(self.user1)
        self.assertEqual(result, "You have no active RSVPs.")


if __name__ == '__main__':
    unittest.main()