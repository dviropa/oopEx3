import hashlib
import pandas as pd
import json

# from Person import Person
from old.humen.Person import Person


class User(Person):

    def __init__(self, name, password, level):
        super().__init__(name)  # שולח רק את השם למחלקת Person
        self.__password = password
        self.level = level
        self.filename = "users.csv"
        self.__user_df = self.__load_csv(["id", "name", "password", "level", "notifications"])
        self.__add()  # הוספת המשתמש למסד הנתונים

    def __load_csv(self, columns):
        """Load a CSV file or create a new one if not found."""
        try:
            return pd.read_csv(self.filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame(columns=columns)

    def __save_csv(self, df):
        """Save a DataFrame to a CSV file."""
        df.to_csv(self.filename, index=False)

    def __add(self):
        filename = "users.csv"

        try:
            users_df = pd.read_csv(filename, dtype={"id": int, "name": str, "password": str, "level": str})
        except (FileNotFoundError, pd.errors.EmptyDataError):
            users_df = pd.DataFrame(columns=["id", "name", "password", "level"])

        encrypted_password = hashlib.sha256(self.__password.encode()).hexdigest()

        if not users_df.empty and self.get_id() in users_df["id"].values:
            users_df.loc[users_df["id"] == self.get_id(), "password"] = encrypted_password
        else:
            new_user = {
                "id": self.get_id(),
                "name": self.get_name(),
                "password": encrypted_password,
                "level": self.level
            }
            users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)

        users_df.to_csv(filename, index=False)
        print(f"User {self.get_name()} added/updated successfully.")

    def __add_notification(self, message):
        """
        Adds a notification message to the client's notifications list.
        """

        user_df = self.__user_df
        client_row = user_df.loc[user_df["id"] == self.get_id()]
        if not client_row.empty:
            notifications = json.loads(client_row["notifications"].values[0]) if not pd.isna(
                client_row["notifications"].values[0]) else []
            notifications.append(message)
            user_df.loc[user_df["id"] == self.get_id(), "notifications"] = json.dumps(notifications)
            print(f"Notification added for {self.get_name()}: {message}")


# Example usage
user = User("", "1234", 1)
