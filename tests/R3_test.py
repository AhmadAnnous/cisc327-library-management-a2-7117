import pytest
from services.library_service import (
    borrow_book_by_patron, return_book_by_patron, add_book_to_catalog
)

# Test borrowing a valid book
def test_valid_borrow():
    valid1, message1 = return_book_by_patron("123456", 3)
    valid, message = borrow_book_by_patron("123456", 3)

    assert "successfully borrowed" in message.lower()
    assert valid == True
    

# Test borrowing a book that is not available
def test_book_not_available():
    valid2, message3 = borrow_book_by_patron("123456", 1)
    valid, message = borrow_book_by_patron("123456", 1)

    assert valid == False
    assert "not available" in message.lower()

# Test borrowing a book with invalid patron ID  
def test_invalid_patron_id():
    valid, message = borrow_book_by_patron("12345", 1)

    assert valid == False
    assert "invalid patron id" in message.lower()

# Test borrowing a book with invalid book ID
def test_invalid_book_id():
    valid, message = borrow_book_by_patron("123456", -1)

    assert valid == False
    assert "book not found" in message.lower()

# Patron reached borrowing limit
def test_patron_reached_borrow_limit(mocker):
    mocker.patch('services.library_service.get_patron_borrow_count', return_value = 6)
    valid, message = borrow_book_by_patron("111111", 4)
    assert valid == False
    assert "borrowing limit" in message.lower()

# Test database error
def test_database_error(mocker):
    mocker.patch('services.library_service.insert_borrow_record', return_value = False)
    valid, message = borrow_book_by_patron("123456", 3)

    assert valid == False
    assert "database error" in message.lower()