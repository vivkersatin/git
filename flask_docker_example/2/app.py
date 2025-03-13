from flask import Flask, request, jsonify

app = Flask(__name__)

# 模擬一個數據庫
data = {
    "1": {"name": "Alice", "age": 30},
    "2": {"name": "Bob", "age": 25}
}

# GET：獲取數據
@app.route('/data/<id>', methods=['GET'])
def get_data(id):
    if id in data:
        return jsonify(data[id])
    else:
        return jsonify({"error": "Not found"}), 404

# POST：向伺服器發送數據
@app.route('/data', methods=['POST'])
def add_data():
    new_id = str(len(data) + 1)
    new_data = request.get_json()
    data[new_id] = new_data
    return jsonify({"id": new_id}), 201

# PUT：更新現有數據
@app.route('/data/<id>', methods=['PUT'])
def update_data(id):
    if id in data:
        updated_data = request.get_json()
        data[id].update(updated_data)
        return jsonify(data[id])
    else:
        return jsonify({"error": "Not found"}), 404

# DELETE：刪除數據
@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    if id in data:
        del data[id]
        return jsonify({"message": "Deleted successfully"})
    else:
        return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0')
