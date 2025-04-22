# -*- coding: utf-8 -*-
"""
同系統內網頁跨轉中的Cookie、Session和Token機制
==============================================

這個腳本旨在解釋在同系統內網頁跨轉中，Cookie、Session和Token機制的作用。
這些機制用於在無狀態的HTTP協議中管理用戶狀態和身份驗證，確保用戶在不同頁面之間切換時仍能保持登錄狀態或訪問權限。

作者：Cline
日期：2025年4月22日
"""

from flask import Flask, request, make_response, session, jsonify, redirect, url_for, render_template_string
import jwt
import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用於session加密的密鑰

# 模擬數據庫
users = {
    "user1": "password1",
    "user2": "password2"
}

# JWT密鑰
JWT_SECRET_KEY = "my_jwt_secret_key"

# 簡單的HTML模板
login_page = """
<html>
<head><title>登錄頁面</title></head>
<body>
    <h1>登錄</h1>
    <form method="POST" action="{{ url_for('session_login') }}">
        <label>用戶名:</label><input type="text" name="username"><br>
        <label>密碼:</label><input type="password" name="password"><br>
        <input type="submit" value="登錄">
    </form>
</body>
</html>
"""

dashboard_page = """
<html>
<head><title>儀表板</title></head>
<body>
    <h1>歡迎, {{ username }}</h1>
    <p>這是您的儀表板。</p>
    <a href="{{ url_for('session_logout') }}">登出</a>
</body>
</html>
"""

# 1. Cookie在跨頁面中的應用
@app.route('/cookie/set', methods=['GET'])
def set_cookie():
    """
    設置一個cookie，展示如何在客戶端存儲簡單數據。
    Cookie是由服務器設置並存儲在客戶端的小型數據片段，可在不同頁面間共享。
    """
    response = make_response("Cookie已設置")
    response.set_cookie('username', 'user1', max_age=24*60*60)  # 設置cookie，有效期1天
    return response

@app.route('/cookie/get', methods=['GET'])
def get_cookie():
    """
    獲取cookie值，展示如何從客戶端讀取數據。
    """
    username = request.cookies.get('username')
    if username:
        return f"從Cookie中獲取的用戶名：{username}"
    return "未找到Cookie中的用戶名"

# 2. Session在跨頁面中的應用
@app.route('/session/login', methods=['GET', 'POST'])
def session_login():
    """
    模擬用戶登錄並設置session。
    Session是存儲在服務器端的用戶數據，客戶端只保存一個標識符（通常是cookie中的session ID）。
    在不同頁面間，Session可以保持用戶的登錄狀態。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        return "登錄失敗", 401
    return render_template_string(login_page)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    檢查session狀態，展示如何在服務器端驗證用戶身份並顯示用戶專屬頁面。
    """
    if 'username' in session:
        return render_template_string(dashboard_page, username=session['username'])
    return redirect(url_for('session_login'))

@app.route('/session/logout', methods=['GET'])
def session_logout():
    """
    清除session，展示如何終止用戶會話。
    """
    session.pop('username', None)
    return redirect(url_for('session_login'))

# 3. Token在跨頁面中的應用 (使用JWT)
@app.route('/token/login', methods=['POST'])
def token_login():
    """
    模擬用戶登錄並生成JWT token。
    Token是一種自包含的認證機制，包含用戶信息和簽名，無需服務器存儲狀態。
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in users and users[username] == password:
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        }, JWT_SECRET_KEY, algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'error': '登錄失敗'}), 401

@app.route('/token/protected', methods=['GET'])
def token_protected():
    """
    受保護的路由，展示如何驗證JWT token。
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '缺少Token'}), 401
    
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})
        return jsonify({'message': f"歡迎 {data['user']}，Token驗證成功"})
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token已過期'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': '無效的Token'}), 401

@app.route('/', methods=['GET'])
def index():
    """
    根路徑，展示可用的路由和使用說明。
    """
    return """
    <h1>Cookie、Session和Token在同系統內網頁跨轉中的應用</h1>
    <p>歡迎使用這個展示服務器。以下是可用的路由：</p>
    <ul>
        <li><b>Cookie:</b> <a href='/cookie/set'>/cookie/set</a> 和 <a href='/cookie/get'>/cookie/get</a></li>
        <li><b>Session:</b> <a href='/session/login'>/session/login</a>, <a href='/dashboard'>/dashboard</a>, <a href='/session/logout'>/session/logout</a></li>
        <li><b>Token:</b> /token/login (POST) 和 /token/protected (需要Authorization頭)</li>
    </ul>
    <p>您也可以使用命令行工具如curl來測試這些路由。例如：</p>
    <pre>
    # 設置Cookie
    curl -X GET http://127.0.0.1:5002/cookie/set -c cookies.txt
    
    # 獲取Cookie
    curl -X GET http://127.0.0.1:5002/cookie/get -b cookies.txt
    
    # Session登錄
    curl -X POST http://127.0.0.1:5002/session/login -F "username=user1" -F "password=password1" -c cookies.txt
    
    # 檢查Session狀態
    curl -X GET http://127.0.0.1:5002/dashboard -b cookies.txt
    
    # Token登錄
    curl -X POST http://127.0.0.1:5002/token/login -F "username=user1" -F "password=password1"
    </pre>
    <p>在同系統內網頁跨轉中，這些機制的應用如下：</p>
    <ul>
        <li><b>Cookie</b>：用於在客戶端存儲用戶信息，如用戶名或偏好設置，這些信息可以在不同頁面間共享，無需每次都重新輸入。</li>
        <li><b>Session</b>：用於在服務器端存儲用戶狀態，確保用戶在不同頁面間切換時仍能保持登錄狀態。例如，用戶登錄後，可以訪問儀表板頁面而無需再次登錄。</li>
        <li><b>Token</b>：用於無狀態的認證機制，特別是在API調用中。Token可以在不同頁面或不同系統間傳遞，用於驗證用戶身份而無需服務器存儲狀態。</li>
    </ul>
    """

if __name__ == '__main__':
    print("啟動服務器，展示Cookie、Session和Token在同系統內網頁跨轉中的應用...")
    print("訪問以下路由來測試：")
    print("- Cookie: /cookie/set 和 /cookie/get")
    print("- Session: /session/login, /dashboard, /session/logout")
    print("- Token: /token/login 和 /token/protected")
    print("您也可以使用命令行工具如curl來測試，訪問 http://127.0.0.1:5002 查看示例。")
    app.run(debug=True, port=5002)
