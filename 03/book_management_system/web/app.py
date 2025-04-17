from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('book_management_system/database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        conn.close()
        flash('書籍已成功添加！')
        return redirect(url_for('index'))

@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        conn = get_db_connection()
        conn.execute('UPDATE books SET title = ?, author = ? WHERE id = ?', (title, author, book_id))
        conn.commit()
        conn.close()
        flash('書籍已成功更新！')
        return redirect(url_for('index'))
    return render_template('update.html', book=book)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash('書籍已成功刪除！')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
