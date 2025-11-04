import pytest
from services.library_service import (
    add_book_to_catalog
)

# Test adding a valid book
def test_add_book_valid_book(mocker):
    mocker.patch('services.library_service.get_book_by_isbn', return_value = False)
    mocker.patch('services.library_service.insert_book', return_value = True)
    valid, message = add_book_to_catalog("My Book", "Me", "1122334455667", 7)

    assert "successfully added" in message.lower()
    assert valid == True

# Tests if the book title is too long
def test_title_too_long():
    valid, message = add_book_to_catalog("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Me", "1234567890123",5)

    assert valid == False
    assert "less than 200" in message.lower()

# Tests if there is an author
def test_no_author():
    valid, message = add_book_to_catalog("Book 2", "", "1234123412341", 3)

    assert valid == False
    assert "author is required" in message.lower()

# Tests a book that already exists with the isbn
def test_book_already_exists_isbn():
    valid, message = add_book_to_catalog("Book 3", "Me", "1122334455667", 4)

    assert valid == False
    assert "already exists" in message.lower()

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

# Test database error
def test_database_error(mocker):
    mocker.patch('services.library_service.insert_book', return_value = False)
    valid, message = add_book_to_catalog("Book 4", "Me", "1212121212121", 1)

    assert valid == False
    assert "database error" in message.lower()