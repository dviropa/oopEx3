import unittest
import pandas as pd
import os
import hashlib
from Authinactor import Authinactor


class TestAuthinactor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # יצירת קובץ CSV דמה לבדיקות
        cls.users_csv = "users.csv"
        pd.DataFrame({
            "id": [1, 2, 3],
            "name": ["Dvir", "Harel", "ETL"],
            "hashed_password": [
                hashlib.sha256("password".encode()).hexdigest(),
                hashlib.sha256("qwerty".encode()).hexdigest(),
                hashlib.sha256("abc123".encode()).hexdigest()
            ]
        }).to_csv(cls.users_csv, index=False)

    @classmethod
    def tearDownClass(cls):
        # מחיקת קובץ CSV לאחר הבדיקות
        os.remove(cls.users_csv)

    def setUp(self):
        self.auth = Authinactor()

    def test_read_users_from_csv(self):
        self.assertEqual(len(self.auth.users), 3)
        self.assertIn(1, self.auth.users)

    def test_register_new_user(self):
        self.auth.register(None, "David", "newpassword")
        self.assertIn(4, self.auth.users)
        self.assertEqual(
            self.auth.hashed_passwords[4],
            self.auth.hash_password("newpassword")
        )

    def test_login_success(self):
        self.assertTrue(self.auth.login(1, "password"))

    def test_login_failure(self):
        self.assertFalse(self.auth.login(1, "wrongpassword"))

    def test_logout(self):
        self.auth.login(1, "password")
        self.assertTrue(self.auth.logout(1))
        self.assertFalse(self.auth.isLoggedIn(1))

    def test_update_file(self):
        self.auth.register(None, "Dvir", "securepass")
        df = pd.read_csv("users.csv")
        self.assertIn("Dvir", df["name"].tolist())


if __name__ == "__main__":
    unittest.main()
