import pytest
from library_service import (
    get_patron_status_report
)

# Test displaying all 4 pieces of information of the patron
def test_display_all_patron_info():
    d = get_patron_status_report("123456")

    assert {"books borrowed","late fees","number of books borrowed","borrow history"} in d
    
# Test displayed info is for the correct patron
def test_correct_patron_info():
    d = get_patron_status_report("123456")

    assert {"books borrowed","late fees","number of books borrowed","borrow history"} in d

# Test checking invalid patron id 7 char
def test_invalid_patron_id_7():
    d = get_patron_status_report("1234567")

    assert "" in d

# Test checking invalid patron id 5 char
def test_invalid_patron_id_5():
    d = get_patron_status_report("12345")

    assert "" in d