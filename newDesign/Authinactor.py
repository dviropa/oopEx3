import hashlib
import pandas as pd
from User import User

class Authinactor:
    def __init__(self):
        self.users = {}
        self.hashed_passwords = {}
    
    def read_users_from_csv(self,filename="users.csv"):
        # read users from csv file and store them in the dict as key with false as value; 
        pass
    def apdate_users_csv(self,filename="users.csv"):
        # read users from csv file and store them in the dict as key with false as value;
        pass
        
    def register(self, user_id, password: str):
        # register the user with the hashed password
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = False
        self.hashed_passwords[user_id] = self.hash_password(password)
        
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
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def isLoggedIn(self,user_id):
        return self.users[user_id]