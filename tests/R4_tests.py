import pytest
from library_service import (
    return_book_by_patron
)

# Test returning a valid borrowed book
def test_valid_book_return():
    valid, message = return_book_by_patron("123456", 3)

    assert valid == True
    assert "returned succesully" in message.lower()

# Test returning a valid book, but incorrect patron ID
def test_invalid_patron_id():
    valid, message = return_book_by_patron("12345678", 3)

    assert valid == False
    assert "invalid id" in message.lower()

# Test returning a book that has not been borrowed.
def test_invalid_return_book_not_borrowed():
    valid, message = return_book_by_patron("123456", 1)

    assert valid == False
    assert "book not borrowed" in message.lower()

# Test checking if error when database has issue.
def test_database_error():
    valid, message = return_book_by_patron("123456", 3)

    assert valid == False
    assert "database error" in message.lower()