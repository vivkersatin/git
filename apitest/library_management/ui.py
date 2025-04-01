import tkinter as tk
from database import add_book, delete_book, search_book, get_all_books

class LibraryUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Title:")
        self.title_label.grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.master)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.author_label = tk.Label(self.master, text="Author:")
        self.author_label.grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(self.master)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.master, text="Add Book", command=self.add_book)
        self.add_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.search_label = tk.Label(self.master, text="Search:")
        self.search_label.grid(row=3, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=3, column=1, padx=5, pady=5)

        self.search_button = tk.Button(self.master, text="Search", command=self.search_book)
        self.search_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.list_button = tk.Button(self.master, text="List All Books", command=self.list_books)
        self.list_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.delete_label = tk.Label(self.master, text="Delete by ID:")
        self.delete_label.grid(row=6, column=0, padx=5, pady=5)
        self.delete_entry = tk.Entry(self.master)
        self.delete_entry.grid(row=6, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.master, text="Delete Book", command=self.delete_book)
        self.delete_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        if title and author:
            add_book(title, author)
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.list_books()

    def delete_book(self):
        book_id = self.delete_entry.get()
        if book_id:
            delete_book(book_id)
            self.delete_entry.delete(0, tk.END)
            self.list_books()

    def search_book(self):
        query = self.search_entry.get()
        if query:
            books = search_book(query)
            self.display_books(books)

    def list_books(self):
        books = get_all_books()
        self.display_books(books)

    def display_books(self, books):
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Listbox):
                widget.destroy()

        listbox = tk.Listbox(self.master, width=50)
        listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

        for book in books:
            listbox.insert(tk.END, f"ID: {book['id']} - Title: {book['title']} - Author: {book['author']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryUI(root)
    root.mainloop()
