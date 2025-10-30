import pytest
from services.library_service import (
    add_book_to_catalog
)

# Test adding a valid book
def test_add_book_valid_book():
    valid, message = add_book_to_catalog("My Book", "Me", "1122334455667", 7)

    assert valid == True
    assert "successfully added" in message.lower()

# Test adding an invalid book with no title
def test_add_book_no_title():
    valid, message = add_book_to_catalog("", "Me", "1122334455667", 7)
    
    assert valid == False
    assert "Title is required" in message

# Test adding an invalid book with an author name that is too long
def test_add_book_author_too_long():
    valid, message = add_book_to_catalog("My Book", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz", "1122334455667", 7)

    assert valid == False
    assert "Author must be less than 100 characters." in message

# Test adding an invalid book with a negative amount of copies.
def test_add_book_copies_neg_int():
    valid, message = add_book_to_catalog("My Book", "Me", "1122334455667", -2)
    
    assert valid == False
    assert "Total copies must be a positive integer." in message

# Test adding an invalid book with an ISBN that is too long
def test_add_book_isbn_too_long():
    valid, message = add_book_to_catalog("My Book", "Me", "11223344556677", 7)

    assert valid == False
    assert "ISBN must be exactly 13 digits." in message
