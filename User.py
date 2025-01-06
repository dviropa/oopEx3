import hashlib
import pandas as pd
import json


class User:
    def __init__(self, name, password):
        self.__name = name
        self.__password = password

        # מקבל את הערך המקסימלי ומוסיף 1 ליצירת ID חדש
        self.__id = self.__get_max_id() + 1
        self.__add()  # קריאה למתודה להוספת משתמש
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id
    def __get_max_id(self, default=1110):
        filename = "users.csv"

        try:
            users_df = pd.read_csv(filename, dtype={"id": int, "name": str, "password": str, "my_books": str})
            if not users_df.empty and "id" in users_df.columns:
                return users_df["id"].max()
            else:
                return default
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return default

    def __add(self):
        filename = "users.csv"

        try:
            users_df = pd.read_csv(filename, dtype={"id": int, "name": str, "password": str, "my_books": str})
        except (FileNotFoundError, pd.errors.EmptyDataError):
            users_df = pd.DataFrame(columns=["id", "name", "password", "my_books"])

        encrypted_password = hashlib.sha256(self.__password.encode()).hexdigest()

        if not users_df.empty and self.__id in users_df["id"].values:
            users_df.loc[users_df["id"] == self.__id, "password"] = encrypted_password
        else:
            new_user = {
                "id": self.__id,
                "name": self.__name,
                "password": encrypted_password,
                "my_books": json.dumps({})
            }
            users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)

        users_df.to_csv(filename, index=False)
        print(f"User {self.__name} added/updated successfully.")

    def borrow_book(self, book_title):
        filename = "users.csv"

        try:
            users_df = pd.read_csv(filename, dtype={"id": int, "name": str, "password": str, "my_books": str})
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print("Users file not found or empty.")
            return False

        user_row = users_df.loc[users_df["id"] == self.__id]
        if user_row.empty:
            print("User not found.")
            return False

        my_books = json.loads(user_row["my_books"].values[0])

        # בדיקה אם ניתן להשאיל את הספר
        if book_title in my_books and my_books[book_title] > 0:
            my_books[book_title] -= 1
            print(f"Book '{book_title}' borrowed successfully by {self.__name}.")
            if my_books[book_title] == 0:
                del my_books[book_title]  # מסיר את הספר אם אין עותקים זמינים
        else:
            print(f"Cannot borrow '{book_title}': not available.")
            return False

        # עדכון הקובץ
        users_df.loc[users_df["id"] == self.__id, "my_books"] = json.dumps(my_books)
        users_df.to_csv(filename, index=False)
        return True

    def return_book(self, book_title):
        filename = "users.csv"

        try:
            users_df = pd.read_csv(filename, dtype={"id": int, "name": str, "password": str, "my_books": str})
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print("Users file not found or empty.")
            return False

        user_row = users_df.loc[users_df["id"] == self.__id]
        if user_row.empty:
            print("User not found.")
            return False

        my_books = json.loads(user_row["my_books"].values[0])

        # החזרת הספר
        if book_title in my_books:
            my_books[book_title] += 1
        else:
            my_books[book_title] = 1

        print(f"Book '{book_title}' returned successfully by {self.__name}.")

        # עדכון הקובץ
        users_df.loc[users_df["id"] == self.__id, "my_books"] = json.dumps(my_books)
        users_df.to_csv(filename, index=False)
        return True


# יצירת אובייקטים ודוגמאות לשימוש
user1 = User("Alice", "password123")
user1.add_to_my_books("The Hobbit")
user1.add_to_my_books("1984")

# השאלה של ספר
if user1.borrow_book("The Hobbit"):
    print("Borrowed successfully!")
else:
    print("Failed to borrow the book.")

# החזרה של ספר
if user1.return_book("The Hobbit"):
    print("Returned successfully!")
else:
    print("Failed to return the book.")
