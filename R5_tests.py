import pytest
from library_service import (
    calculate_late_fee_for_book
)

# Test book returned on / before due date
def test_book_returned_on_time():
    fees, days = calculate_late_fee_for_book("123456", 3)

    assert fees == 0.00
    assert days <= 14

# Test invalid patron id
def test_invalid_patron_id():
    fees, days = calculate_late_fee_for_book("1234567", 3)

    assert fees == 0.00
    assert days == 0

# Test book returned 3 days overdue, $0.50 per day up to 7
def test_book_returned_3_days_late():
    fees, days = calculate_late_fee_for_book("123456", 3)

    assert fees == 1.50
    assert days == 17

# Test book returned 8 days overdue, $0.50 up to 7 days + $1 x remaining days up to $15
def test_book_returned_10_days_late():
    fees, days = calculate_late_fee_for_book("123456", 3)

    assert fees == 6.50
    assert days == 24

# Test book returned after more than 33 days, max fee of $15
def test_max_fees():
    fees, days = calculate_late_fee_for_book("123456", 3)

    assert fees == 15.00
    assert days >= 33