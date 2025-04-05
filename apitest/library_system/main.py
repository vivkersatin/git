import sqlite3
import os

DB_FILE = 'library.db'

def init_db():
    """初始化資料庫，建立表格（如果不存在）"""
    conn = None # 初始化 conn
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                is_borrowed INTEGER DEFAULT 0 -- 0: 可借閱, 1: 已借出
            )
        ''')
        conn.commit()
        print(f"資料庫 {DB_FILE} 初始化完成。")
    except sqlite3.Error as e:
        print(f"資料庫錯誤：{e}")
    finally:
        if conn:
            conn.close()

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    """執行 SQL 查詢的輔助函數"""
    conn = None
    result = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)

        if commit:
            conn.commit()
            result = cursor.lastrowid # 對於 INSERT 操作，返回新插入的 ID
        elif fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"資料庫查詢錯誤：{e}")
        if commit: # 如果是寫入操作出錯，嘗試回滾
             if conn:
                 conn.rollback()
    finally:
        if conn:
            conn.close()
    return result


def add_book():
    """新增一本書籍到資料庫"""
    title = input("請輸入書名：")
    author = input("請輸入作者：")
    isbn = input("請輸入 ISBN：")

    # 檢查 ISBN 是否已存在
    existing_book = execute_query("SELECT isbn FROM books WHERE isbn = ?", (isbn,), fetchone=True)
    if existing_book:
        print(f"錯誤：ISBN {isbn} 已存在，無法新增。")
        return

    query = "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)"
    book_id = execute_query(query, (title, author, isbn), commit=True)

    if book_id:
        print(f"書籍 '{title}' 已成功新增。")
    else:
        print(f"新增書籍 '{title}' 失敗。")


def get_all_books():
    """從資料庫取得所有書籍"""
    query = "SELECT id, title, author, isbn, is_borrowed FROM books ORDER BY title"
    return execute_query(query, fetchall=True)

def list_books():
    """列出所有書籍"""
    books = get_all_books()
    if not books:
        print("目前圖書館沒有任何書籍。")
        return

    print("\n--- 圖書館藏書清單 ---")
    for book in books:
        book_id, title, author, isbn, is_borrowed = book
        status = "已借出" if is_borrowed else "可借閱"
        # 顯示資料庫中的 ID，方便借閱/歸還操作
        print(f"ID: {book_id}, 書名：{title}, 作者：{author}, ISBN：{isbn}, 狀態：{status}")
    print("----------------------")

def search_book():
    """根據書名或 ISBN 查詢書籍"""
    query_term = input("請輸入要查詢的書名或 ISBN：").strip()
    # 使用 LIKE 進行模糊查詢書名，使用 = 精確查詢 ISBN
    search_query = """
        SELECT id, title, author, isbn, is_borrowed
        FROM books
        WHERE title LIKE ? OR isbn = ?
        ORDER BY title
    """
    # 為 LIKE 查詢添加萬用字元 %
    found_books = execute_query(search_query, (f'%{query_term}%', query_term), fetchall=True)

    if not found_books:
        print(f"找不到符合 '{query_term}' 的書籍。")
    else:
        print("\n--- 查詢結果 ---")
        for book in found_books:
            book_id, title, author, isbn, is_borrowed = book
            status = "已借出" if is_borrowed else "可借閱"
            print(f"ID: {book_id}, 書名：{title}, 作者：{author}, ISBN：{isbn}, 狀態：{status}")
        print("----------------")

def update_borrow_status(book_id, borrow_status):
    """更新書籍的借閱狀態"""
    query = "UPDATE books SET is_borrowed = ? WHERE id = ?"
    execute_query(query, (borrow_status, book_id), commit=True)

def borrow_book():
    """借閱書籍"""
    list_books() # 先列出所有書籍及其 ID
    books = get_all_books() # 獲取書籍列表以檢查狀態
    if not books:
        return

    try:
        book_id_to_borrow = int(input("請輸入要借閱的書籍 ID："))
        # 從獲取的書籍列表中查找對應 ID 的書籍信息
        target_book = next((book for book in books if book[0] == book_id_to_borrow), None)

        if target_book:
            book_id, title, author, isbn, is_borrowed = target_book
            if is_borrowed:
                print(f"錯誤：書籍 '{title}' (ID: {book_id}) 已被借出。")
            else:
                update_borrow_status(book_id, 1) # 1 代表已借出
                print(f"書籍 '{title}' (ID: {book_id}) 已成功借出。")
        else:
            print("錯誤：無效的書籍 ID。")
    except ValueError:
        print("錯誤：請輸入有效的數字 ID。")


def list_borrowed_books():
     """列出已借出的書籍"""
     query = "SELECT id, title, author, isbn FROM books WHERE is_borrowed = 1 ORDER BY title"
     borrowed_books = execute_query(query, fetchall=True)
     return borrowed_books

def return_book():
    """歸還書籍"""
    borrowed_books = list_borrowed_books()
    if not borrowed_books:
        print("目前沒有任何書籍被借出。")
        return

    print("\n--- 已借出書籍清單 ---")
    for book in borrowed_books:
        book_id, title, author, isbn = book
        print(f"ID: {book_id}, 書名：{title}, 作者：{author}, ISBN：{isbn}")
    print("----------------------")

    try:
        book_id_to_return = int(input("請輸入要歸還的書籍 ID："))
        # 檢查輸入的 ID 是否在已借出書籍列表中
        if any(book[0] == book_id_to_return for book in borrowed_books):
             # 獲取書名用於提示信息
             book_details = execute_query("SELECT title FROM books WHERE id = ?", (book_id_to_return,), fetchone=True)
             book_title = book_details[0] if book_details else f"ID {book_id_to_return}"

             update_borrow_status(book_id_to_return, 0) # 0 代表可借閱
             print(f"書籍 '{book_title}' (ID: {book_id_to_return}) 已成功歸還。")
        else:
            print("錯誤：無效的書籍 ID 或該書籍未被借出。")
    except ValueError:
        print("錯誤：請輸入有效的數字 ID。")


def main_menu():
    """顯示主選單並處理使用者輸入"""
    while True:
        print("\n===== 圖書管理系統 (SQLite) =====")
        print("1. 新增書籍")
        print("2. 列出所有書籍")
        print("3. 查詢書籍")
        print("4. 借閱書籍")
        print("5. 歸還書籍")
        print("6. 離開系統")
        print("================================")

        choice = input("請選擇操作 (1-6)：")

        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            borrow_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            print("感謝使用圖書管理系統，再見！")
            break
        else:
            print("無效的選擇，請重新輸入。")

if __name__ == "__main__":
    # 確保資料庫檔案所在的目錄存在 (如果 DB_FILE 包含路徑)
    db_dir = os.path.dirname(DB_FILE)
    if db_dir and not os.path.exists(db_dir):
         os.makedirs(db_dir)

    init_db() # 初始化資料庫
    main_menu()
