from queue import Queue

import pandas as pd


class Library:
    def __init__(self, books=None):
        self.books = books if books else []
        self.available_books = {}
        self.borrowed_books = {}
        self.waiting_list_of_popular_books = {}

    def add_book(self, book):
        self.__add()


    def get_available_books(self):#מילון של כל ספר וכמות הספרים שניתן לקחת
        self.available_books = {book.get_name(): book.get_num_of_available_copies() for book in self.books}
        return self.available_books

    def get_borrowed_books(self):
        self.borrowed_books = {book.get_name(): book.get_num_of_borrowed_copies() for book in self.books}
        return self.borrowed_books

    def add_to_waiting_list(self, book, user):
        if book in self.books:
            if book.get_name() in self.waiting_list_of_popular_books:
                self.waiting_list_of_popular_books[book.get_name()].add(user.get_id())
            else:
                self.waiting_list_of_popular_books[book.get_name()] = {user.get_id()}
        else:
            print(f"Book '{book.get_name()}' not in library. Adding it...")
            self.add_book(book)
            self.add_to_waiting_list(book, user.get_id())

    def borrow_book(self, book, user):
        if user.add_to_my_books(book.get_name()):
            book.borrow_book()
    def return_borrow_book(self, book, user):
        if user.remove_book(book.get_name()):
            book.return_book()




    def __add(self):
        filename = "books.csv"

        try:
            # קריאת קובץ ה-CSV
            books_df = pd.read_csv(filename, dtype={
                "title": str,
                "author": str,
                "is_loaned": bool,
                "copies": int,
                "genre": str,
                "year": int
            })
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # יצירת DataFrame חדש אם הקובץ לא קיים או ריק
            books_df = pd.DataFrame(columns=["title", "author", "is_loaned", "copies", "genre", "year"])

        # בדיקת קיום הספר לפי title ו-author
        book_exists = (books_df["title"] == self.title) & (books_df["author"] == self.author)

        if book_exists.any():
            # עדכון עמודת 'copies' אם הספר קיים
            books_df.loc[book_exists, "copies"] += self.copies
            print(f"Updated copies for '{self.title}' by {self.author}.")
        else:
            # הוספת ספר חדש אם הוא לא קיים
            new_book = {
                "title": self.title,
                "author": self.author,
                "is_loaned": self.is_loaned,
                "copies": self.copies,
                "genre": self.genre,
                "year": self.year
            }
            books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
            print(f"Added new book: '{self.title}' by {self.author}.")

        # שמירת העדכונים לקובץ
        books_df.to_csv(filename, index=False)
        print("Books database updated successfully.")