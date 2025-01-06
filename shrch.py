class Search:
    def __init__(self, library):
        self.library = library
        self.filtered_books = library.books  # רשימת הספרים המסוננת

    def filter_by(self, **criteria):
        """
        פילטר לפי קריטריונים (לדוגמה: genre="Drama", year=1999).
        """
        for key, value in criteria.items():
            self.filtered_books = [
                book for book in self.filtered_books if getattr(book, key, None) == value
            ]
        return self  # מחזיר את האובייקט עצמו כדי לאפשר שלבים

    def filter_by_genres(self, genres):
        """
        פילטר לפי רשימת ז'אנרים (לדוגמה: ["Drama", "Comedy"]).
        """
        self.filtered_books = [
            book for book in self.filtered_books if book.genre in genres
        ]
        return self

    def sort_by(self, key, reverse=False):
        """
        מיון לפי מפתח מסוים (לדוגמה: year).
        """
        self.filtered_books.sort(key=lambda book: getattr(book, key, None), reverse=reverse)
        return self

    def get_results(self):
        """
        מחזיר את התוצאות המסוננות.
        """
        return self.filtered_books
