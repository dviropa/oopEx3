import User
import Library

def main():
    lib = Library.Library()
    user = User.User("John", 1)
    
    lib.subscribe(user)
    
    lib.add_book("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction", 2)   
    
if __name__ == "__main__":
    main()