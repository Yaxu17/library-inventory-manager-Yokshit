# Command-line interface for the Library Inventory Manager.

import logging
import sys
from library_manager.inventory import LibraryInventory
from library_manager.book import Book

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def prompt(msg: str) -> str:
    return input(msg).strip()

def menu() -> None:
    inv = LibraryInventory()

    while True:
        print("\n=== Library Inventory Manager ===")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search by Title")
        print("6. Search by ISBN")
        print("7. Exit")

        choice = prompt("Choose an option (1-7): ")
        if choice == "1":
            try:
                title = prompt("Title: ")
                author = prompt("Author: ")
                isbn = prompt("ISBN: ")
                if not (title and author and isbn):
                    print("All fields are required.")
                    continue
                book = Book(title=title, author=author, isbn=isbn)
                inv.add_book(book)
                print("Book added successfully.")
            except ValueError as e:
                print("Error:", e)
            except Exception:
                logger.exception("Unexpected error while adding a book.")
                print("An unexpected error occurred.")

        elif choice == "2":
            isbn = prompt("ISBN to issue: ")
            if not isbn:
                print("ISBN required.")
                continue
            if inv.issue_book(isbn):
                print("Book issued successfully.")
            else:
                print("Failed to issue book — check ISBN or availability.")

        elif choice == "3":
            isbn = prompt("ISBN to return: ")
            if not isbn:
                print("ISBN required.")
                continue
            if inv.return_book(isbn):
                print("Book returned successfully.")
            else:
                print("Failed to return book — check ISBN or status.")

        elif choice == "4":
            books = inv.display_all()
            if not books:
                print("No books in catalog.")
            else:
                print("\nCatalog:")
                for line in books:
                    print(" - ", line)

        elif choice == "5":
            q = prompt("Search title: ")
            results = inv.search_by_title(q)
            if not results:
                print("No matches found.")
            else:
                for b in results:
                    print(b)

        elif choice == "6":
            isbn = prompt("Search ISBN: ")
            book = inv.search_by_isbn(isbn)
            if not book:
                print("Not found.")
            else:
                print(book)

        elif choice == "7":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Enter a number between 1 and 7.")

if __name__ == "__main__":
    menu()
