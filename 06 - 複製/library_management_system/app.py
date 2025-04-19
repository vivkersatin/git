from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 初始化數據庫
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                status TEXT DEFAULT '可用')''')
    c.execute('''CREATE TABLE IF NOT EXISTS borrowings
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                user_name TEXT,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books (id))''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)", (title, author, isbn))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        user_name = request.form['user_name']
        borrow_date = request.form['borrow_date']
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("UPDATE books SET status = '已借出' WHERE id = ?", (book_id,))
        c.execute("INSERT INTO borrowings (book_id, user_name, borrow_date) VALUES (?, ?, ?)", (book_id, user_name, borrow_date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('borrow_book.html')

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        return_date = request.form['return_date']
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("UPDATE books SET status = '可用' WHERE id = ?", (book_id,))
        c.execute("UPDATE borrowings SET return_date = ? WHERE book_id = ? AND return_date IS NULL", (return_date, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('return_book.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    c.execute("SELECT * FROM borrowings")
    borrowings = c.fetchall()
    conn.close()
    return render_template('admin.html', books=books, borrowings=borrowings)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
