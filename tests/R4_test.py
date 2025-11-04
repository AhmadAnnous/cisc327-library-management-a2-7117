import pytest
from services.library_service import (
    return_book_by_patron, borrow_book_by_patron
)

# Test returning a valid borrowed book
def test_valid_book_return():
    valid, message = return_book_by_patron("123456", 3)

    assert valid == True
    assert "successfully returned" in message.lower()

# Test returning a valid book, but incorrect patron ID
def test_invalid_patron_id():
    valid, message = return_book_by_patron("12345678", 3)

    assert valid == False
    assert "invalid patron id" in message.lower()

# Test returning a book that has not been borrowed.
def test_invalid_return_book_not_borrowed():
    valid, message = return_book_by_patron("123456", 6)

    assert valid == False
    assert "not borrowed" in message.lower()

# Test checking if error when database has issue.
def test_database_error(mocker):
    mocker.patch('services.library_service.update_book_availability', return_value = False)
    bvalid, bmessage = borrow_book_by_patron("123456", 3)
    valid, message = return_book_by_patron("123456", 3)

    assert valid == False
    assert "database error" in message.lower()

# Book not found by id
def test_book_not_found_id():
    valid, message = return_book_by_patron("123456", 1000)

    assert valid == False
    assert "book not found" in message.lower()