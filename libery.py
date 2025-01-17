import json
from queue import Queue
import pandas as pd
from books import Book as book
from books.Book import BookFactory


class Library:
    def __init__(self, books_file="books.csv", available_books_file="available_books.csv",
                 borrowed_books_file="borrowed_books.csv"):
        self.books_file = books_file
        self.available_books_file = available_books_file
        self.borrowed_books_file = borrowed_books_file

    def __load_csv(self, filename= "books.csv"):
        """Load a CSV file or create a new one if not found."""
        try:
            return pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame()

    def __save_csv(self, df, filename):
        """Save a DataFrame to a CSV file."""
        df.to_csv(filename, index=False)

    def book_exists(self, title):
        """Check if a book exists in the library."""
        # books_df = self.__load_csv(self.books_file,
        #                            ["title", "author", "year", "category", "copies", "borrowed_copies"])
        books_df=self.__load_csv(self.books_file)
        return (books_df["title"] == title).any()

    def add_book(self, book):
        """Add a new book to the library or update copies if it exists."""
        # books_df = self.__load_csv(self.books_file,
        #                            ["title", "author", "year", "category", "copies", "borrowed_copies"])
        books_df=self.__load_csv(self.books_file)
        if self.book_exists(book.get_title()):
            #books_df.loc[books_df["title"] == book.get_title(), "copies"] += book.get_copies()
            BookFactory.add_copy(book.get_title())
            print(f"Updated copies for '{book.get_title()}'.")
        else:
            new_book = {
                "title": book.get_title(),
                "author": book.get_author(),
                "year": book.get_year(),
                "category": book.get_category(),
                "copies": book.get_copies(),
                "borrowed_copies": 0
            }

            #books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
            BookFactory.add_book(book)
            print(f"Added new book: '{book.get_title()}'.")
        self.__save_csv(books_df, self.books_file)



    def add_to_waiting_list(self, book, user):#לטפל אחרכך
        if self.book_exists(book.get_title()):
            if book.get_name() in self.waiting_list_of_popular_books:
                self.waiting_list_of_popular_books[book.get_name()].add(user.get_id())
            else:
                self.waiting_list_of_popular_books[book.get_name()] = {user.get_id()}
        else:
            print(f"Book '{book.get_name()}' not in library.")

    def borrow_book(self, book, user):
        """
        Handles the process of borrowing a book for a user.
        """
        sirial_number=BookFactory.borrow_book(book.get)
        if sirial_number is not None:
            if user.borrow_book(book.get_name(), sirial_number):
                self.add_to_borrow_book_file(book.get_name(), sirial_number)
                self.remov_from_avaikacle_book_file(book.get_name(), sirial_number)
                print(
                    f"Book '{book.get_name()}' (Serial Number: {sirial_number}) successfully borrowed by {user.get_name()}.")
            else:
                print(f"Book '{book.get_name()}' (Serial Number: {sirial_number}) returned due to user issue.")
                BookFactory.return_book(sirial_number,book.get_name())
        else:
            print(f"No available copies of '{book.get_name()}' to borrow.")
    def return_borrow_book(self, book, user):
        check, sirial_number = user.remove_books(book.get_name())
        if check:
            book.return_book(sirial_number,book.get_name)
            # לשנות את זה
            self.remov_from_borrow_book_file(book.get_name(), sirial_number)
            self.add_to_borrow_book_file(book.get_name(), sirial_number)

    def add_copy(self, title):
        BookFactory.add_copy_to_existing_book(title)

    def add_new_book(self, book):
        BookFactory.add_book(book)

    def remov_from_borrow_book_file(self, name, serial_number):
        try:
            books_df=self.__load_csv(self.borrowed_books_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print(f"File  not found or is empty.")
            return

        # Find the book in the file
        book_row = books_df[books_df["name"] == name]
        if book_row.empty:
            print("Book not found in the file.")
            return

        self.__num_of_borrowed_copies += 1
        books_df.loc[books_df["name"] == self.__name, "num_of_borrowed_copies"] = self.__num_of_borrowed_copies
        books_df.loc[books_df["name"] == self.__name, "borrow_book"] = json.dumps(self.__is_loaned)
        self.__save_csv(books_df, self.available_books_file)
        # books_df.to_csv(filename, index=False)
        print()

    def add_to_borrow_book_file(self, name, serial_number):
        try:
            books_df = self.__load_csv(self.borrowed_books_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # אם הקובץ לא קיים או ריק, יוצרים DataFrame חדש
            books_df = pd.DataFrame(columns=["name", "borrowed_serials"])

        # Find the book in the file
        book_row = books_df[books_df["name"] == name]

        if book_row.empty:
            # אם הספר לא נמצא, נוסיף רשומה חדשה
            new_entry = {
                "name": name,
                "borrowed_serials": json.dumps([serial_number])  # יוצרים רשימה חדשה עם המספר הסידורי
            }
            books_df = pd.concat([books_df, pd.DataFrame([new_entry])], ignore_index=True)
        else:
            # אם הספר קיים, נוסיף את המספר הסידורי לרשימה הקיימת
            borrowed_books = json.loads(
                book_row.iloc[0]["borrowed_serials"]) if "borrowed_serials" in book_row.columns else []

            if serial_number in borrowed_books:
                print(f"Serial number {serial_number} already exists in the borrowed list for book '{name}'.")
                return

            borrowed_books.append(serial_number)
            books_df.loc[books_df["name"] == name, "borrowed_serials"] = json.dumps(borrowed_books)

        # Save the updated DataFrame back to the file
        self.__save_csv(books_df, self.borrowed_books_file)
        print(f"Serial number {serial_number} added to the borrowed list for book '{name}'.")

    def remov_from_avaikacle_book_file(self, name, serial_number):
        filename = "avaikacle_books.csv"
        try:
            books_df = self.__load_csv(self.available_books_file)

        except (FileNotFoundError, pd.errors.EmptyDataError):
            print(f"File '{filename}' not found or is empty.")
            return

        # Find the book in the file
        book_row = books_df[books_df["name"] == name]
        if book_row.empty:
            print("Book not found in the file.")
            return

        self.__num_of_borrowed_copies += 1
        books_df.loc[books_df["name"] == self.__name, "num_of_borrowed_copies"] = self.__num_of_borrowed_copies
        books_df.loc[books_df["name"] == self.__name, "borrow_book"] = json.dumps(self.__is_loaned)
        books_df.to_csv(filename, index=False)
        print()

    def add_to_avaikacle_book_file(self, name, serial_number):
        """
        Adds a specific serial number to the borrowed book list in the file 'loaned_books.csv'.
        """
        try:
            books_df = self.__load_csv(self.available_books_file)

        except (FileNotFoundError, pd.errors.EmptyDataError):
            # אם הקובץ לא קיים או ריק, יוצרים DataFrame חדש
            books_df = pd.DataFrame(columns=["name", "borrowed_serials"])

        # Find the book in the file
        book_row = books_df[books_df["name"] == name]

        if book_row.empty:
            # אם הספר לא נמצא, נוסיף רשומה חדשה
            new_entry = {
                "name": name,
                "borrowed_serials": json.dumps([serial_number])  # יוצרים רשימה חדשה עם המספר הסידורי
            }
            books_df = pd.concat([books_df, pd.DataFrame([new_entry])], ignore_index=True)
        else:
            # אם הספר קיים, נוסיף את המספר הסידורי לרשימה הקיימת
            borrowed_books = json.loads(
                book_row.iloc[0]["borrowed_serials"]) if "borrowed_serials" in book_row.columns else []

            if serial_number in borrowed_books:
                print(f"Serial number {serial_number} already exists in the borrowed list for book '{name}'.")
                return

            borrowed_books.append(serial_number)
            books_df.loc[books_df["name"] == name, "borrowed_serials"] = json.dumps(borrowed_books)

        # Save the updated DataFrame back to the file
        self.__save_csv(books_df, self.available_books_file)
        # books_df.to_csv(filename, index=False)
        print(f"Serial number {serial_number} added to the borrowed list for book '{name}'.")
    def get_available_books(self):  # מילון של כל ספר וכמות הספרים שניתן לקחת
        try:
            avaliable_books_df = self.__load_csv(self.available_books_file)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            avaliable_books_df = pd.DataFrame(columns=["name", "borrowed_serials"])

        books = avaliable_books_df.set_index("name")[len(["borrowed_serials"])].to_dict()
        return books

    def get_borrowed_books(self):
        try:
            loaned_books_df = pd.read_csv("loaned_books.csv")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            loaned_books_df = pd.DataFrame(columns=["name", "borrowed_serials"])
        borrowed_books = loaned_books_df.set_index("name")[len(["borrowed_serials"])].to_dict()
        return borrowed_books

    # def get_clint(self):
    #     try:
    #         client_df = pd.read_csv("client.csv", dtype={"id": int, "name": str, "my_books": str, "notifications": str})
    #     except (FileNotFoundError, pd.errors.EmptyDataError):
    #         client_df = pd.DataFrame(columns=["id", "name", "my_books", "notifications"])
    #     return client_df.set_index("name")

    def get_users(self):
        try:
            users_df = pd.read_csv("users.csv",)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            users_df = pd.DataFrame(columns=["id", "name", "password", "level"])
        return users_df.set_index("name")["password"].to_dict()