from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os

app = Flask(__name__, template_folder='templates', static_folder='templates')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates'), filename)

def init_db():
    with sqlite3.connect('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            author TEXT NOT NULL,
                            year INTEGER NOT NULL
                        )''')
        conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books', methods=['GET'])
def get_books():
    with sqlite3.connect('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    with sqlite3.connect('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                       (data['title'], data['author'], data['year']))
        conn.commit()
    return jsonify({'message': 'Book added successfully!'}), 201

@app.route('/add-book', methods=['GET', 'POST'])
def add_book_page():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                           (title, author, year))
            conn.commit()
        return render_template('add_book.html', message='Book added successfully!')

    return render_template('add_book.html')

@app.route('/view-books', methods=['GET'])
def view_books_page():
    with sqlite3.connect('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()
    return render_template('view_books.html', books=books)

@app.route('/update-book', methods=['GET', 'POST'])
def update_book_page():
    if request.method == 'POST':
        book_id = request.form['book']
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?',
                           (title, author, year, book_id))
            conn.commit()
        return render_template('update_book.html', message='Book updated successfully!', books=get_books_list())

    return render_template('update_book.html', books=get_books_list())

@app.route('/delete-book', methods=['GET', 'POST'])
def delete_book_page():
    if request.method == 'POST':
        book_id = request.form['book']
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
        return render_template('delete_book.html', message='Book deleted successfully!', books=get_books_list())

    return render_template('delete_book.html', books=get_books_list())

def get_books_list():
    with sqlite3.connect('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author, year FROM books')
        return cursor.fetchall()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)