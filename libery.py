from queue import Queue
class Library:
    def __init__(self, books=None):
        self.books = books if books else []
        self.available_books = {}
        self.borrowed_books = {}
        self.waiting_list_of_popular_books = {}

    def add_book(self, book):
        if book not in self.books:
            self.add_book_to_libery( book)
        else:
            book.add_copi_Book()
    def add_book_to_libery(self, book):
        self.books.append(book)
        לקובץ הוספה

    def get_available_books(self):#מילון של כל ספר וכמות הספרים שניתן לקחת
        self.available_books = {book.get_name(): book.get_num_of_available_copies() for book in self.books}
        return self.available_books

    def get_borrowed_books(self):
        self.borrowed_books = {book.get_name(): book.get_num_of_borrowed_copies() for book in self.books}
        return self.borrowed_books

    def add_to_waiting_list(self, book, customer):
        if book in self.books:
            if book.get_name() in self.waiting_list_of_popular_books:
                self.waiting_list_of_popular_books[book.get_name()].add(customer)
            else:
                self.waiting_list_of_popular_books[book.get_name()] = {customer}
        else:
            print(f"Book '{book.get_name()}' not in library. Adding it...")
            self.add_book(book)
            self.add_to_waiting_list(book, customer)
