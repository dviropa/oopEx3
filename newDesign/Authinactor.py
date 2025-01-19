import hashlib
import uuid

import pandas as pd
from User import User
from log import Log

class Authinactor:
    def __init__(self):
        self.users = {}
        self.hashed_passwords = {}
        self.read_users_from_csv()
        self.logger=Log()

    def __load_csv(self):
        try:
            return pd.read_csv("users.csv")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.logger.log(f"not abele to open users.csv")
            df = pd.DataFrame(columns=["id", "name", "hashed_password"])
            return df

    def read_users_from_csv(self):
        df = self.__load_csv()
        if not df.empty:
            self.users = {user_id: False for user_id in df["id"].tolist()}
            self.hashed_passwords = {
                user_id: hashed_password
                for user_id, hashed_password in zip(df["id"].tolist(), df["hashed_password"].tolist())
            }

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, user_id, user_name, password: str):
        # register the user with the hashed password
        if user_id is None:
            df = self.__load_csv()
            user_id = int(df["id"].max()) + 1 if not df.empty else 1
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = False
        self.hashed_passwords[user_id] = self.hash_password(password)
        self.update_file(user_id, user_name, password)

    def update_file(self, user_id, user_name, password):
        df = self.__load_csv("users.csv")
        new_row = {"id": user_id, "name": user_name, "hashed_password": self.hash_password(password)}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("users.csv", index=False)




    def login(self, user_id, password: str):
        if self.hash_password(password) == self.hashed_passwords[user_id]:
            self.users[user_id] = True
            return True
        return False


    def logout(self, user_id):
        if self.users[user_id]:
            self.users[user_id] = False
            return True
        return False



    def isLoggedIn(self, user_id):
        return self.users[user_id]
