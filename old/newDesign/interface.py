
from Book import Book
from Library import Library as lib
from User import User as u

from old.newDesign.search import Search
from Authinactor import Authinactor as auth
import tkinter as tk
import pandas as pd

# ---------------- Model ------------------
class LibraryDataManager:
    def __init__(self):
        # self.lib = lib.Library()
        # self.books = lib.get_available_books()
        # self.users = lib.get_users()
        # self.clients = lib.get_clint()
        # waitlist = []
        # self.borrowed_books = lib.get_borrowed_books()
        self.books= []
        self.users= []
        self.clients= []
        waitlist = []
        self.borrowed_books= []


    def login_user(self, name, password):
        return auth.login(name,password)
        # return True
    def add_book(self, book_name,titel,yeare,zaner):
        lib.add_book(book_name,titel,yeare,zaner)

    def remove_book(self, book_name):
        lib.delete_book(book_name)

    def borrow_book(self, user_id, book_name):
        lib.borrow_book(user_id, book_name)

    def return_book(self, user_id, book_name):
        lib.return_book(user_id, book_name)

    def add_user(self, user_name,password):
        lib.register_new_user(user_name,password)
    def get_top10_most_pupular(self):
        lib.top10_popular_books()


# ---------------- View ------------------
class LibraryUI:
    def __init__(self, root):
        self.root = root

    def show_popup(self, message):
        popup = tk.Toplevel(self.root, bg="#f0f0f0")
        popup.title("הודעה")
        popup.geometry("300x150")
        label = tk.Label(popup, text=message, font=("Arial", 14), bg="#f0f0f0", fg="#333")
        label.pack(expand=True, pady=20)
        popup.after(1000, popup.destroy)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self, login_callback,rejester_callback):
        self.clear_screen()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="#f5f5f5")
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="שם משתמש:", font=("Arial", 14), bg="#f5f5f5", fg="#555").pack(pady=10)
        username_entry = tk.Entry(frame, font=("Arial", 14))
        username_entry.pack()

        tk.Label(frame, text="סיסמה:", font=("Arial", 14), bg="#f5f5f5", fg="#555").pack(pady=10)
        password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
        password_entry.pack()
        def on_rejester():
            rejester_callback(username_entry.get(), password_entry.get())
        tk.Button(frame, text="rejester", command=on_rejester, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)

        def on_login():
            login_callback(username_entry.get(), password_entry.get())

        tk.Button(frame, text="login", command=on_login, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)

    def show_main_menu(self, menu_options):
        self.clear_screen()
        tk.Label(self.root, text="תפריט ראשי", font=("Arial", 24), bg="#f5f5f5", fg="#333").pack(pady=20)

        for text, command in menu_options:
            tk.Button(
                self.root, text=text, command=command, font=("Arial", 14), bg="#4CAF50", fg="white",
                activebackground="#45a049", padx=20, pady=10
            ).pack(pady=10)

