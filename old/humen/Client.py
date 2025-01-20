import json

import pandas as pd

# from humen import  Person
from old.humen.Person import Person


class Client(Person):

    def __init__(self, name, id=None):
        super().__init__(name)  # קריאה לבנאי של Person
        self.__my_books = {}
        self.id = id if id is not None else super().get_id()  # הגדרה נכונה של self.id
        self.__add()  # הוספת הלקוח למסד הנתונים
        self.__filename = "client.csv"

    def __add(self):
        filename = "client.csv"

        try:
            # Load the existing clients data
            clients_df = pd.read_csv(filename, dtype={"id": int, "name": str, "my_books": str, "notifications": str})
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # Initialize a new DataFrame if the file doesn't exist or is empty
            clients_df = pd.DataFrame(columns=["id", "name", "my_books", "notifications"])

        if not clients_df.empty and self.get_id() in clients_df["id"].values:
            # Update the existing client
            clients_df.loc[clients_df["id"] == self.get_id(), "my_books"] = json.dumps(self.__my_books)
            self.__add_notification(clients_df, f"Client {self.get_name()} updated successfully in the system.")
        else:
            # Add a new client
            new_client = {
                "id": self.get_id(),
                "name": self.get_name(),
                "my_books": json.dumps(self.__my_books),
                "notifications": json.dumps([])  # Initialize an empty notifications list
            }
            clients_df = pd.concat([clients_df, pd.DataFrame([new_client])], ignore_index=True)
            self.__add_notification(clients_df, f"New client {self.get_name()} added successfully to the system.")

        # Save the updated DataFrame to the CSV file
        clients_df.to_csv(filename, index=False)
        print(f"Client {self.get_name()} added/updated successfully.")

    def __add_notification(self, message):
        """
        Adds a notification message to the client's notifications list.
        """

        clients_df = self.__clients_df
        client_row = clients_df.loc[clients_df["id"] == self.get_id()]
        if not client_row.empty:
            notifications = json.loads(client_row["notifications"].values[0]) if not pd.isna(
                client_row["notifications"].values[0]) else []
            notifications.append(message)
            clients_df.loc[clients_df["id"] == self.get_id(), "notifications"] = json.dumps(notifications)
            print(f"Notification added for {self.get_name()}: {message}")

    def borrow_book(self, book_title, book_id):
        filename = "../client.csv"

        try:
            clients_df = pd.read_csv(filename, dtype={"id": int, "name": str, "my_books": str, "notifications": str})
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print("Clients file not found or empty.")
            return False

        client_row = clients_df.loc[clients_df["id"] == self.get_id()]
        if client_row.empty:
            print("Client not found.")
            return False

        my_books = json.loads(client_row["my_books"].values[0]) if not pd.isna(client_row["my_books"].values[0]) else {}

        if book_title not in my_books:
            my_books[book_title] = []

        if book_id not in my_books[book_title]:
            my_books[book_title].append(book_id)
            self.__add_notification(clients_df, f"Book '{book_title}' with ID {book_id} borrowed successfully.")
        else:
            print(f"Book '{book_title}' with ID {book_id} is already borrowed by {self.get_name()}.")
            return False

        clients_df.loc[clients_df["id"] == self.get_id(), "my_books"] = json.dumps(my_books)
        clients_df.to_csv(filename, index=False)
        return True

    def return_book(self, book_title):
        """
        Returns a borrowed book for the client.
        If successful, returns (True, serial_number).
        If unsuccessful, returns (False, -1).
        """
        filename = "../client.csv"

        try:
            clients_df = pd.read_csv(filename, dtype={"id": int, "name": str, "my_books": str, "notifications": str})
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print("Clients file not found or empty.")
            return False, -1

        client_row = clients_df.loc[clients_df["id"] == self.get_id()]
        if client_row.empty:
            print("Client not found.")
            return False, -1

        my_books = json.loads(client_row["my_books"].values[0]) if not pd.isna(client_row["my_books"].values[0]) else {}

        if book_title in my_books and my_books[book_title]:
            max_id = max(my_books[book_title])
            my_books[book_title].remove(max_id)
            if not my_books[book_title]:
                del my_books[book_title]
            self.__add_notification(clients_df, f"Book '{book_title}' with ID {max_id} returned successfully.")
        else:
            print(f"Book '{book_title}' is not currently borrowed or has no copies.")
            return False, -1

        clients_df.loc[clients_df["id"] == self.get_id(), "my_books"] = json.dumps(my_books)
        clients_df.to_csv(filename, index=False)

        return True, max_id


# Example Usage
client = Client("Alice")
client.borrow_book("The Hobbit", 1)
