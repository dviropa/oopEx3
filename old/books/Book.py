import json

import pandas as pd


class Book:
    def __init__(self, author, name, year, category, num_of_copies=1,count_num_of_burows_copize=0):
        self.__author = author
        self.__name = name
        self.__year = year
        self.__category = category
        self.__num_of_copies = num_of_copies
        self.__num_of_borrowed_copies = 0
        self.__is_loaned = {i: False for i in range(1, num_of_copies + 1)}
        self.__count_num_of_burows_copize=count_num_of_burows_copize
        # self.__initialize_book_in_file()
    # def __init__(self,book):
    #     self.__author = book.__author
    #     self.__name = book.__name
    #     self.__year = book.__year
    #     self.__category = book.__category
    #     self.__num_of_copies = book.__num_of_copies
    #     self.__num_of_borrowed_copies = book.__num_of_borrowed_copies
    #     self.__is_loaned = book.__is_loaned
    #     self.__count_num_of_burows_copize=book.__count_num_of_burows_copize
    #     self.__initialize_book_in_file()
    def __str__(self):
        return f"Book(title={self.title}, author={self.author}, genre={self.genre}, year={self.year})"


class BookFactory:
    def __init__(self, filename="books.csv"):
        self.filename = filename
        self._ensure_file_exists()
    def __load_csv(self, filename= "books.csv"):
        """Load a CSV file or create a new one if not found."""
        try:
            return pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return pd.DataFrame()

    def __save_csv(self, df, filename="books.csv"):
        """Save a DataFrame to a CSV file."""
        df.to_csv(filename, index=False)

    def _ensure_file_exists(self):
        try:
            pd.read_csv(self.filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # Create an empty DataFrame with required columns
            books_df = pd.DataFrame(columns=[
                "name", "author", "year", "category", "num_of_copies", "num_of_borrowed_copies", "is_loaned"
            ])
            books_df.to_csv(self.filename, index=False)



    def create_book(self,book):#הוספה ךקובץ ספרים פנויים
        books_df = self.__load_csv()
        if book.__name in books_df["title"].values:
            self.add_copy_to_existing_book(book.__name)
            return

        # new_book = Book(book.__title, book.__author, book.__year, book.__category, book.__num_of_copies)
        books_df = pd.concat([books_df, pd.DataFrame([{"title": book.__title,"author": book.__author,"year": book.__year,"category": book.__category,"num_of_copies": book.__num_of_copies,"num_of_borrowed_copies": book.__num_of_borrowed_copies,"is_loaned": json.dumps(book.__is_loaned)}])], ignore_index=True)
        self.__save_csv(books_df)
        print(f"Book '{book.__name}' created successfully.")
    def create_book(self, title, author, year, category, num_of_copies=1):#הוספה ךקובץ ספרים פנויים
        """Create a new book or add a copy if the book exists."""
        books_df = self.__load_csv()
        if title in books_df["title"].values:
            self.add_copy_to_existing_book(title)
            return

        new_book = Book(title, author, year, category, num_of_copies)
        books_df = pd.concat([books_df, pd.DataFrame([{"title": new_book.title,"author": new_book.author,"year": new_book.year,"category": new_book.category,"num_of_copies": new_book.num_of_copies,"num_of_borrowed_copies": new_book.num_of_borrowed_copies,"is_loaned": json.dumps(new_book.is_loaned)}])], ignore_index=True)
        self.__save_csv(books_df)
        print(f"Book '{title}' created successfully.")

    def add_copy_to_existing_book(self, book_name):
        try:
            books_df = self.__load_csv()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            books_df = pd.DataFrame(columns=[
                "name", "author", "year", "category", "num_of_copies", "num_of_borrowed_copies", "is_loaned"
            ])
        if book_name in books_df["name"].values:
            books_df.loc[books_df["name"] == book_name, "num_of_copies"] += 1
            serial_number=self.get_avelibul_sirial_number()
            books_df.loc[books_df["name"] == book_name, "is_loaned"][serial_number]="NO"
            self.add_to_available_book_file(book.__name, serial_number)
            self.__save_csv(books_df)
            print(f"A new copy of '{book_name}' has been added.")
            return True
        else:
            print(f"Book '{book_name}' does not exist in the file. Cannot add a copy.")
            return False

    def add_book(self,book):
        try:
            books_df = self.__load_csv()
        except (FileNotFoundError, pd.errors.EmptyDataError):
            books_df = pd.DataFrame(columns=[
                "name", "author", "year", "category", "num_of_copies", "num_of_borrowed_copies", "is_loaned"
            ])

        if book.__name in books_df["name"].values:
            self.add_copy_to_existing_book(book.__name)
            return

        new_book = {"name": book.__name,"author": book.__author,"year": book.__year,"category": book.__category,"num_of_copies": book.__num_of_copies,"num_of_borrowed_copies": book.__num_of_borrowed_copies,"is_loaned": json.dumps(book.__is_loaned)
        }

        for serial_number in book.__is_loaned.keys():
            self.add_to_available_book_file(book.__name, serial_number)

        books_df = pd.concat([books_df, pd.DataFrame([new_book])], ignore_index=True)
        self.__save_csv(books_df)
        print(f"Added new book: '{book.__name}'.")

    def add_to_available_book_file(self, name, serial_number):
        filename = "avaikacle_books.csv"
        try:
            books_df = pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # אם הקובץ לא קיים או ריק, יוצרים DataFrame חדש
            books_df = pd.DataFrame(columns=["name", "available_serials"])

        # Find the book in the file
        book_row = books_df[books_df["name"] == name]

        if book_row.empty:
            # אם הספר לא נמצא, נוסיף רשומה חדשה
            new_entry = {
                "name": name,
                "available_serials": json.dumps([serial_number])  # יוצרים רשימה חדשה עם המספר הסידורי
            }
            books_df = pd.concat([books_df, pd.DataFrame([new_entry])], ignore_index=True)
        else:
            # אם הספר קיים, נוסיף את המספר הסידורי לרשימה הקיימת
            available_books = json.loads(
                book_row.iloc[0]["available_serials"]) if "available_serials" in book_row.columns else []

            if serial_number in available_books:
                print(f"Serial number {serial_number} already exists in the available list for book '{name}'.")
                return

            available_books.append(serial_number)
            books_df.loc[books_df["name"] == name, "available_serials"] = json.dumps(available_books)

        # Save the updated DataFrame back to the file
        books_df.to_csv(filename, index=False)
        print(f"Serial number {serial_number} added to the available list for book '{name}'.")

    def get_avelibul_sirial_number(self):
        """
        Returns the first available serial number for the book by reading from the CSV file.
        """
        filename = "../books.csv"

        try:
            # קריאת הקובץ books.csv
            books_df = pd.read_csv(filename)

            # סינון הרשומות של הספר הנוכחי לפי השם
            book_rows = books_df[books_df["name"] == self.__name]

            if book_rows.empty:
                print(f"No records found for the book '{self.__name}' in the file.")
                return None

            # חיפוש המספר הסידורי הראשון הפנוי (is_loaned = False)
            for _, row in book_rows.iterrows():
                if not row["is_loaned"]:  # בדיקה אם העותק אינו מושאל
                    return row["sirial_number"]

            print(f"No available copies for the book '{self.__name}'.")
            return None  # במקרה שאין עותקים פנויים

        except (FileNotFoundError, pd.errors.EmptyDataError):
            print(f"File '{filename}' not found or is empty.")
            return None

    def set_sirial_number(self, default=1):

        filename = "../books.csv"
        try:
            users_df = pd.read_csv(filename)
            if not users_df.empty and "is_loaned" in users_df.columns:
                return users_df["is_loaned"].max() + 1
            else:
                return default
        except (FileNotFoundError, pd.errors.EmptyDataError):
            return default

    def borrow_book(self,name,book=None):
        """
        Borrow a specific copy of the book.
        """
        filename = "../books.csv"
        try:
            books_df = pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print(f"File '{filename}' not found or is empty.")
            return

        # Find the book in the file
        book_row = books_df[books_df["name"] == name]
        if book_row.empty:
            print("Book not found in the file.")
            return

        serial_number=self.get_avelibul_sirial_number()
        # Update the internal and file data
        self.__is_loaned[serial_number] = True
        self.__num_of_borrowed_copies += 1
        books_df=books_df.loc[books_df["name"]]
        books_df.loc["count_num_of_burows_copize"] = books_df.loc["count_num_of_burows_copize"] +1
        books_df.loc["num_of_borrowed_copies"] = books_df.loc[ "num_of_borrowed_copies"] +1
        books_df.loc["is_loaned"] = json.dumps(book.__is_loaned)
        books_df.to_csv(filename, index=False)
        print(f"Book '{self.__name}' copy {serial_number} borrowed successfully.")
        return serial_number

    def return_book(self, serial_number,name):
        """
        Return a borrowed copy of the book.
        """
        filename = "../books.csv"
        try:
            books_df = pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print(f"File '{filename}' not found or is empty.")
            return

        # Find the book in the file
        book_row = books_df[books_df["name"] == self.__name]
        if book_row.empty:
            print("Book not found in the file.")
            return

        if serial_number not in self.__is_loaned or not self.__is_loaned[serial_number]:
            print(f"Copy {serial_number} is not currently borrowed.")
            return

        # Update the internal and file data
        self.__is_loaned[serial_number] = False
        self.__num_of_borrowed_copies -= 1

        book_row.loc[books_df["name"] == self.__name, "num_of_borrowed_copies"] = self.__num_of_borrowed_copies
        book_row.loc[books_df["name"] == self.__name, "is_loaned"] = json.dumps(self.__is_loaned)
        book_row.to_csv(filename, index=False)

        print(f"Book '{self.__name}' copy {serial_number} returned successfully.")

    def add_copy(self):
        """
        Add a new copy of the book.
        """
        self.__num_of_copies += 1
        new_serial = max(self.__is_loaned.keys(), default=0) + 1
        self.__is_loaned[new_serial] = False

        filename = "../books.csv"
        try:
            books_df = pd.read_csv(filename)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print(f"File '{filename}' not found or is empty.")
            return

        books_df.loc[books_df["name"] == self.__name, "num_of_copies"] = self.__num_of_copies
        books_df.loc[books_df["name"] == self.__name, "is_loaned"] = json.dumps(self.__is_loaned)
        books_df.to_csv(filename, index=False)
        print(f"A new copy of '{self.__name}' has been added.")

# Example usage
if __name__ == "__main__":
    factory = BookFactory()
    data = """title,author,is_loaned,copies,genre,year
    The Catcher in the Rye,J.D. Salinger,No,3,Fiction,1951
    To Kill a Mockingbird,Harper Lee,Yes,2,Fiction,1960
    1984,George Orwell,Yes,5,Dystopian,1949
    The Great Gatsby,F. Scott Fitzgerald,No,4,Classic,1925
    Moby Dick,Herman Melville,No,1,Adventure,1851
    Pride and Prejudice,Jane Austen,Yes,3,Romance,1813
    War and Peace,Leo Tolstoy,No,2,Historical Fiction,1869
    Great Expectations,Charles Dickens,No,3,Classic,1861
    Crime and Punishment,Fyodor Dostoevsky,Yes,1,Psychological Drama,1866
    The Brothers Karamazov,Fyodor Dostoevsky,No,3,Philosophy,1880
    The Divine Comedy,Dante Alighieri,Yes,1,Epic Poetry,1320
    Jane Eyre,Charlotte Brontë,No,2,Gothic Fiction,1847
    Wuthering Heights,Emily Brontë,No,4,Gothic Romance,1847
    Anna Karenina,Leo Tolstoy,Yes,2,Fiction,1877
    Madame Bovary,Gustave Flaubert,No,3,Realism,1857
    The Iliad,Homer,Yes,1,Epic Poetry,-750
    The Sound and the Fury,William Faulkner,No,2,Modernism,1929
    Invisible Man,Ralph Ellison,Yes,1,Fiction,1952
    Beloved,Toni Morrison,Yes,3,Historical Fiction,1987
    Catch-22,Joseph Heller,No,4,Satire,1961
    Slaughterhouse-Five,Kurt Vonnegut,Yes,2,Science Fiction,1969
    Brave New World,Aldous Huxley,No,5,Dystopian,1932
    Heart of Darkness,Joseph Conrad,Yes,3,Adventure,1899
    The Grapes of Wrath,John Steinbeck,No,2,Fiction,1939
    Of Mice and Men,John Steinbeck,Yes,1,Tragedy,1937
    The Old Man and the Sea,Ernest Hemingway,No,3,Fiction,1952
    The Hobbit,J.R.R. Tolkien,Yes,4,Fantasy,1937
    The Lord of the Rings,J.R.R. Tolkien,Yes,2,Fantasy,1954
    Harry Potter and the Philosopher's Stone,J.K. Rowling,No,7,Fantasy,1997
    A Game of Thrones,George R.R. Martin,Yes,5,Fantasy,1996
    The Name of the Wind,Patrick Rothfuss,No,3,Fantasy,2007
    Mistborn: The Final Empire,Brandon Sanderson,Yes,4,Fantasy,2006
    The Handmaid's Tale,Margaret Atwood,No,3,Dystopian,1985
    The Odyssey,Homer,Yes,2,Epic Poetry,-800"""

    # קריאת הנתונים ל-DataFrame
    from io import StringIO

    df = pd.read_csv(StringIO(data))

    # יצירת פאקטורי
    factory = BookFactory()
    books = []
    for _, row in df.iterrows():
        book = factory.create_book(
            title=row["title"],
            author=row["author"],
            copies=row["copies"],
            genre=row["genre"],
            year=row["year"]
        )
        books.append(book)



    all_books = factory.__load_csv()
    for book in all_books:
        print(book)
