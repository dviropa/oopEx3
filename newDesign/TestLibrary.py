import unittest
import pandas as pd
import os
import json
from Library import Library
from User import User
from Book import Book

class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # יצירת קבצי CSV דמה לבדיקות
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

    @classmethod
    def tearDownClass(cls):
        # מחיקת קבצי CSV לאחר הבדיקות
        os.remove(cls.books_csv)
        os.remove(cls.available_books_csv)
        os.remove(cls.loaned_books_csv)
        os.remove(cls.wait_list_csv)

    def setUp(self):
        self.library = Library()

    def test_add_book(self):
        self.library.add_book("Book4", "Author4", 2023, "Fiction")
        self.assertTrue("Book4" in self.library.lib_books)
    def test_loan_book(self):
        user = User(456, "TestUser")
        self.library.loan_book("Book1", user)
        self.assertEqual(self.library.lib_books["Book1"]["sum_borowd_amunt"], 11)
        self.assertTrue(
            any([v == {True: user} for v in self.library.lib_books["Book1"]["is_loaned"].values()])
        )

    def test_return_book(self):
        user = User(123, "User1")
        self.library.return_book("Book2", user)
        self.assertEqual(self.library.lib_books["Book2"]["sum_borowd_amunt"], 4)

    def test_add_book_copy(self):
        self.library.add_book_copy("Book1")
        self.assertEqual(len(self.library.lib_books["Book1"]["is_loaned"]), 3)

    def test_remove_book_copy(self):
        self.library.remove_book_copy("Book1")
        self.assertEqual(len(self.library.lib_books["Book1"]["is_loaned"]), 1)

if __name__ == '__main__':
    unittest.main()


