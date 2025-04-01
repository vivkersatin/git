import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# 連接到 SQLite 數據庫
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

# 創建書籍表
def create_table():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT)')
    conn.commit()
    conn.close()

# 添加書籍
@app.route('/add', methods=['POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

# 刪除書籍
@app.route('/delete/<int:book_id>', methods=['GET'])
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 搜索書籍
@app.route('/search', methods=['GET'])
def search_book():
    query = request.args.get('query', '')
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ?', ('%' + query + '%', '%' + query + '%')).fetchall()
    conn.close()
    return render_template('index.html', books=books, query=query)

# 首頁
@app.route('/')
def index():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('index.html', books=books)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
