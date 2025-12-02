import pytest
from cpsc_event import CPSC_event  # adjust import path to match your repo

def test_update_event_name_success():
    event = CPSC_event("CPSC Kickoff", "2025-09-01", "Xavier South 402")
    msg = event.update_event_name("CPSC Freshman Kickoff")
    assert event.name == "CPSC Freshman Kickoff"
    assert "successfully updated" in msg

def test_empty_name_rejected():
    event = CPSC_event("CPSC Kickoff", "2025-09-01", "Xavier South 402")
    with pytest.raises(ValueError) as excinfo:
        event.update_event_name("   ")
    assert "cannot be empty" in str(excinfo.value)

def test_invalid_characters_rejected():
    event = CPSC_event("CPSC Kickoff", "2025-09-01", "Xavier South 402")
    with pytest.raises(ValueError) as excinfo:
        event.update_event_name("CPSC Freshman Kickoff!!!")
    assert "invalid characters" in str(excinfo.value)

def test_banned_word_rejected():
    event = CPSC_event("CPSC Kickoff", "2025-09-01", "Xavier South 402")
    with pytest.raises(ValueError) as excinfo:
        event.update_event_name("Inappropriate Test Event")
    assert "cannot contain" in str(excinfo.value)

def test_same_name_rejected():
    event = CPSC_event("CPSC Freshman Kickoff", "2025-09-01", "Xavier South 402")
    with pytest.raises(ValueError) as excinfo:
        event.update_event_name("CPSC Freshman Kickoff")
    assert "different from the current name" in str(excinfo.value)
