import pytest
from library_service import (
    borrow_book_by_patron
)

# Test borrowing a valid book
def test_valid_borrow():
    valid, message = borrow_book_by_patron("123456", 1)

    assert valid == True
    assert "succesfully borrowed" in message.lower()

# Test borrowing a book with invalid patron ID  
def test_invalid_patron_id():
    valid, message = borrow_book_by_patron("12345", 1)

    assert valid == False
    assert "invalid id" in message.lower()

# Test borrowing a book with invalid book ID
def test_invalid_book_id():
    valid, message = borrow_book_by_patron("123456", -1)

    assert valid == False
    assert "book not found" in message.lower()

# Test borrowing a valid book, but databse error occurs.
def test_database_error():
    valid, message = borrow_book_by_patron("123456", 3)
    
    assert valid == False
    assert "database error" in message.lower()