# ---------------- Controller ------------------
class LibraryController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.show_login_screen(self.check_login)
        self.books_df=pd.read_csv("books.csv")

    def check_login(self, username, password):
        if self.model.login_user(username, password):
            self.view.show_popup("נכנס בהצלחה!")
            self.view.root.after(1000, self.load_main_menu)
        else:
            self.view.show_popup("שם משתמש או סיסמה שגויים.")

    def load_main_menu(self):
        menu_options = [
             ("הוספת ספר", self.add_book_screen),
            ("הסרת ספר", self.remove_book_screen),
            ("add user", self.add_user_screen()),
            ("הוסף לרשימת המתנה", self.add_to_waitlist),
            ("השאלת ספר", self.borrow_book),
            ("logaut",self.logaut),
            ("החזרת ספר", self.return_book_screen),
            ("search", self.search_book_screen)
        ]
        self.view.show_main_menu(menu_options)

    def search_book_screen(self):
        # פונקציה לחיפוש ספר
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="#f9f9f9")
        tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)

        tk.Label(root, text="חפש ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)

        search_entry = tk.Entry(root, font=("Arial", 14))
        search_entry.pack(pady=10)

        # רשימת ז'אנרים לדוגמה
        genres = list(self.books_df["genre"].unique())
        genre_vars = {genre: tk.BooleanVar() for genre in genres}

        # יצירת מסגרות לעמודות ימין ושמאל
        left_frame = tk.Frame(root, bg="#f9f9f9")
        right_frame = tk.Frame(root, bg="#f9f9f9")

        tk.Label(root, text="בחר ז'אנרים:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack(pady=10)

        # הצגת הצ'קבוקסים בחלוקה לשתי עמודות
        for i, genre in enumerate(genres):
            frame = left_frame if i % 2 == 0 else right_frame
            tk.Checkbutton(
                frame, text=genre, variable=genre_vars[genre], font=("Arial", 12),
                bg="#f9f9f9", fg="#333", selectcolor="#f9f9f9", anchor="w"
            ).pack(anchor="w", padx=10, pady=2)

        # ארגון המסגרות בעמודות
        left_frame.pack(side="left", fill="y", padx=20, pady=10)
        right_frame.pack(side="right", fill="y", padx=20, pady=10)

        results_list = tk.Listbox(root, width=70, height=50, font=("Arial", 12))

        def search_action():
            search_query = search_entry.get().lower()
            selected_genres = [genre for genre, var in genre_vars.items() if var.get()]

            # שימוש במערכת האסטרטגיות
            search = Search(self.books_df)
            if search_query:
                search = search.apply_strategy(search.FilterByAuthor(), author=[search_query])
            if selected_genres:
                search = search.apply_strategy(search.FilterByGenres(), genres=selected_genres)

            results = search.get_results()

            # הצגת התוצאות
            results_list.delete(0, tk.END)
            if not results.empty:
                for _, row in results.iterrows():
                    results_list.insert(tk.END, f"{row['title']} by {row['author']} ({row['year']})")
            else:
                results_list.insert(tk.END, "לא נמצאו ספרים מתאימים.")

        def on_book_select(event):
            try:
                selected = results_list.get(results_list.curselection())
                self.borrow_book_screen(selected)
            except tk.TclError:
                pass  # אין פריט נבחר

        results_list.bind("<<ListboxSelect>>", on_book_select)

        tk.Button(root, text="חפש", command=search_action, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=10)
        results_list.pack(pady=10)

        tk.Button(root, text="חזרה", command=self.load_main_menu, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)

    # def search_book_screen(self):
    #     # פונקציה לחיפוש ספר
    #     for widget in root.winfo_children():
    #         widget.destroy()
    #     root.configure(bg="#f9f9f9")
    #
    #     tk.Label(root, text="חפש ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
    #
    #     search_entry = tk.Entry(root, font=("Arial", 14))
    #     search_entry.pack(pady=10)
    #
    #     # רשימת ז'אנרים לדוגמה
    #     # רשימת הז'אנרים
    #     genres = ["Fiction", "Dystopian", "Classic", "Adventure", "Romance",
    #               "Philosophy", "Drama", "Psychological", "Epic", "Poetry",
    #               "Gothic", "Realism", "Modernism", "Historical", "Satire",
    #               "Science Fiction", "Tragedy"]
    #     genre_vars = {genre: tk.BooleanVar() for genre in genres}
    #
    #     # יצירת מסגרות לעמודות ימין ושמאל
    #     left_frame = tk.Frame(root, bg="#f9f9f9")
    #     right_frame = tk.Frame(root, bg="#f9f9f9")
    #
    #     # כותרת
    #     tk.Label(root, text="בחר ז'אנרים:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack(pady=10)
    #
    #     # הצגת הצ'קבוקסים בחלוקה לשתי עמודות
    #     for i, genre in enumerate(genres):
    #         frame = left_frame if i % 2 == 0 else right_frame
    #         tk.Checkbutton(
    #             frame, text=genre, variable=genre_vars[genre], font=("Arial", 12),
    #             bg="#f9f9f9", fg="#333", selectcolor="#f9f9f9", anchor="w"
    #         ).pack(anchor="w", padx=10, pady=2)
    #
    #     # ארגון המסגרות בעמודות
    #     left_frame.pack(side="left", fill="y", padx=20, pady=10)
    #     right_frame.pack(side="right", fill="y", padx=20, pady=10)
    #
    #     results_list = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
    #
    #     def search_action():
    #         search_query = search_entry.get().lower()
    #         selected_genres = [genre for genre, var in genre_vars.items() if var.get()]
    #
    #         # סינון הספרים לפי החיפוש והז'אנרים שנבחרו
    #         filtered_books = [
    #             book for book in self.books.keys()
    #             if search_query in book.lower() and
    #             (not selected_genres or any(genre in book.lower() for genre in selected_genres))
    #         ]
    #
    #         results_list.delete(0, tk.END)
    #         if filtered_books:
    #             for book in filtered_books:
    #                 results_list.insert(tk.END, book)
    #         else:
    #             results_list.insert(tk.END, "לא נמצאו ספרים מתאימים.")
    #
    #     def on_book_select(event):
    #         selected = results_list.get(results_list.curselection())
    #         self.borrow_book_screen(selected)
    #
    #     results_list.bind("<<ListboxSelect>>", on_book_select)
    #
    #     tk.Button(root, text="חפש", command=search_action, font=("Arial", 14),
    #               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=10)
    #     results_list.pack(pady=10)
    #
    #     tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
    #               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)

    def add_user_screen(self):
        # הוספת משתמש
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="#f9f9f9")
        tk.Label(root, text="הוספת משתמש", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)

        tk.Label(root, text="שם משתמש:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        username_entry = tk.Entry(root, font=("Arial", 14))
        username_entry.pack(pady=10)

        tk.Label(root, text="סיסמה:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        password_entry = tk.Entry(root, font=("Arial", 14), show="*")
        password_entry.pack(pady=10)

        def add_user():
            username = username_entry.get()
            password = password_entry.get()
            LibraryDataManager.add_user(username,password)
            LibraryUI.show_popup(f"'{username}' נוסף בהצלחה.")
            LibraryUI.load_main_menu()

        tk.Button(root, text="הוסף משתמש", command=add_user, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
        tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)


    def add_book(self):
        self.view.show_popup("פונקציית הוספת ספר")
    def add_book_screen(self):
        # הוספת ספר
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="#f9f9f9")
        tk.Label(root, text="הוספת ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)

        tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        book_entry = tk.Entry(root, font=("Arial", 14))
        book_entry.pack(pady=10)

        def check_book():
            book_name = book_entry.get()
            if not book_name:
                LibraryUI.show_popup("יש להזין שם ספר.")
                return
            if lib.book_exists(book_name):
                lib.add_copy(book_name)
                LibraryUI.show_popup(f"עותק נוסף נוסף לספר '{book_name}'.")
                LibraryUI.load_main_menu()
            else:
                show_extra_fields(book_name)

        def show_extra_fields(book_name):
            for widget in root.winfo_children():
                widget.destroy()
            tk.Label(root, text=f"הוספת ספר חדש: {book_name}", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(
                pady=20)

            tk.Label(root, text="תאריך הוצאה:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
            date_entry = tk.Entry(root, font=("Arial", 14))
            date_entry.pack(pady=10)

            tk.Label(root, text="סופר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
            author_entry = tk.Entry(root, font=("Arial", 14))
            author_entry.pack(pady=10)

            tk.Label(root, text="כמות:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
            quantity_entry = tk.Entry(root, font=("Arial", 14))
            quantity_entry.pack(pady=10)

            tk.Label(root, text="שנת הוצאה:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
            year_entry = tk.Entry(root, font=("Arial", 14))
            year_entry.pack(pady=10)

            tk.Label(root, text="category:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
            category_entry = tk.Entry(root, font=("Arial", 14))
            category_entry.pack(pady=10)

            tk.Label(root, text="name:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
            name_entry = tk.Entry(root, font=("Arial", 14))
            name_entry.pack(pady=10)

            def save_book():
                date = date_entry.get()
                author = author_entry.get()
                quantity = quantity_entry.get()
                year = year_entry.get()
                name = name_entry.get()
                category = category_entry.get()

                if not (date and author and quantity.isdigit() and year.isdigit()):
                    LibraryUI.show_popup("נא למלא את כל השדות בצורה תקינה.")
                    return
                book = Book(author, name, year, category, quantity)
                lib.add_new_book(book)
                LibraryUI.show_popup(f"'{book_name}' נוסף בהצלחה לספרייה.")
                LibraryUI.load_main_menu()

            tk.Button(root, text="שמור ספר", command=save_book, font=("Arial", 14),
                      bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
            tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                      bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)

        tk.Button(root, text="בדוק ספר", command=check_book, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
        tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)

    def remove_book(self):
        self.view.show_popup("פונקציית הסרת ספר")

    def remove_book_screen(self):
        # הסרת ספר
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="#f9f9f9")
        tk.Label(root, text="הסרת ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)

        tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        book_entry = tk.Entry(root, font=("Arial", 14))
        book_entry.pack(pady=10)

        def remove_book():
            book_name = book_entry.get()
            # if book_name in books:
            #     books[book_name] -= 1
            #     if books[book_name] == 0:
            #         del books[book_name]
            #     show_popup(f"'{book_name}' הוסר מהספרייה.")
            # else:
            #     show_popup("הספר לא נמצא בספרייה.")
            # load_main_menu()

        tk.Button(root, text="הסר ספר", command=remove_book, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=20)
        tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=10)



    def borrow_book(self):
        self.view.show_popup("פונקציית השאלת ספר")

    # def return_book(self):
    #     self.view.show_popup("פונקציית החזרת ספר")

    def return_book_screen(self):
        # פונקציה להחזרת ספר
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="#f9f9f9")
        tk.Label(root, text="החזרת ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)

        tk.Label(root, text="שם:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        name_entry = tk.Entry(root, font=("Arial", 14))
        name_entry.pack(pady=10)

        tk.Label(root, text="תעודת זהות:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        id_entry = tk.Entry(root, font=("Arial", 14))
        id_entry.pack(pady=10)

        tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        book_entry = tk.Entry(root, font=("Arial", 14))
        book_entry.pack(pady=10)

        def return_book():
            name = name_entry.get()
            id_num = id_entry.get()
            book_name = book_entry.get()
            if name and id_num and book_name:
                for record in self.borrowed_books:
                    if record["name"] == name and record["id"] == id_num and record["book"] == book_name:
                        self.borrowed_books.remove(record)
                        self.books[book_name] = self.books.get(book_name, 0) + 1
                        self.show_popup(f"{name} החזיר את '{book_name}'.")
                        LibraryUI.load_main_menu()
                        return
                LibraryUI.show_popup("הרשומה לא נמצאה.")
            else:
                LibraryUI.show_popup("יש למלא את כל השדות.")

        tk.Button(root, text="החזר ספר", command=return_book, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
        tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)


    def add_to_waitlist(self):
        self.view.show_popup("פונקציית הוספה לרשימת המתנה")

    def add_to_waitlist_screen(self):
        # הוספה לרשימת המתנה
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="#f9f9f9")
        tk.Label(root, text="הוספה לרשימת המתנה", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)

        tk.Label(root, text="שם הלקוח:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        name_entry = tk.Entry(root, font=("Arial", 14))
        name_entry.pack(pady=10)

        tk.Label(root, text="תעודת זהות:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        id_entry = tk.Entry(root, font=("Arial", 14))
        id_entry.pack(pady=10)

        tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        book_entry = tk.Entry(root, font=("Arial", 14))
        book_entry.pack(pady=10)

        def add_to_waitlist():
            name = name_entry.get()
            id_num = id_entry.get()
            book_name = book_entry.get()
            if name and id_num and book_name:
                LibraryUI.waitlist.append({"name": name, "id": id_num, "book": book_name})
                LibraryUI.show_popup(f"'{name}' נוסף לרשימת ההמתנה עבור '{book_name}'.")
            else:
                LibraryUI.show_popup("נא למלא את כל השדות.")
            LibraryUI.load_main_menu()

        tk.Button(root, text="הוסף לרשימה", command=add_to_waitlist, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
        tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)


    def add_client(self):
        self.view.show_popup("פונקציית הוספת לקוח")
    def add_client_screen(self):
        # הוספת לקוח
        for widget in root.winfo_children():
            widget.destroy()
        root.configure(bg="#f9f9f9")
        tk.Label(root, text="הוספת לקוח", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)

        tk.Label(root, text="שם הלקוח:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
        client_entry = tk.Entry(root, font=("Arial", 14))
        client_entry.pack(pady=10)

        def add_user():
            client_name = client_entry.get()
            if client_name:
                u.User.__init__(client_name)
                LibraryUI.show_popup(f"'{client_name}' נוסף בהצלחה.")
            else:
                LibraryUI.show_popup("נא להזין שם לקוח.")
            LibraryUI.load_main_menu()

        tk.Button(root, text="הוסף לקוח", command=add_user, font=("Arial", 14),
                  bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
        tk.Button(root, text="חזרה", command=LibraryUI.load_main_menu, font=("Arial", 14),
                  bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)


# ---------------- Main ------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("ספרייה")
    root.geometry("600x600")
    root.configure(bg="#f5f5f5")

    model = LibraryDataManager()
    view = LibraryUI(root)
    controller = LibraryController(model, view)

    root.mainloop()








# library = lib.Library()
# books = lib.get_available_books(library)
# users = lib.get_users(library)
# clients = lib.get_clint(library)
# waitlist = []
# borrowed_books  = lib.get_borrowed_books(library)
#
#
# def show_popup(message):
#     popup = tk.Toplevel(root, bg="#f0f0f0")
#     popup.title("הודעה")
#     popup.geometry("300x150")
#     label = tk.Label(popup, text=message, font=("Arial", 14), bg="#f0f0f0", fg="#333")
#     label.pack(expand=True, pady=20)
#     popup.after(1000, popup.destroy)
#
#
# def login(name, password):
#     filename = "users.csv"
#     try:
#         users_df = pd.read_csv(filename, dtype={"id": int, "name": str, "password": str, "level": str})
#     except (FileNotFoundError, pd.errors.EmptyDataError):
#         users_df = pd.DataFrame(columns=["id", "name", "password", "level"])
#     encrypted_password = hashlib.sha256(password.encode()).hexdigest()
#     if not users_df.empty and name in users_df["name"].values:
#         user_data = users_df.loc[(users_df["name"] == name) & (users_df["password"] == encrypted_password)]
#         if not user_data.empty:
#             return True  # התחברות הצליחה
#         return False
#     return False  # התחברות נכשלה
# # פונקציה להתחברות
# def check_login():
#     username = username_entry.get()
#     password = password_entry.get()
#     if login(username,password):
#         show_popup("נכנס בהצלחה!")
#         root.after(1000, load_main_menu)
#     else:
#         show_popup("שם משתמש או סיסמה שגויים.")
#
#
# # תפריט ראשי
# def load_main_menu():
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f5f5f5")
#
#     tk.Label(root, text="תפריט ראשי", font=("Arial", 24), bg="#f5f5f5", fg="#333").pack(pady=20)
#
#     buttons = [
#         ("הוספת ספר", add_book_screen),
#         ("הסרת ספר", remove_book_screen),
#         ("הוספת משתמש", add_user_screen),
#         ("הוספת לקוח", add_client_screen),
#         ("הוסף לרשימת המתנה", add_to_waitlist_screen),
#         ("חפש ספר", search_book_screen),
#         ("השאלת ספר", borrow_book_screen),
#         ("החזרת ספר", return_book_screen),
#     ]
#
#     for text, command in buttons:
#         tk.Button(
#             root, text=text, command=command, font=("Arial", 14), bg="#4CAF50", fg="white",
#             activebackground="#45a049", activeforeground="white", padx=20, pady=10
#         ).pack(pady=10)
# def add_book_screen():
#     # הוספת ספר
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#     tk.Label(root, text="הוספת ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     book_entry = tk.Entry(root, font=("Arial", 14))
#     book_entry.pack(pady=10)
#
#     def check_book():
#         book_name = book_entry.get()
#         if not book_name:
#             show_popup("יש להזין שם ספר.")
#             return
#         if lib.book_exists(book_name):
#             lib.add_copy(book_name)
#             show_popup(f"עותק נוסף נוסף לספר '{book_name}'.")
#             load_main_menu()
#         else:
#             show_extra_fields(book_name)
#
#     def show_extra_fields(book_name):
#         for widget in root.winfo_children():
#             widget.destroy()
#         tk.Label(root, text=f"הוספת ספר חדש: {book_name}", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#         tk.Label(root, text="תאריך הוצאה:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#         date_entry = tk.Entry(root, font=("Arial", 14))
#         date_entry.pack(pady=10)
#
#         tk.Label(root, text="סופר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#         author_entry = tk.Entry(root, font=("Arial", 14))
#         author_entry.pack(pady=10)
#
#         tk.Label(root, text="כמות:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#         quantity_entry = tk.Entry(root, font=("Arial", 14))
#         quantity_entry.pack(pady=10)
#
#         tk.Label(root, text="שנת הוצאה:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#         year_entry = tk.Entry(root, font=("Arial", 14))
#         year_entry.pack(pady=10)
#
#         tk.Label(root, text="category:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#         category_entry = tk.Entry(root, font=("Arial", 14))
#         category_entry.pack(pady=10)
#
#         tk.Label(root, text="name:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#         name_entry = tk.Entry(root, font=("Arial", 14))
#         name_entry.pack(pady=10)
#
#
#         def save_book():
#             date = date_entry.get()
#             author = author_entry.get()
#             quantity = quantity_entry.get()
#             year = year_entry.get()
#             name=name_entry.get()
#             category = category_entry.get()
#
#             if not (date and author and quantity.isdigit() and year.isdigit()):
#                 show_popup("נא למלא את כל השדות בצורה תקינה.")
#                 return
#             book = Book(author, name, year, category, quantity)
#             lib.add_new_book(book)
#             show_popup(f"'{book_name}' נוסף בהצלחה לספרייה.")
#             load_main_menu()
#
#         tk.Button(root, text="שמור ספר", command=save_book, font=("Arial", 14),
#                   bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#         tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#                   bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#
#     tk.Button(root, text="בדוק ספר", command=check_book, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#
#
# def remove_book_screen():
#     # הסרת ספר
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#     tk.Label(root, text="הסרת ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     book_entry = tk.Entry(root, font=("Arial", 14))
#     book_entry.pack(pady=10)
#
#     def remove_book():
#         book_name = book_entry.get()
#         if book_name in books:
#             books[book_name] -= 1
#             if books[book_name] == 0:
#                 del books[book_name]
#             show_popup(f"'{book_name}' הוסר מהספרייה.")
#         else:
#             show_popup("הספר לא נמצא בספרייה.")
#         load_main_menu()
#
#     tk.Button(root, text="הסר ספר", command=remove_book, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=20)
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=10)
#
#

# def add_user_screen():
#     # הוספת משתמש
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#     tk.Label(root, text="הוספת משתמש", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     tk.Label(root, text="שם משתמש:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     username_entry = tk.Entry(root, font=("Arial", 14))
#     username_entry.pack(pady=10)
#
#     tk.Label(root, text="סיסמה:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     password_entry = tk.Entry(root, font=("Arial", 14), show="*")
#     password_entry.pack(pady=10)
#
#     tk.Label(root, text="level", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     level_entry = tk.Entry(root, font=("Arial", 14))
#     level_entry.pack(pady=10)
#
#     def add_user():
#         username = username_entry.get()
#         password = password_entry.get()
#         level=level_entry.get()
#
#         u.User.__init__(username,password,level)
#         show_popup(f"'{username}' נוסף בהצלחה.")
#         load_main_menu()
#
#     tk.Button(root, text="הוסף משתמש", command=add_user, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#

# def add_client_screen():
#     # הוספת לקוח
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#     tk.Label(root, text="הוספת לקוח", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     tk.Label(root, text="שם הלקוח:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     client_entry = tk.Entry(root, font=("Arial", 14))
#     client_entry.pack(pady=10)
#
#     def add_client():
#         client_name = client_entry.get()
#         if client_name:
#             c.Client.__init__(client_name)
#             show_popup(f"'{client_name}' נוסף בהצלחה.")
#         else:
#             show_popup("נא להזין שם לקוח.")
#         load_main_menu()
#
#     tk.Button(root, text="הוסף לקוח", command=add_client, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#
# def search_book_screen():
#     # פונקציה לחיפוש ספר
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#
#     tk.Label(root, text="חפש ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     search_entry = tk.Entry(root, font=("Arial", 14))
#     search_entry.pack(pady=10)
#
#     # רשימת ז'אנרים לדוגמה
#     genres = ["רומן", "מתח", "מדע בדיוני", "פנטזיה", "עיון"]
#     genre_vars = {genre: tk.BooleanVar() for genre in genres}
#
#     # יצירת צ'קבוקסים לז'אנרים
#     tk.Label(root, text="בחר ז'אנרים:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack(pady=5)
#     for genre in genres:
#         tk.Checkbutton(
#             root, text=genre, variable=genre_vars[genre], font=("Arial", 12),
#             bg="#f9f9f9", fg="#333", selectcolor="#f9f9f9", anchor="w"
#         ).pack(anchor="w", padx=20)
#
#     results_list = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
#
#     def search_action():
#         search_query = search_entry.get().lower()
#         selected_genres = [genre for genre, var in genre_vars.items() if var.get()]
#
#         # סינון הספרים לפי החיפוש והז'אנרים שנבחרו
#         filtered_books = [
#             book for book in books.keys()
#             if search_query in book.lower() and
#             (not selected_genres or any(genre in book.lower() for genre in selected_genres))
#         ]
#
#         results_list.delete(0, tk.END)
#         if filtered_books:
#             for book in filtered_books:
#                 results_list.insert(tk.END, book)
#         else:
#             results_list.insert(tk.END, "לא נמצאו ספרים מתאימים.")
#
#     def on_book_select(event):
#         selected = results_list.get(results_list.curselection())
#         borrow_book_screen(selected)
#
#     results_list.bind("<<ListboxSelect>>", on_book_select)
#
#     tk.Button(root, text="חפש", command=search_action, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=10)
#     results_list.pack(pady=10)
#
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#



# def borrow_book_screen(selected_book=""):
#     # פונקציה להשאלת ספר
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#     tk.Label(root, text="השאלת ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     tk.Label(root, text="שם:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     name_entry = tk.Entry(root, font=("Arial", 14))
#     name_entry.pack(pady=10)
#
#     tk.Label(root, text="תעודת זהות:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     id_entry = tk.Entry(root, font=("Arial", 14))
#     id_entry.pack(pady=10)
#
#     tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     book_entry = tk.Entry(root, font=("Arial", 14))
#     book_entry.insert(0, selected_book)  # ממלא את שם הספר אם נבחר מתוך חיפוש
#     book_entry.pack(pady=10)
#
#     def borrow_book():
#         name = name_entry.get()
#         id_num = id_entry.get()
#         book_name = book_entry.get()
#         if name and id_num and book_name:
#             if book_name in books and books[book_name] > 0:
#                 cl=c.Client.__init__(name,id_num)
#                 lib.borrow_book(book_name,cl)
#                 show_popup(f"{name} השאיל את '{book_name}'.")
#                 load_main_menu()
#             else:
#                 show_popup("הספר אינו זמין כרגע.")
#         else:
#             show_popup("יש למלא את כל השדות.")
#
#     tk.Button(root, text="השאל ספר", command=borrow_book, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#
# def return_book_screen():
#     # פונקציה להחזרת ספר
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#     tk.Label(root, text="החזרת ספר", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     tk.Label(root, text="שם:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     name_entry = tk.Entry(root, font=("Arial", 14))
#     name_entry.pack(pady=10)
#
#     tk.Label(root, text="תעודת זהות:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     id_entry = tk.Entry(root, font=("Arial", 14))
#     id_entry.pack(pady=10)
#
#     tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     book_entry = tk.Entry(root, font=("Arial", 14))
#     book_entry.pack(pady=10)
#
#     def return_book():
#         name = name_entry.get()
#         id_num = id_entry.get()
#         book_name = book_entry.get()
#         if name and id_num and book_name:
#             for record in borrowed_books:
#                 if record["name"] == name and record["id"] == id_num and record["book"] == book_name:
#                     borrowed_books.remove(record)
#                     books[book_name] = books.get(book_name, 0) + 1
#                     show_popup(f"{name} החזיר את '{book_name}'.")
#                     load_main_menu()
#                     return
#             show_popup("הרשומה לא נמצאה.")
#         else:
#             show_popup("יש למלא את כל השדות.")
#
#     tk.Button(root, text="החזר ספר", command=return_book, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#
# def add_to_waitlist_screen():
#     # הוספה לרשימת המתנה
#     for widget in root.winfo_children():
#         widget.destroy()
#     root.configure(bg="#f9f9f9")
#     tk.Label(root, text="הוספה לרשימת המתנה", font=("Arial", 20), bg="#f9f9f9", fg="#333").pack(pady=20)
#
#     tk.Label(root, text="שם הלקוח:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     name_entry = tk.Entry(root, font=("Arial", 14))
#     name_entry.pack(pady=10)
#
#     tk.Label(root, text="תעודת זהות:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     id_entry = tk.Entry(root, font=("Arial", 14))
#     id_entry.pack(pady=10)
#
#     tk.Label(root, text="שם הספר:", font=("Arial", 14), bg="#f9f9f9", fg="#555").pack()
#     book_entry = tk.Entry(root, font=("Arial", 14))
#     book_entry.pack(pady=10)
#
#     def add_to_waitlist():
#         name = name_entry.get()
#         id_num = id_entry.get()
#         book_name = book_entry.get()
#         if name and id_num and book_name:
#             waitlist.append({"name": name, "id": id_num, "book": book_name})
#             show_popup(f"'{name}' נוסף לרשימת ההמתנה עבור '{book_name}'.")
#         else:
#             show_popup("נא למלא את כל השדות.")
#         load_main_menu()
#
#     tk.Button(root, text="הוסף לרשימה", command=add_to_waitlist, font=("Arial", 14),
#               bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#     tk.Button(root, text="חזרה", command=load_main_menu, font=("Arial", 14),
#               bg="#f44336", fg="white", activebackground="#d32f2f", padx=20, pady=10).pack(pady=10)
#
#
# # חלון ראשי
# root = tk.Tk()
# root.title("ספרייה")
# root.geometry("600x600")
# root.configure(bg="#f5f5f5")
#
# # מסך התחברות
# frame = tk.Frame(root, padx=20, pady=20, bg="#f5f5f5")
# frame.pack(fill=tk.BOTH, expand=True)
#
# tk.Label(frame, text="שם משתמש:", font=("Arial", 14), bg="#f5f5f5", fg="#555").pack(pady=10)
# username_entry = tk.Entry(frame, font=("Arial", 14))
# username_entry.pack()
#
# tk.Label(frame, text="סיסמה:", font=("Arial", 14), bg="#f5f5f5", fg="#555").pack(pady=10)
# password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
# password_entry.pack()
#
# tk.Button(frame, text="התחבר", command=check_login, font=("Arial", 14),
#           bg="#4CAF50", fg="white", activebackground="#45a049", padx=20, pady=10).pack(pady=20)
#
# root.mainloop()