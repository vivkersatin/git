from flask import Flask, request, jsonify

# 建立 Flask 應用程式實例
app = Flask(__name__)

# 配置 Flask 的 JSON 編碼，禁用 ASCII 轉義
app.config['JSON_AS_ASCII'] = False

# 創建一個簡單的待辦事項清單（模擬資料庫）
todos = [
    {"id": 1, "task": "學習 Python", "done": False},
    {"id": 2, "task": "完成作業", "done": True}
]

# 路由：讀取所有待辦事項（GET 方法）
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# 路由：根據 ID 讀取單一待辦事項（GET 方法）
@app.route('/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = next((todo for todo in todos if todo['id'] == id), None)
    if todo is None:
        return jsonify({"error": "待辦事項不存在"}), 404
    return jsonify(todo)

# 路由：新增待辦事項（POST 方法）
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "請提供任務內容"}), 400
    new_todo = {
        "id": len(todos) + 1,
        "task": data['task'],
        "done": data.get('done', False)
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# 路由：更新待辦事項（PUT 方法）
@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = next((todo for todo in todos if todo['id'] == id), None)
    if todo is None:
        return jsonify({"error": "待辦事項不存在"}), 404
    data = request.get_json()
    todo['task'] = data.get('task', todo['task'])
    todo['done'] = data.get('done', todo['done'])
    return jsonify(todo)

# 路由：刪除待辦事項（DELETE 方法）
@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos
    todo = next((todo for todo in todos if todo['id'] == id), None)
    if todo is None:
        return jsonify({"error": "待辦事項不存在"}), 404
    todos = [todo for todo in todos if todo['id'] != id]
    return jsonify({"message": "待辦事項已刪除"})

# 啟動 Flask 應用程式
if __name__ == '__main__':
    app.run(debug=True)