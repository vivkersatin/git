from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# 連接到 MySQL 數據庫
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='db',
            user='flask_user',
            password='flask_password',
            database='flask_db'
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# GET：獲取數據
@app.route('/data/<id>', methods=['GET'])
def get_data(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM users WHERE id = {id}")
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Not found"}), 404

# POST：向伺服器發送數據
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.get_json()
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (new_data['name'], new_data['age']))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Created successfully"}), 201

# PUT：更新現有數據
@app.route('/data/<id>', methods=['PUT'])
def update_data(id):
    updated_data = request.get_json()
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET name = %s, age = %s WHERE id = %s", (updated_data['name'], updated_data['age'], id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Updated successfully"}), 200

# DELETE：刪除數據
@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM users WHERE id = {id}")
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Deleted successfully"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
