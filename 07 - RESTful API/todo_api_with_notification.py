# 導入 Flask、Flask-SQLAlchemy 和 requests 模組
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.exceptions import BadRequest, NotFound, MethodNotAllowed
import requests
import logging

# 創建 Flask 應用程式實例
app = Flask(__name__)

# 配置 SQLite 資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置外部通知系統的 URL
NOTIFICATION_API_URL = 'http://127.0.0.1:5001/notify'

# 配置日誌記錄
logging.basicConfig(filename='api_errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 創建 SQLAlchemy 實例
db = SQLAlchemy(app)

# 定義 Todo 模型
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# 自訂錯誤處理函數：統一錯誤回應格式
def error_response(message, status_code):
    return jsonify({
        'error': message,
        'status_code': status_code,
        'timestamp': datetime.utcnow().isoformat()
    }), status_code

# 處理 Flask 的 BadRequest 異常（400）
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return error_response(str(e), 400)

# 處理 Flask 的 NotFound 異常（404）
@app.errorhandler(NotFound)
def handle_not_found(e):
    return error_response("資源不存在", 404)

# 處理 Flask 的 MethodNotAllowed 異常（405）
@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    return error_response("不支援的 HTTP 方法", 405)

# 處理未預期的伺服器錯誤（500）
@app.errorhandler(Exception)
def handle_general_exception(e):
    logging.error(f"未預期錯誤: {str(e)}")
    return error_response("伺服器內部錯誤，請稍後再試", 500)

# 創建資料庫表格
with app.app_context():
    try:
        db.create_all()
    except SQLAlchemyError as e:
        logging.error(f"創建資料庫表格失敗: {str(e)}")
        raise

# 輸入驗證函數
def validate_todo_data(data, require_task=True):
    if not data:
        raise BadRequest("請求資料不可為空")
    if require_task and 'task' not in data:
        raise BadRequest("必須提供 task 欄位")
    if 'task' in data:
        if not isinstance(data['task'], str):
            raise BadRequest("task 必須是字串")
        if len(data['task'].strip()) == 0:
            raise BadRequest("task 不可為空")
        if len(data['task']) > 200:
            raise BadRequest("task 長度不可超過 200 字元")
    if 'completed' in data and not isinstance(data['completed'], bool):
        raise BadRequest("completed 必須是布林值")

# 發送通知到外部系統
def send_notification(event, todo):
    try:
        # 準備通知資料
        notification_data = {
            'event': event,
            'todo': todo
        }
        # 發送 POST 請求到外部通知系統
        response = requests.post(NOTIFICATION_API_URL, json=notification_data, timeout=5)
        response.raise_for_status()  # 如果狀態碼不是 2xx，拋出異常
        return True
    except requests.exceptions.RequestException as e:
        # 記錄錯誤，但不影響主要操作
        logging.error(f"發送通知失敗 (事件: {event}): {str(e)}")
        return False

# 定義路由：獲取所有待辦事項 (Read - 讀取全部)
@app.route('/todos', methods=['GET'])
def get_todos():
    try:
        todos = Todo.query.all()
        return jsonify([todo.to_dict() for todo in todos])
    except SQLAlchemyError as e:
        logging.error(f"資料庫查詢失敗: {str(e)}")
        return error_response(f"資料庫查詢失敗: {str(e)}", 500)

# 定義路由：根據 ID 獲取單一待辦事項 (Read - 讀取單筆)
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    try:
        todo = Todo.query.get(id)
        if todo is None:
            raise NotFound("待辦事項不存在")
        return jsonify(todo.to_dict())
    except SQLAlchemyError as e:
        logging.error(f"資料庫查詢失敗: {str(e)}")
        return error_response(f"資料庫查詢失敗: {str(e)}", 500)

# 定義路由：創建新待辦事項 (Create - 創建)
@app.route('/todos', methods=['POST'])
def create_todo():
    try:
        data = request.get_json()
        validate_todo_data(data)
        
        todo = Todo(
            task=data['task'],
            completed=data.get('completed', False)
        )
        db.session.add(todo)
        db.session.commit()
        
        # 發送通知到外部系統
        todo_dict = todo.to_dict()
        if not send_notification('created', todo_dict):
            logging.warning("通知外部系統失敗，但待辦事項已創建")
        
        return jsonify(todo_dict), 201
    except BadRequest as e:
        return error_response(str(e), 400)
    except IntegrityError:
        db.session.rollback()
        return error_response("資料庫完整性錯誤（例如重複 ID）", 400)
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"資料庫操作失敗: {str(e)}")
        return error_response(f"資料庫操作失敗: {str(e)}", 500)

# 定義路由：更新現有待辦事項 (Update - 更新)
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    try:
        todo = Todo.query.get(id)
        if todo is None:
            raise NotFound("待辦事項不存在")
        
        data = request.get_json()
        validate_todo_data(data, require_task=False)
        
        todo.task = data.get('task', todo.task)
        todo.completed = data.get('completed', todo.completed)
        db.session.commit()
        
        # 發送通知到外部系統
        todo_dict = todo.to_dict()
        if not send_notification('updated', todo_dict):
            logging.warning("通知外部系統失敗，但待辦事項已更新")
        
        return jsonify(todo_dict)
    except BadRequest as e:
        return error_response(str(e), 400)
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"資料庫操作失敗: {str(e)}")
        return error_response(f"資料庫操作失敗: {str(e)}", 500)

# 定義路由：刪除待辦事項 (Delete - 刪除)
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    try:
        todo = Todo.query.get(id)
        if todo is None:
            raise NotFound("待辦事項不存在")
        
        todo_dict = todo.to_dict()  # 先儲存資料以便通知
        db.session.delete(todo)
        db.session.commit()
        
        # 發送通知到外部系統
        if not send_notification('deleted', todo_dict):
            logging.warning("通知外部系統失敗，但待辦事項已刪除")
        
        return jsonify({"message": "待辦事項已刪除"})
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"資料庫操作失敗: {str(e)}")
        return error_response(f"資料庫操作失敗: {str(e)}", 500)

# 啟動 Flask 應用程式
if __name__ == '__main__':
    app.run(debug=True)