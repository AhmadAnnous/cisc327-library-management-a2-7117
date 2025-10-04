"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    Implements R4 as per requirements

    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."

    # Get book borrowed by patron
    patron_books = get_patron_borrowed_books(patron_id)
    returned_book = {}

    for book in patron_books:
        if book["book_id"] == book_id :
            returned_book = book
    
    # Validate book is borrowed by patron
    if returned_book == {}:
        return False, f'Error occured: Book ID: {book_id} not borrowed by patron ID: "{patron_id}."'

    # Update availablility of book and create return record.
    availability_success = update_book_availability(book_id, +1)
    if not availability_success:
        return False, "Database error occured while updating book availability."
    
    return_record_success = update_borrow_record_return_date(patron_id, book_id, datetime.now())
    if not return_record_success:
        return False, "Database error occured while recording book return."
    
    # Calculate and display late fees owed
    fee = 0.00
    if(returned_book["is_overdue"]):
        fees = calculate_late_fee_for_book(patron_id, book_id)
        fee = fees["fee_amount"]
    return True, f'Book successfully returned. Late fees incurred: {fee}'

    

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    Implements R5 as per requirements 

    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        Dict: (fee: float, days_overdue: int)
    
    """
    # Get book from patron records
    patron_books = get_patron_borrowed_books(patron_id)
    late_book = {}

    for book in patron_books:
        if book["book_id"] == book_id :
            late_book = book

    # Calculate how many days overdue
    days_overdue = ((int(datetime.now().strftime("%Y")) - int(late_book['due_date'].strftime("%Y"))) * 365 + (int(datetime.now().strftime("%j")) - int(late_book['due_date'].strftime("%j"))))

    # Calculate fee based on requirements
    if(days_overdue > 7):
        fee = (0.5 * 7) + (days_overdue - 7)
    else:
        fee = 0.5 * days_overdue
    if(fee > 15.00):
        fee = 15.00

    return { 
        'fee_amount': fee,
        'days_overdue': days_overdue,
    }
    

    

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    Implements R6 as per requirements

    Args:
        search_term: alphanumeric search criteria  e.g. "the great 2"
        search_type: title, author, isbn
    """
    books = []

    all_books = get_all_books()

    for book in all_books:
        if search_type == 'title':
            if search_term.lower() in book["title"].lower():
                books.append(book)
        if search_type == 'author':
            if search_term.lower() in book["author"].lower():
                books.append(book)
        if search_type == 'isbn':
            if search_term == book["isbn"].lower():
                books.append(book)

    return books

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    TODO: Implement borrow history as per requirements of R7.
    """
    patron_books = get_patron_borrowed_books(patron_id)

    book_and_due_date = []

    for book in patron_books:
        book_and_due_date.append((book["title"], book["due_date"]))
    
    num_books_borrowed = get_patron_borrow_count(patron_id)

    total_fees = 0.00

    for book in patron_books:
        total_fees += calculate_late_fee_for_book(patron_id, book["book_id"])["fee_amount"]
        
    return {
        'books_borrowed': book_and_due_date,
        'late_fees': total_fees,
        'num_borrowed': num_books_borrowed,
        'borrow_history': '' # Borrow record not yet implemented
    }
