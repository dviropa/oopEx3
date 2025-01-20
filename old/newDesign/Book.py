
class Book():
    def __init__(self, title, author, year , category,id=0):
        self.__title = title
        self.__author = author
        self.__year = year
        self.__category = category
        # self.id = id
        
    def get_title(self):
        return self.__title
    
    def get_author(self):
        return self.__author
    
    def get_year(self):
        return self.__year
    
    def get_categories(self):
        return self.__category

    def __str__(self):
        return f"Title: {self.__title}, Author: {self.__author}, Year: {self.__year}, Category: {self.__category}"