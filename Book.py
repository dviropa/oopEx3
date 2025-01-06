
import pandas as pd
class Book:
    def __init__(self, author, name, year, category, available, num_of_copies):
        self.__author = author
        self.__name = name
        self.__year = year
        self.__category = category
        self.__num_of_copies = num_of_copies
        self.__num_of_available_copies = num_of_copies
        self.__num_of_borrowed_copies = 0


    def get_author(self):
        return self.author
    def set_author(self, author):
        # עדכון כמות הספרים בקובץ
        self.update_book(self).set_val("author", author)
        self.author = author

    def get_name(self):
        return self.name

    def set_name(self, name):
        # עדכון כמות הספרים בקובץ
        self.update_book(self).set_val("name", name)

        self.name = name

    def get_year(self):
        return self.year

    def set_year(self, year):
        # עדכון כמות הספרים בקובץ
        self.update_book(self).set_val("year", year)
        self.year = year

    def get_category(self):
        return self.category

    def set_category(self, category):
        self.update_book(self).set_val("category", category)
        self.category = category
        self.genre = category

    def add_category(self, category):
        new_category = []
        new_category = self.update_book(self).get_val(category)
        new_category.add(category)

        self.update_book(self).set_val("category", category)
        self.category.append(category)
        self.genre.append(category)

    def return_book(self):
        if self.num_of_borowd_copise > 0:
            self.num_of_availibole_copise += 1
            self.num_of_borowd_copise -= 1
        else:
            print("ther ar no boks to return")

    def boro_book(self):
        if self.num_of_availibole_copise > 0:
            self.num_of_availibole_copise -= 1
            self.num_of_borowd_copise += 1
        else:
            print("ther ar no boks to boro")

    def get_num_of_boro_copisek(self):
        return self.num_of_borowd_copise

    def get_num_of_num_of_availibole_copisek(self):
        return self.availibole_copisek
    def add_copy(self):
        self.num_of_copies += 1
        self.num_of_available_copies += 1
        self.update_file("copies", self.num_of_copies)

    def remove_copy(self):
        if self.num_of_copies > 0:
            self.num_of_copies -= 1
            if self.num_of_available_copies > 0:
                self.num_of_available_copies -= 1
            self.update_file("copies", self.num_of_copies)
        else:
            print("No copies available to remove.")

    def borrow_book(self):
        if self.num_of_available_copies > 0:
            self.num_of_available_copies -= 1
            self.num_of_borrowed_copies += 1
        else:
            print("No copies available to borrow.")

    def return_book(self):
        if self.num_of_borrowed_copies > 0:
            self.num_of_available_copies += 1
            self.num_of_borrowed_copies -= 1
        else:
            print("No borrowed copies to return.")

    def update_file(self, column, value):
        filename = "books.csv"
        books_df = pd.read_csv(filename)
        books_df.loc[books_df["title"] == self.name, column] = value
        books_df.to_csv(filename, index=False)


