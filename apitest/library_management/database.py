import sqlite3

def create_connection():
    conn = sqlite3.connect('library.db')
    return conn

def create_table(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,author TEXT NOT NULL,isbn TEXT NOT NULL);''')

def insert_sample_data(conn):
    for i in range(1, 101):
        conn.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",(f"Book {i}", f"Author {i}", f"ISBN-{i:03d}"))
    conn.commit()

def get_all_books(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    return cur.fetchall()

if __name__ == "__main__":
    conn = create_connection()
    create_table(conn)
    insert_sample_data(conn)
    conn.close()
