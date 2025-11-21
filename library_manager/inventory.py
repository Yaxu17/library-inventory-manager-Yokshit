# LibraryInventory: manages a collection of Book objects with CSV persistence.
import csv
import logging
from pathlib import Path
from typing import List, Optional, Dict

from .book import Book

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class LibraryInventory:
    """Manages a list of Book objects and persists them to a CSV file."""

    FIELDNAMES = ["title","author","isbn","status"]

    def __init__(self, storage_path: Optional[str] = None):
        # default storage path
        self.storage_path = Path(storage_path) if storage_path else Path("data/catalog.csv")
        self.books: List[Book] = []
        self._ensure_data_dir()
        self.load()

    def _ensure_data_dir(self):
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        # ensure file exists and has header
        if not self.storage_path.exists():
            try:
                with self.storage_path.open("w", encoding="utf-8", newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                    writer.writeheader()
            except Exception as e:
                logger.error("Could not create storage file: %s", e)

    def add_book(self, book: Book) -> None:
        """Add a book to the inventory. Raises ValueError on duplicate ISBN."""
        if self.search_by_isbn(book.isbn):
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        logger.info("Book added: %s", book)
        self.save()

    def search_by_title(self, title_query: str) -> List[Book]:
        q = title_query.strip().lower()
        return [b for b in self.books if q in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        isbn_q = isbn.strip()
        for b in self.books:
            if b.isbn == isbn_q:
                return b
        return None

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            return False
        if not book.issue():
            return False
        logger.info("Book issued: %s", book)
        self.save()
        return True

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            return False
        if not book.return_book():
            return False
        logger.info("Book returned: %s", book)
        self.save()
        return True
    
    def remove_book(self, isbn: str) -> bool:
        """Remove a book by ISBN. Returns True if removed, False if not found."""
        book = self.search_by_isbn(isbn)
        if not book:
            return False
        try:
            self.books.remove(book)
            logger.info("Book removed: %s", book)
            self.save()
            return True
        except ValueError:
            return False


    def save(self) -> None:
        """Persist the catalog to CSV. Robustly handles file errors."""
        try:
            with self.storage_path.open("w", encoding="utf-8", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                for b in self.books:
                    writer.writerow(b.to_dict())
        except Exception as e:
            logger.error("Failed to save catalog: %s", e)
            raise

    def load(self) -> None:
        """Load the catalog from CSV; handles missing/corrupt files."""
        if not self.storage_path.exists():
            # No file, start with empty catalog
            self.books = []
            return
        try:
            with self.storage_path.open("r", encoding="utf-8", newline='') as f:
                reader = csv.DictReader(f)
                items = [row for row in reader if row and row.get('isbn')]
            self.books = [Book.from_dict(item) for item in items]
        except Exception as e:
            logger.error("Error loading catalog, starting with empty: %s", e)
            self.books = []
