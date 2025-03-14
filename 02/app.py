from flask import Flask, jsonify, request

app = Flask(__name__)

# 模擬資料庫，用於儲存待辦事項
todos = [
    {
        'id': 1,
        'description': '學習 REST API',
        'completed': False
    },
    {
        'id': 2,
        'description': '使用 Flask 實作 API',
        'completed': True
    }
]

# GET /todos
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# GET /todos/{id}
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if todo:
        return jsonify(todo)
    else:
        return jsonify({'message': '待辦事項未找到'}), 404

# POST /todos
@app.route('/todos', methods=['POST'])
def create_todo():
    if not request.json or 'description' not in request.json:
        return jsonify({'message': '請求格式錯誤'}), 400
    new_todo = {
        'id': len(todos) + 1,
        'description': request.json['description'],
        'completed': False
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# PUT /todos/{id}
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = next((todo for todo in todos if todo['id'] == todo_id), None)
    if not todo:
        return jsonify({'message': '待辦事項未找到'}), 404
    if not request.json:
        return jsonify({'message': '請求格式錯誤'}), 400
    if 'description' in request.json:
        todo['description'] = request.json['description']
    if 'completed' in request.json:
        todo['completed'] = request.json['completed']
    return jsonify(todo)

# DELETE /todos/{id}
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos  # 声明使用全局变量
    todos = [todo for todo in todos if todo['id'] != todo_id]
    return jsonify({'message': '待辦事項已刪除'})

if __name__ == '__main__':
    app.run(debug=True)
