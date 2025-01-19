import unittest
import os
import pandas as pd
import json
from Library import Library
from User import User
from Book import Book


class TestLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # יצירת קבצי CSV לדוגמה
        cls.books_csv = "books.csv"
        cls.available_books_csv = "available_books.csv"
        cls.loaned_books_csv = "loaned_books.csv"
        cls.wait_list_csv = "wait_list.csv"

        pd.DataFrame({
            "title": ["Book1", "Book2", "Book3"],
            "author": ["Author1", "Author2", "Author3"],
            "year": [2020, 2021, 2022],
            "category": ["Fiction", "Sci-Fi", "Fantasy"],
            "sum_borowd_amunt": [10, 5, 7],
            "is_loaned": [
                json.dumps({1: True, 2: False}),
                json.dumps({1: True}),
                json.dumps({1: True, 2: False, 3: True})
            ]
        }).to_csv(cls.books_csv, index=False)

        pd.DataFrame({
            "title": ["Book1", "Book3"],
            "copies": [2, 3]
        }).to_csv(cls.available_books_csv, index=False)

        pd.DataFrame({
            "title": ["Book2"],
            "copies": 1,
            "user_id": 123
        }).to_csv(cls.loaned_books_csv, index=False)

        pd.DataFrame({
            "title": ["Book1"],
            "user_id": [json.dumps(456)]
        }).to_csv(cls.wait_list_csv, index=False)

    @classmethod
    def tearDownClass(cls):
        # מחיקת קבצי CSV לאחר הבדיקות
        os.remove(cls.books_csv)
        os.remove(cls.available_books_csv)
        os.remove(cls.loaned_books_csv)
        os.remove(cls.wait_list_csv)

    def setUp(self):
        self.library = Library()

    def test_load_books_from_csv(self):
        self.assertEqual(len(self.library.lib_books), 3)
        self.assertIn("Book1", self.library.lib_books)

    def test_add_book(self):
        self.library.add_book("Book4", "Author4", 2023, "Drama", 1)
        self.assertIn("Book4", self.library.lib_books)

    def test_remove_book_copy(self):
        initial_copies = len(self.library.lib_books["Book1"][2])
        self.library.remove_book_copy("Book1")
        updated_copies = len(self.library.lib_books["Book1"][2])
        self.assertEqual(updated_copies, initial_copies - 1)

    def test_add_book_copy(self):
        initial_copies = len(self.library.lib_books["Book1"][2])
        self.library.add_book_copy("Book1")
        updated_copies = len(self.library.lib_books["Book1"][2])
        self.assertEqual(updated_copies, initial_copies + 1)

    def test_loan_book(self):
        user = User(123, "TestUser")
        result = self.library.loan_book("Book1", user)
        self.assertTrue(result)
        self.assertIn(user, self.library.wait_list.get("Book1", []))

    def test_return_book(self):
        user = User(123, "TestUser")
        self.library.loan_book("Book1", user)
        result = self.library.return_book("Book1", user)
        self.assertTrue(result)

    def test_update_book(self):
        self.library.update_book("Book1", "UpdatedBook1", "NewAuthor", 2025, "Drama")
        self.assertIn("UpdatedBook1", self.library.lib_books)
        updated_book = self.library.lib_books["UpdatedBook1"][0]
        self.assertEqual(updated_book.author, "NewAuthor")
        self.assertEqual(updated_book.year, 2025)
        self.assertEqual(updated_book.category, "Drama")

    def test_update_waiting_list_csv(self):
        user = User(789, "NewUser")
        self.library.wait_list["Book1"] = [user]
        self.library.__update_waiting_list_csv("Book1")
        df = pd.read_csv(self.wait_list_csv)
        self.assertIn(789, json.loads(df.loc[df["title"] == "Book1", "user_id"].values[0]))

    def test_is_book_valid(self):
        self.assertTrue(self.library.is_book_valid("Book1"))
        self.assertFalse(self.library.is_book_valid("NonExistentBook"))


if __name__ == "__main__":
    unittest.main()
