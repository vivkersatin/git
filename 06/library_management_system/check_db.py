import sqlite3
import os

def check_database():
    db_path = 'library.db'
    if not os.path.exists(db_path):
        print(f"數據庫文件 {db_path} 不存在。")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = c.fetchall()
        print(f"數據庫中找到的表: {tables}")
        if tables:
            for table in tables:
                table_name = table[0]
                c.execute(f"SELECT * FROM {table_name} LIMIT 1;")
                columns = [description[0] for description in c.description]
                print(f"表 {table_name} 的欄位: {columns}")
        else:
            print("數據庫中未找到任何表。")
        conn.close()
        return True
    except Exception as e:
        print(f"訪問數據庫時發生錯誤: {str(e)}")
        return False

if __name__ == "__main__":
    if check_database():
        print("數據庫檢查成功。")
    else:
        print("數據庫檢查失敗。")
