# Book model for the library inventory
from typing import Dict

class Book:

    def __init__(self, title: str, author: str, isbn: str, status: str = "available"):
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.status = status

    def __str__(self) -> str:
        return f"{self.title} — {self.author} (ISBN: {self.isbn}) [{self.status}]"

    def to_dict(self) -> Dict[str, str]:
        """Return a dict representation of the book."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        """Create a Book from a dictionary-like mapping."""
        return cls(
            title=data.get("title", ""),
            author=data.get("author", ""),
            isbn=data.get("isbn", ""),
            status=data.get("status", "available"),
        )

    def is_available(self) -> bool:
        return self.status == "available"

    def issue(self) -> bool:
        """Mark the book as issued. Returns True if successful, False if already issued."""
        if not self.is_available():
            return False
        self.status = "issued"
        return True

    def return_book(self) -> bool:
        """Mark the book as available. Returns True if state changed."""
        if self.is_available():
            return False
        self.status = "available"
        return True
