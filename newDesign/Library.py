from Book import Book
import pandas as pd
from Observable import Observable
from Authinactor import Authinactor
from User import User
from log import Log
import json


class Library(Observable):

    def __init__(self):
        super().__init__()
        self.lib_books: dict = {}
        self.wait_list: dict = {}
        auth_system: Authinactor = Authinactor()
        self.logger = Log()
        self.load_books_from_csv()

    def load_books_from_csv(self):
        # טעינת קובצי CSV
        books_df = pd.read_csv("books.csv",
            dtype={"title": str, "author": str, "year": int, "category": str, "sum_borowd_amunt": int})
        books_df["is_loaned"] = books_df["is_loaned"].apply(json.loads)

        available_df = pd.read_csv("available_books.csv", dtype={"title": str, "copies": int})
        loaned_df = pd.read_csv("loaned_books.csv", dtype={"title": str, "copies": int})
        wait_list_df = pd.read_csv("wait_list.csv", dtype={"title": str})

        wait_list_df["user_id"] = wait_list_df["user_id"].apply(json.loads)

        # אתחול lib_books
        for _, row in books_df.iterrows():
            book = Book(row["title"], row["author"], row["year"], row["category"], row["copies"])
            self.lib_books[row["title"]] = (book, row["sum_borowd_amunt"], row["is_loaned"])

        # אתחול wait_list
        for _, row in wait_list_df.iterrows():
            if row["title"] not in self.wait_list:
                self.wait_list[row["title"]] = []
            self.wait_list[row["title"]].append(User(row["user_id"]))



    def __update_books_csv(self, titel, filename="books.csv"):
        df = self.__load_csv(filename)
        # dict{titel,(book,sum_borowd_amunt,dict{book_id,(bool,user)})}
        # book,sum_borowd_amunt,dict{book_id,(bool,user)}
        is_loaned_data = json.dumps(self.lib_books[titel][2])
        df.loc[df["titel"] == titel, "is_loaned"] = is_loaned_data
        df.to_csv(filename, index=False)

    def __update_available_csv(self, titel, amount, filename="available_books.csv"):
        df = self.__load_csv(filename)

        if titel in df["titel"].values:
            df.loc[df["titel"] == titel, "amount"] += amount
        else:
            new_row = {"titel": titel, "amount": 1}
            df = df.append(new_row, ignore_index=True)

        df.to_csv(filename, index=False)

    def __update_loaned_csv(self, titel, amount, filename="loaned_books.csv"):
        df = self.__load_csv(filename)

        if titel in df["titel"].values:
            df.loc[df["titel"] == titel, "amount"] += amount
        else:
            new_row = {"titel": titel, "amount": 1}
            df = df.append(new_row, ignore_index=True)

        df.to_csv(filename, index=False)

    def __update_waiting_list_csv(self, titel, user: User, filename="wait_list.csv"):
        df = self.__load_csv(filename)
        #
        # if titel in df["titel"].values:
        #     df.loc[df["titel"] == titel, "user"]+=user
        # else:
        #     new_row = {"titel": titel, "amount": 1}
        #     df = df.append(new_row, ignore_index=True)
        #
        # df.to_csv(filename, index=False)
    def __load_csv(self, filename):
        """Load a CSV file or create a new one if not found."""
        try:
            return pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.logger.log(f"not abele to open {filename}")
            return pd.DataFrame()
    def add_exsisting_book(self, book: Book, dict: dict):
        # לוקחים מהcsv את הערכים למילון כלומר
        # dict{titel,(book,sum_borowd_amunt,dict{book_id,(bool,user)})}
        self.lib_books[book.get_title()] = dict

    def top10_popular_books(self):
        books_df = pd.read_csv("books.csv")

        books_df = books_df.sort_values(by="sum_borowd_amunt", ascending=False).head(10)
        popular_titles = books_df["titel"].tolist()
        return popular_titles
    def get_books_in_waiting_list(self):
        wait_list_titles = []
        if hasattr(self, "wait_list") and isinstance(self.wait_list, dict):
            wait_list_titles = list(self.wait_list.keys())
        return wait_list_titles
    def top10_and_waiting_list(self):
        combined_titles = self.top10_popular_books() + [title for title in self.get_books_in_waiting_list() if title not in self.top10_popular_books()]
        return combined_titles

    def add_book(self, title, author, year, category, copies=1):

        if title in self.lib_books:
            book = self.lib_books[title][0]

            assert book.get_author() == author, "book added fail, Author mismatch"
            assert book.get_year() == year, "book added fail, Year mismatch"
            assert book.get_categories() == category, "book added fail, Category mismatch"

            while copies-1 > 1:
                copies-=1
                self.add_book_copy(title)
            self.add_book_copy(title)
        else:
            book = Book(title, author, year, category)
            self.lib_books[title] = (
            book, 0, {i: {False: None} for i in range(copies)})  # book and empty dictionary for borrowed books
            self.logger.log(f"a new book {title} has been added")
            # self.notify(f"book added successfully")
            # עדכון קובץ ספרים וספרים פנויים
        self.__update_books_csv(title)
        self.__update_available_csv(title, 1)

    def remove_books(self, title):
        # if book is not borrowd
        if not self.is_book_valid(title):
            self.logger.log(f"book removed fail")

        try:
            num_copis = len(self.lib_books[title][1][1])
            for i in range(len(self.lib_books[title][1][1])):
                num_copis -= 1
                self.remove_book_copy(title)
            if num_copis == 0:
                self.logger.log(f"book removed successfully")
            else:
                self.logger.log(f"book removed fail")

        except RuntimeError:
            return False

    def remove_book_copy(self, title):
        index = self.first_available_copy(title)

        if index is not None:
            del self.lib_books[title][1][1][index]
            self.logger.log(f"removing one copy of {title} copy number {index} successfully ")

            # עדכון קובץ ספרים וספרים פנויים
            self.__update_books_csv(title)
            self.__update_available_csv(title, -1)

        else:
            self.logger.log("Eror: No available copies")
            raise RuntimeError("No available copies to remove")

    def add_book_copy(self, title):
        index = len(self.lib_books[title][1][1]) + 1
        self.lib_books[title][1][1][index] = {False: None}
        self.logger.log(f"aded a new copy of {title}  copy number {index}")

        # עדכון קובץ ספרים וספרים פנויים
        self.__update_books_csv(title)
        self.__update_available_csv(title, 1)

    def loan_book(self, title, user: User):
        try:
            index = self.first_available_copy(title)
            if index is None:
                if not user in self.wait_list[title]:
                    self.wait_list[title].append(user)
                    self.logger.log(f"add user :{user.get_name()} to  {title} witing list")
                    # עדקון קובץ רשימת המתנה
                    self.__update_waiting_list_csv()
                self.logger.log(f"book borrowed fail - there are no available copy")
                return False

            self.lib_books[title][1][1][index] = {True: user}
            self.lib_books[title][1][0] = self.lib_books[title][1][0] + 1
            self.logger.log(f"book borrowed successfully - user :{user.get_name()} lownd {title}")
            # עדכון קובץ ספרים וספרים פנויים וספרים מושאלים
            self.__update_books_csv(title)
            self.__update_available_csv(title, -1)
            self.__update_loaned_csv(title, 1)

            if user in self.wait_list[title]:
                self.logger.log(f" removing user :{user.get_name()} from waiting list ")
                self.wait_list[title].remove(user)

            return True

        except ValueError as e:
            print(e.args[0])
            return False

    def return_book(self, title, user: User):
        try:
            index = self.user_borrowed_book(title, user)
            if index is None:
                raise ValueError("book returned fail - User has not borrowed this book")
            self.logger.log(f"book returned successfully - user:{user.get_name()} returned {title} ")
            self.lib_books[title][1][1][index] = {False: None}
            # עדכון קובץ ספרים וספרים פנויים וספרים מושאלים
            self.__update_books_csv(title)
            self.__update_available_csv(title, 1)
            self.__update_loaned_csv(title, -1)

            if self.wait_list[title]:
                # self.loan_book(title, self.wait_list[title].pop(0))
                self.logger.log(f" nowtify all whiting list of{title} that the book is avalibol")
                for client in self.wait_list[title]:
                    client.update(f"Book {title} is available now")

            return True



        except ValueError as e:
            print(e.args[0])
            return False

    def first_available_copy(self, title):
        if title not in self.lib_books:
            raise ValueError("Book not found")
        for i in range(len(self.lib_books[title][1][1])):
            if not self.lib_books[title][1][1][i]:
                return i
        return None

    def update_book(self, title, new_title, author, year, category):
        self.logger.log(f"abdate {title}")
        # עדכון קובץ ספרים וספרים פנויים וספרים מושאלים

    def register_new_user(self, user: User, password):
        try:
            self.auth_system.register(user.get_id(),user.get_name(), password)
            self.logger.log(f"register new user:{user.get_name()} ")
        except ValueError as e:
            print(e.args[0])

    def user_login(self, user: User, password):
        if self.auth_system.login(user.get_id(), password):
            self.logger.log(f"user:{user.get_name()} login")
            return True

        else:
            self.logger.log(f"user:{user.get_name()}failde to login")
            return False

    def user_logout(self, user: User):
        if self.auth_system.logout(user.get_id()):
            self.logger.log(f"user:{user.get_name()} logout")
        else:
            self.logger.log(f"user:{user.get_name()}failde to logout")

    def is_book_valid(self, title):
        if title in self.lib_books:
            return True

        return False

    def user_borrowed_book(self, title, user: User):
        if not self.is_book_valid(title):
            raise ValueError("Book not found")

        for i in range(len(self.lib_books[title][1][1])):
            if self.lib_books[title][1][1][i] == {True: user}:
                return i

        return None
