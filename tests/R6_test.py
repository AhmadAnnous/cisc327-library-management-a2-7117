import pytest
from services.library_service import (
    search_books_in_catalog
)

# Test correctly searches for a book by the full title
def test_correct_search_by_full_title():
    l = search_books_in_catalog("The Great Gatsby","title")

    assert "the great gatsby" in l[0]["title"].lower()

# Test correctly searches for book with partial title 'the'
def test_partial_title():
    l = search_books_in_catalog("the","title")

    assert "the" in l[0]["title"].lower()

# Test searches for invalid isbn, too short
def test_invalid_isbn_search_too_short():
    l = search_books_in_catalog("112233445566", "isbn")

    assert l == []

# Test searches for invalid isbn, too long
def test_invalid_isbn_search_too_long():
    l = search_books_in_catalog("11223344556677", "isbn")

    assert l == []

# Test correctly searches for book with valid isbn.
def test_correct_isbn_search():
    l = search_books_in_catalog("1122334455667", "isbn")

    assert l[0]["isbn"] == "1122334455667"

# Test searching by author
def test_search_by_author():
    l = search_books_in_catalog("Me", "author")

    assert l[0]['author'] == "Me"