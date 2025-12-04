# Team Volcanoes


## What happens when Dr. Edwards runs your code ($ python main.py)
main.py': [Errno 2] No such file or directory

python3 driver.py
Driver started
Driver ends

## What happens when Dr. Edwards runs your tests ($ python main.py)

python3 -m unittest discover -s tests
EEEEE
======================================================================
ERROR: test_calendar_sync_service (unittest.loader._FailedTest.test_calendar_sync_service)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_calendar_sync_service
...
test_calendar_sync_service.py", line 16
    """Test ICS generation for canceled event includes CANCELLED status."""
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IndentationError: expected an indented block after function definition on line 15


======================================================================
ERROR: test_event_cancellation_manager (unittest.loader._FailedTest.test_event_cancellation_manager)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_event_cancellation_manager
...
test_event_cancellation_manager.py", line 74
    reason="De
           ^
SyntaxError: unterminated string literal (detected at line 74)


======================================================================
ERROR: test_event_cancellation_service (unittest.loader._FailedTest.test_event_cancellation_service)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_event_cancellation_service
    """Test late cancellation (< 24 hours) with valid reason passes validation."""
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
IndentationError: expected an indented block after function definition on line 20


======================================================================
ERROR: test_feed_service (unittest.loader._FailedTest.test_feed_service)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_feed_service
...
ModuleNotFoundError: No module named 'models.events'


======================================================================
ERROR: test_user_story_8 (unittest.loader._FailedTest.test_user_story_8)
----------------------------------------------------------------------
ImportError: Failed to import test module: test_user_story_8
...
ModuleNotFoundError: No module named 'models.events'


----------------------------------------------------------------------
Ran 5 tests in 0.000s

FAILED (errors=5)


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
