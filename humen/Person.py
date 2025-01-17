import pandas as pd

class Person:
    def __init__(self, name):
        self.name = name
        self.__id = self.__get_max_id()

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.name

    def __get_max_id(self, default=1110):
        users_filename = "../users.csv"
        clients_filename = "../client.csv"

        try:
            # קריאת קובץ המשתמשים
            users_df = pd.read_csv(users_filename)
            max_user_id = users_df["id"].max() if not users_df.empty and "id" in users_df.columns else default
        except (FileNotFoundError, pd.errors.EmptyDataError):
            max_user_id = default

        try:
            # קריאת קובץ הלקוחות
            clients_df = pd.read_csv(clients_filename)
            max_client_id = clients_df["id"].max() if not clients_df.empty and "id" in clients_df.columns else default
        except (FileNotFoundError, pd.errors.EmptyDataError):
            max_client_id = default

        # החזרת הערך המקסימלי בין שני הקבצים + 1
        return max(max_user_id, max_client_id) + 1

