from playwright.sync_api import Page, expect

def test_search_borrow_book(page: Page):
    # Open page
    page.goto("http://localhost:5000/catalog")

    # Search for book "My Book" by author "Me"
    page.get_by_role("link", name="🔍 Search").click()
    page.get_by_role("textbox", name="Search Term").click()
    page.get_by_role("textbox", name="Search Term").fill("Me")
    page.get_by_label("Search Type").select_option("author")
    page.get_by_role("button", name="🔍 Search").click()

    # Check book showed up
    expect(page.get_by_role("cell", name="My Book")).to_be_visible()

    # Borrow the book
    page.get_by_role("row", name="5 My Book Me 1122334455667").get_by_placeholder("Patron ID").click()
    page.get_by_role("row", name="5 My Book Me 1122334455667").get_by_placeholder("Patron ID").fill("789000")
    page.get_by_role("cell", name="789000 Borrow").get_by_role("button").click()

    # Check book was borrowed
    expect(page.get_by_text("Successfully borrowed \"My")).to_be_visible()
    

def test_borrow_return_book(page : Page):
    #Open page
    page.goto("http://localhost:5000/catalog")
    
    # Borrow the book
    page.get_by_role("row", name="3 1984 George Orwell").get_by_placeholder("Patron ID (6 digits)").click()
    page.get_by_role("row", name="3 1984 George Orwell").get_by_placeholder("Patron ID (6 digits)").fill("456789")
    page.get_by_role("cell", name="456789 Borrow").get_by_role("button").click()

    # Check book was borrowed
    expect(page.get_by_text("Successfully borrowed \"1984")).to_be_visible()

    # Return the book
    page.get_by_role("link", name="↩️ Return Book").click()
    page.get_by_role("textbox", name="Patron ID *").click()
    page.get_by_role("textbox", name="Patron ID *").fill("456789")
    page.get_by_role("spinbutton", name="Book ID *").click()
    page.get_by_role("spinbutton", name="Book ID *").fill("3")
    page.get_by_role("button", name="Process Return").click()

    # check book was returned
    expect(page.get_by_text("Book successfully returned.")).to_be_visible()


