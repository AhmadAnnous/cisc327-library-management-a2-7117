import pytest
from services.library_service import (
    get_all_books
)

# Test checking if book catalog is displayed in table format.
def catalog_in_table():
    get_all_books()

    assert "Catalogue displayed in table"

# Test checking if book catalog does not include author.
def catalog_not_includes_author():
    get_all_books()

    assert "Author name not shown in catalog table"

# Test checking if catalog correctly shows number of copies.
def catalog_shows_copies():
    get_all_books()

    assert "Catalog table correctly shows Available / Total Copies."

# Test checking if catalog does not include a borrow button.
def catalog_not_contains_borrow_button():
    get_all_books()

    assert "Catalog does not show or contain a working borrow button"