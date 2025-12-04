# Team Volcanoes

## What the Code Does When You Run It

When you run `python3 driver.py`, the program demonstrates the complete Xavier University Event Management System with the following features:

1. **USE CASE P1: COURSE EVENT (PROFESSOR)** - Demonstrates a professor creating a course-related event (CS101 Final Exam Review Session) with automatic section authorization
2. **FEED SERVICE: EVENT FEED MANAGEMENT** - Shows adding events to the feed, displaying feed contents, canceling events, and removing them from the feed
3. **NOTIFICATION SERVICE: FOLLOWER NOTIFICATIONS** - Demonstrates notifying followers when events are created or updated
4. **USE CASE RP1: REQUIRE REASON FOR LATE CANCELLATIONS** - Validates cancellation reasons for events starting within 24 hours (two scenarios: with and without reasons)
5. **USE CASE RP2: RSVP-BASED CANCELLATION NOTIFICATIONS** - Shows cancellation notifications sent to students who RSVP'd to an event, with urgency flags for events starting soon
6. **USE CASE RP3: CALENDAR SYNC FOR CANCELLATIONS** - Demonstrates ICS calendar generation and syncing canceled events to external calendars (Google Calendar, Outlook)
7. **INTEGRATED WORKFLOW: COMPLETE EVENT LIFECYCLE** - End-to-end demonstration of creating an event, adding to feed, RSVPs, validation, cancellation, notifications, and calendar sync

The driver outputs detailed success messages, emoji indicators, and structured information showing each feature in action.

## What the Code Does When You Run Tests

When you run `python3 -m unittest discover -s tests`, the test suite runs the following test modules:

1. **test_calendar_sync_service.py** - Tests ICS calendar data generation and syncing to external calendar integrations
2. **test_event_cancellation_manager.py** - Tests the event cancellation manager functionality
3. **test_event_cancellation_service.py** - Tests event cancellation validation rules, late cancellation detection, and reason requirements
4. **test_feed_service.py** - Tests adding/removing events from the feed and feed management operations
5. **test_user_story_8.py** - Integration tests for the complete user story workflow

The test suite validates all service functionality, edge cases, error handling, and integration between components. All tests should pass with "OK" status if the code is working correctly.

---

## Final Release Checklist

- [ ] README states purpose, contributors, and how to build, run, and test all the code from the CLI. Build and run should **not** assume everyone is using an IDE (no "Run" button or VS Code–specific commands).
- [ ] SDD has the project description, outline, architecture (including UML class diagrams), and all project user stories and use cases.
- [ ] Each team member must update our team's **Statement of Work** shared Excel spreadsheet.  
      Your grade on this assignment is based ONLY on:  
      - the quality of your use cases  
      - your accepted GitHub pull requests  
      - 10% peer evaluation from your teammates
- [ ] **Ja'Nya** must finish her pushes to the repo by **8 PM on Dec 1st**.
- [ ] **Jon** must finish his pushes to the repo by **8 PM on Dec 1st**.
- [ ] **Ausar** must finish his pushes to the repo by **8 PM on Dec 1st**.
- [ ] **Ja'Nya** must do one last check that the code builds, runs, and that all tests run by **10 PM on Dec 1st**.
- [ ] **Ja'Nya** must apply the **"Project Release"** tag to the repo.
- [ ] Everyone must complete the **Brightspace survey** for Assignment08.
- [ ] Everyone should complete the **Class Climate survey** to help Dr. Edwards improve her teaching.

---

## Team Members

- **Designer:** Jon Johnson (john205)  
- **SWE:** Ausar Khan (akhan5)  
- **Lead:** Ja'Nya Ward (jward12)

---

## Project Priority (High → Low)

1. CPSC Events  
2. CPSC Core Curriculum Recommender  
3. CPSC Friends  
4. CPSC Help Desk  
5. CPSC Study Buddies  
6. CPSC Course Offering  

---

### NOTE  
**Get Dr. Edwards' written approval before using any API or package.**


## Project Purpose:
A console-based program where CS/CIS/BINF majors, minors, and faculty can create, edit, remove, list, search, RSVP, and get alerts for events based on their notifications/alert settings. Key features include event notifications, RSVP management, and category-based subscriptions.

## How to build:
```bash
# Clone the repo
git clone https://github.com/ausarkhan/Volcanoes.git
cd Volcanoes

# Install dependencies
pip install -r requirements.txt

# (Optional) create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run instructions:
```bash
# Run the main program
python3 driver.py

# Run all unit tests
python3 -m unittest discover -s tests
```
