import pytest
from services.library_service import (
    get_patron_status_report
)

# Test displaying all 4 pieces of information of the patron
def test_display_all_patron_info():
    d = get_patron_status_report("777777")

    assert d == {'books_borrowed': [], 'borrow_history': '', 'late_fees': 0.0, 'num_borrowed': 0}
    
# Test displayed info is for the correct patron
def test_correct_patron_info():
    d = get_patron_status_report("123456")

    assert d["num_borrowed"] == 3

# Test checking invalid patron id 7 char
def test_invalid_patron_id_7():
    d = get_patron_status_report("1234567")

    assert d == {}

# Test checking invalid patron id 5 char
def test_invalid_patron_id_5():
    d = get_patron_status_report("12345")

    assert d == {}