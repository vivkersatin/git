# 導入 Flask 和 Flask-SQLAlchemy 相關模組
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 創建 Flask 應用程式實例
app = Flask(__name__)

# 配置 SQLite 資料庫
# 'sqlite:///todos.db' 表示資料庫檔案為 todos.db，儲存在當前目錄
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
# 禁用 SQLAlchemy 的事件追蹤，以提高效能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 創建 SQLAlchemy 實例，並與 Flask 應用程式綁定
db = SQLAlchemy(app)

# 定義 Todo 模型，映射到資料庫中的 todos 表格
class Todo(db.Model):
    # 定義 id 欄位，主鍵，自動遞增
    id = db.Column(db.Integer, primary_key=True)
    # 定義 task 欄位，字串型態，不可為空
    task = db.Column(db.String(200), nullable=False)
    # 定義 completed 欄位，布林值，預設為 False
    completed = db.Column(db.Boolean, default=False)
    # 定義 created_at 欄位，記錄創建時間
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 定義一個方法，將物件轉為字典，方便 JSON 序列化
    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# 創建資料庫表格（僅在應用程式啟動時執行一次）
with app.app_context():
    db.create_all()

# 定義路由：獲取所有待辦事項 (Read - 讀取全部)
@app.route('/todos', methods=['GET'])
def get_todos():
    # 查詢資料庫中的所有 Todo 物件
    todos = Todo.query.all()
    # 將每個 Todo 物件轉為字典並組成列表
    return jsonify([todo.to_dict() for todo in todos])

# 定義路由：根據 ID 獲取單一待辦事項 (Read - 讀取單筆)
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    # 根據 id 查詢 Todo 物件，若不存在則回傳 None
    todo = Todo.query.get(id)
    if todo is None:
        # 如果找不到，回傳 404 錯誤
        return jsonify({"error": "待辦事項不存在"}), 404
    # 將 Todo 物件轉為字典並回傳
    return jsonify(todo.to_dict())

# 定義路由：創建新待辦事項 (Create - 創建)
@app.route('/todos', methods=['POST'])
def create_todo():
    # 從請求中獲取 JSON 資料
    data = request.get_json()
    if not data or 'task' not in data:
        # 如果請求無效，回傳 400 錯誤
        return jsonify({"error": "無效的請求，必須包含 task 欄位"}), 400
    
    # 創建新的 Todo 物件
    todo = Todo(
        task=data['task'],
        completed=data.get('completed', False)  # 預設 completed 為 False
    )
    # 將新物件加入資料庫
    db.session.add(todo)
    # 提交變更到資料庫
    db.session.commit()
    # 回傳新創建的待辦事項及 201 狀態碼
    return jsonify(todo.to_dict()), 201

# 定義路由：更新現有待辦事項 (Update - 更新)
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    # 根據 id 查詢 Todo 物件
    todo = Todo.query.get(id)
    if todo is None:
        return jsonify({"error": "待辦事項不存在"}), 404
    
    # 從請求中獲取 JSON 資料
    data = request.get_json()
    if not data:
        return jsonify({"error": "無效的請求"}), 400
    
    # 更新 Todo 物件的欄位
    todo.task = data.get('task', todo.task)
    todo.completed = data.get('completed', todo.completed)
    # 提交變更到資料庫
    db.session.commit()
    # 回傳更新後的待辦事項
    return jsonify(todo.to_dict())

# 定義路由：刪除待辦事項 (Delete - 刪除)
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    # 根據 id 查詢 Todo 物件
    todo = Todo.query.get(id)
    if todo is None:
        return jsonify({"error": "待辦事項不存在"}), 404
    
    # 從資料庫中刪除該物件
    db.session.delete(todo)
    # 提交變更到資料庫
    db.session.commit()
    # 回傳成功訊息
    return jsonify({"message": "待辦事項已刪除"})

# 啟動 Flask 應用程式
if __name__ == '__main__':
    app.run(debug=True)