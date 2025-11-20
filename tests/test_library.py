# Basic unit tests for LibraryInventory and Book using CSV storage.
import unittest
from pathlib import Path
import tempfile
import os

from library_manager.book import Book
from library_manager.inventory import LibraryInventory

class TestLibraryInventory(unittest.TestCase):

    def setUp(self):
        # create a temp file for CSV storage
        fd, self.tmpfile = tempfile.mkstemp(text=True)
        os.close(fd)    # <-- VERY IMPORTANT FIX
        Path(self.tmpfile).write_text("title,author,isbn,status\n", encoding="utf-8")
        self.inv = LibraryInventory(storage_path=self.tmpfile)

    def tearDown(self):
        Path(self.tmpfile).unlink(missing_ok=True)

    def test_add_and_search(self):
        b = Book("A Tale", "Author", "ISBN123")
        self.inv.add_book(b)
        self.assertIsNotNone(self.inv.search_by_isbn("ISBN123"))

    def test_duplicate_isbn(self):
        b1 = Book("One", "A", "DUP1")
        b2 = Book("Two", "B", "DUP1")
        self.inv.add_book(b1)
        with self.assertRaises(ValueError):
            self.inv.add_book(b2)

    def test_issue_and_return(self):
        b = Book("IssueTest", "Author", "ISS1")
        self.inv.add_book(b)
        self.assertTrue(self.inv.issue_book("ISS1"))
        self.assertFalse(self.inv.issue_book("ISS1"))  # already issued
        self.assertTrue(self.inv.return_book("ISS1"))

if __name__ == "__main__":
    unittest.main()
