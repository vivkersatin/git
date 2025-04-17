import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# 创建书籍表
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER
)
''')

# 函数：添加书籍
def add_book(title, author, year):
    cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    conn.commit()
    print(f"已添加书籍: {title} by {author}")

# 函数：列出所有书籍
def list_books():
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    for book in books:
        print(f"ID: {book[0]}, 书名: {book[1]}, 作者: {book[2]}, 年份: {book[3]}")

# 函数：删除书籍
def delete_book(book_id):
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    print(f"已成功删除ID为 {book_id} 的书籍")

def update_book(book_id, title=None, author=None, year=None):
    update_query = "UPDATE books SET "
    params = []
    if title:
        update_query += "title = ?, "
        params.append(title)
    if author:
        update_query += "author = ?, "
        params.append(author)
    if year:
        update_query += "year = ?, "
        params.append(year)
    if params:
        update_query = update_query.rstrip(", ") + " WHERE id = ?"
        params.append(book_id)
        cursor.execute(update_query, tuple(params))
        conn.commit()
        print(f"已成功更新ID为 {book_id} 的书籍")
    else:
        print("没有提供更新信息")
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    print(f"已删除ID为 {book_id} 的书籍")

def search_book(keyword):
    cursor.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ?', ('%' + keyword + '%', '%' + keyword + '%'))
    books = cursor.fetchall()
    if books:
        for book in books:
            print(f"ID: {book[0]}, 书名: {book[1]}, 作者: {book[2]}, 年份: {book[3]}")
    else:
        print("没有找到匹配的书籍")

def add_book(title, author, year):
    cursor.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)', (title, author, year))
    conn.commit()
    print(f"已成功添加书籍: {title} 作者: {author} 年份: {year}")

def delete_book(book_id):
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    print(f"已成功删除ID为 {book_id} 的书籍")

def search_book(keyword):
    cursor.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ?', ('%' + keyword + '%', '%' + keyword + '%'))
    books = cursor.fetchall()
    if books:
        for book in books:
            print(f"ID: {book[0]}, 書名: {book[1]}, 作者: {book[2]}, 年份: {book[3]}")
    else:
        print("沒有找到匹配的書籍")
# 示例使用
if __name__ == "__main__":
    add_book("Python Crash Course", "Eric Matthes", 2019)
    add_book("Automate the Boring Stuff with Python", "Al Sweigart", 2015)
    list_books()
    delete_book(1)
    list_books()

# 关闭数据库连接
conn.close()
