from Book import Book
import pandas as pd
from Observable import Observable
from Authinactor import Authinactor
from User import User
from log import Log

class Library(Observable):
    
    def __init__(self):
        super().__init__()
        self.lib_books: dict = {}
        self.wait_list: dict = {}
        auth_system : Authinactor = Authinactor()
        self.logger = Log()
        self.load_books_from_csv()

        
    def load_books_from_csv(self):
        books_df = pd.read_csv("books.csv", dtype={"title": str, "author": str, "year": int, "category": str, "copies": int})
        available_df = pd.read_csv("available_books.csv", dtype={"title":str, "copies": int})
        loaned_df = pd.read_csv("loaned_books.csv", dtype={"title":str, "copies": int , "user_id": int})
        wait_listdf=pd.read_csv("wait_list.csv", dtype={"title":str, "user": str })

        for item in books_df.itertuples():
            book = Book(item.title, item.author, item.year, item.category, item.copies)
            self.add_exsisting_book(book.get_title(),item.dict)

        for item in wait_listdf.itertuples():
            user=User()
            self.wait_list[item.title].append(user)

    def __load_csv(self, filename):
        """Load a CSV file or create a new one if not found."""
        try:
            return pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.logger.log(f"not abele to open {filename}")
            return pd.DataFrame()

    def __apdate_books_csv(self, filename="books.csv"):
        df = self.__load_csv(filename)

    def __apdate_available_csv(self, filename="available_books.csv"):
      df = self.__load_csv(filename)
    def __apdate_loaned_csv(self, filename="loaned_books.csv"):
      df = self.__load_csv(filename)
    def __apdate_whiting_list_csv(self, filename="wait_list.csv"):
      df = self.__load_csv(filename)

    def add_exsisting_book(self, book:Book,dict):
        # לוקחים מהcsv את הערכים למילון כלומר
        # dict{titel,(book,sum_borowd_amunt,dict{book_id,(bool,user)})}
        self.lib_books[book.get_title()] = dict
    def popular_books(self):
        popular_books=self.wait_list[list(self.wait_list.keys())[0]]
        #popular_books+= dict{titel,(book,sum_borowd_amunt}  10 עם הכי הרבה השאלות
        return self.lib_books
    def add_book(self, title, author, year, category ,copies , available_copies = 1, ):
        
        if title in self.lib_books:
            book = self.lib_books[title][0]
            
            assert book.get_author() == author, "Author mismatch"
            assert book.get_year() == year, "Year mismatch"
            assert book.get_categories() == category, "Category mismatch"
            
            self.add_book_copy(title)

        
        else:
            book = Book(title, author, year, category)
            self.lib_books[title] = (book , 0,{i:{False: None} for i in range(copies)}) # book and empty dictionary for borrowed books
            
            self.notify(f"New Book in the library: {book.__str__()}")

            # עדכון קובץ ספרים וספרים פנויים
            self.__apdate_books_csv()
            self.__apdate_available_csv()


    def remove_books(self, title):
        # if book is not borrowd 
        try:
            for i in range(len(self.lib_books[title][1][1])):
                self.remove_book_copy(title)
            
        except RuntimeError:
            return False
    
    def remove_book_copy(self, title):
        index = self.first_available_copy(title)
        
        if index is not None:
            del self.lib_books[title][1][1][index]
            self.logger.log(f"removing one copy of {title} copy number {index}")

            # עדכון קובץ ספרים וספרים פנויים
            self.__apdate_books_csv()
            self.__apdate_available_csv()

        else:
            raise RuntimeError("No available copies")
            self.logger.log("Eror: No available copies")
    
    def add_book_copy(self, title):
        index = len(self.lib_books[title][1][1])+1
        self.lib_books[title][1][1][index] = {False: None}
        self.logger.log(f"add new copy of {title} copy number {index}")

        # עדכון קובץ ספרים וספרים פנויים
        self.__apdate_books_csv()
        self.__apdate_available_csv()

    
      
    def loan_book(self, title, user:User):
        try:
            index = self.first_available_copy(title)
            if index is None:
                if not user in self.wait_list[title]:
                    self.wait_list[title].append(user)
                    self.logger.log(f"add user :{user.get_name()} to  {title} witing list")
                    # עדקון קובץ רשימת המתנה
                    self.__apdate_whiting_list_csv()
                return False

            self.lib_books[title][1][1][index] = {True: user}
            self.lib_books[title][1][0]=self.lib_books[title][1][0]+1
            self.logger.log(f" user :{user.get_name()} lownd {title} ")
            # עדכון קובץ ספרים וספרים פנויים וספרים מושאלים
            self.__apdate_books_csv()
            self.__apdate_available_csv()
            self.__apdate_loaned_csv()


            if user in self.wait_list[title]:
                self.logger.log(f" removing user :{user.get_name()} from whiting list ")
                self.wait_list[title].remove(user)
                
            return True
        
        except ValueError as e:
            print(e.args[0])
            return False
        
    
    def return_book(self, title, user:User):
        try:
            index = self.user_borrowed_book(title, user)
            if index is None:
                raise ValueError("User has not borrowed this book")
            self.logger.log(f" user:{user.get_name()} reterning {title} ")
            self.lib_books[title][1][1][index] = {False: None}
            # עדכון קובץ ספרים וספרים פנויים וספרים מושאלים
            self.__apdate_books_csv()
            self.__apdate_available_csv()
            self.__apdate_loaned_csv()
            
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
    

    def update_book(self,title,new_title,author, year , category):
        self.logger.log(f"abdate {title}")
        # עדכון קובץ ספרים וספרים פנויים וספרים מושאלים
    
    def register_new_user(self, user:User ,password):
        try:
            self.auth_system.register(user.get_id(), password)
            self.logger.log(f"register new user:{user.get_name()} ")
        except ValueError as e:
            print(e.args[0])
            
    def user_login(self, user:User, password):
        if self.auth_system.login(user.get_id(), password):
            self.logger.log(f"user:{user.get_name()} login")
            return True
        
        else:
            self.logger.log(f"user:{user.get_name()}failde to login")
            return False
        
    def user_logout(self, user:User):
        if self.auth_system.logout(user.get_id()):
            self.logger.log(f"user:{user.get_name()} logout")
        else:
            self.logger.log(f"user:{user.get_name()}failde to logout")
        
    def is_book_valid(self,title):
        if title in self.lib_books:
            return True
        
        return False
    
    def user_borrowed_book(self, title, user:User):
        if not self.is_book_valid(title):
            raise ValueError("Book not found")
        
        for i in range(len(self.lib_books[title][1][1])):
            if self.lib_books[title][1][1][i] == {True: user}:
                return i
        
        return None
        