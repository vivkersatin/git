from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import jwt
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'
SECRET_KEY = 'your-secret-key-for-jwt'

# 初始化數據庫
def init_db():
    conn = sqlite3.connect('iam.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('iam.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error="用戶名已存在")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('iam.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            token = jwt.encode({
                'user_id': user[0],
                'username': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            return render_template('token.html', token=token)
        else:
            return render_template('login.html', error="用戶名或密碼錯誤")
    return render_template('login.html')

@app.route('/verify_token', methods=['POST'])
def verify_token():
    token = request.form.get('token')
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'valid': True, 'decoded': decoded_token})
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False, 'error': 'Token已過期'})
    except jwt.InvalidTokenError:
        return jsonify({'valid': False, 'error': '無效的Token'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5002)
