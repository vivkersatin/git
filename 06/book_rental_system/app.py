from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json

app = Flask(__name__)

# IAM系統的URL
IAM_URL = "http://localhost:5002"
# 人事系統的URL
HR_URL = "http://localhost:5000"
# 圖書管理系統的URL
LIBRARY_URL = "http://localhost:5001"

# 存儲用戶token
user_tokens = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            response = requests.post(f"{IAM_URL}/login", data={'username': username, 'password': password})
            if response.status_code == 200:
                # 從HTML響應中提取token
                token_start = response.text.find('<textarea readonly class="token-box">') + 37
                token_end = response.text.find('</textarea>', token_start)
                if token_start != -1 and token_end != -1:
                    token = response.text[token_start:token_end].strip()
                    if token:
                        user_tokens[username] = token
                        return redirect(url_for('rent_book'))
                return f"登錄失敗：無法從響應中提取token - {response.text[:200]}", 401
            else:
                return "登錄失敗", response.status_code
        except requests.exceptions.RequestException as e:
            return f"登錄失敗：連接錯誤 - {str(e)}", 503
    return render_template('login.html')

@app.route('/rent_book', methods=['GET', 'POST'])
def rent_book():
    if request.method == 'POST':
        username = request.form.get('username', '')
        book_id = request.form.get('book_id', '')
        if not username or username not in user_tokens:
            return redirect(url_for('login'))
        token = user_tokens[username]
        
        # 驗證用戶資格
        try:
            hr_response = requests.get(f"{HR_URL}/check_user/{username}", headers={'Authorization': f'Bearer {token}'})
            if hr_response.status_code != 200:
                error_detail = hr_response.text if hr_response.text else "無詳細錯誤信息"
                return f"用戶資格驗證失敗，狀態碼: {hr_response.status_code}，詳細信息: {error_detail}", 403
        except requests.exceptions.RequestException as e:
            return f"用戶資格驗證失敗：連接錯誤 - {str(e)}", 503
        
        # 租書
        try:
            library_response = requests.post(f"{LIBRARY_URL}/borrow_book", data={'user_name': username, 'book_id': book_id, 'borrow_date': '2025-04-19'}, headers={'Authorization': f'Bearer {token}'})
            if library_response.status_code == 200:
                return "租書成功", 200
            else:
                error_detail = library_response.text if library_response.text else "無詳細錯誤信息"
                return f"租書失敗，狀態碼: {library_response.status_code}，詳細信息: {error_detail}", 400
        except requests.exceptions.RequestException as e:
            return f"租書失敗：連接錯誤 - {str(e)}", 503
    else:
        # 獲取書籍列表
        books = []
        error_message = ""
        test_message = ""
        current_user = ""
        for user in user_tokens:
            current_user = user
            break
        try:
            library_response = requests.get(f"{LIBRARY_URL}/books")
            if library_response.status_code == 200:
                # 處理文本響應
                response_text = library_response.text
                books = []
                lines = response_text.split('\n')
                for line in lines:
                    if line.startswith('ID:'):
                        parts = line.split(', ')
                        if len(parts) == 4:
                            try:
                                book_id = int(parts[0].split(': ')[1])
                                title = parts[1].split(': ')[1]
                                author = parts[2].split(': ')[1]
                                status = parts[3].split(': ')[1]
                                books.append({'id': book_id, 'title': title, 'author': author, 'status': status})
                            except (IndexError, ValueError):
                                pass
                if not books:
                    error_message = "無法從響應中提取書籍列表數據"
            else:
                error_message = f"獲取書籍列表失敗，狀態碼: {library_response.status_code}"
                books = []
                # 嘗試訪問測試端點
                try:
                    test_response = requests.get(f"{LIBRARY_URL}/test")
                    if test_response.status_code == 200:
                        test_message = f"圖書管理系統測試端點響應: {test_response.text}"
                    else:
                        test_message = f"圖書管理系統測試端點失敗，狀態碼: {test_response.status_code}"
                except requests.exceptions.RequestException as te:
                    test_message = f"訪問圖書管理系統測試端點時發生連接錯誤: {str(te)}"
        except requests.exceptions.RequestException as e:
            error_message = f"獲取書籍列表時發生連接錯誤: {str(e)}"
            books = []
        return render_template('rent_book.html', books=books, error_message=error_message, test_message=test_message, current_user=current_user)

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        username = request.form['username']
        book_id = request.form['book_id']
        if username not in user_tokens:
            return redirect(url_for('login'))
        token = user_tokens[username]
        
        # 還書
        try:
            library_response = requests.post(f"{LIBRARY_URL}/return_book", data={'username': username, 'book_id': book_id}, headers={'Authorization': f'Bearer {token}'})
            if library_response.status_code == 200:
                try:
                    return jsonify(library_response.json())
                except ValueError:
                    return "還書失敗：無法解析響應數據", 500
            else:
                return "還書失敗", 400
        except requests.exceptions.RequestException as e:
            return f"還書失敗：連接錯誤 - {str(e)}", 503
    return render_template('return_book.html')

@app.route('/api/get_token', methods=['POST'])
def get_token():
    username = request.json['username']
    password = request.json['password']
    try:
        response = requests.post(f"{IAM_URL}/login", data={'username': username, 'password': password})
        if response.status_code == 200:
            # 從HTML響應中提取token
            token_start = response.text.find('<textarea readonly class="token-box">') + 37
            token_end = response.text.find('</textarea>', token_start)
            if token_start != -1 and token_end != -1:
                token = response.text[token_start:token_end].strip()
                if token:
                    user_tokens[username] = token
                    return jsonify({'token': token})
            return jsonify({'error': f'登錄失敗：無法從響應中提取token - {response.text[:200]}'}), 401
        else:
            return jsonify({'error': '登錄失敗'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'登錄失敗：連接錯誤 - {str(e)}'}), 503

@app.route('/api/check_user', methods=['GET'])
def check_user():
    username = request.args.get('username')
    if username not in user_tokens:
        return jsonify({'error': '用戶未登錄'}), 401
    token = user_tokens[username]
    try:
        hr_response = requests.get(f"{HR_URL}/check_user/{username}", headers={'Authorization': f'Bearer {token}'})
        if hr_response.status_code == 200:
            try:
                return jsonify(hr_response.json())
            except ValueError:
                return jsonify({'error': '用戶資格驗證失敗：無法解析響應數據'}), 500
        else:
            return jsonify({'error': '用戶資格驗證失敗'}), 403
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'用戶資格驗證失敗：連接錯誤 - {str(e)}'}), 503

@app.route('/api/rent_book', methods=['POST'])
def api_rent_book():
    username = request.json['username']
    book_id = request.json['book_id']
    if username not in user_tokens:
        return jsonify({'error': '用戶未登錄'}), 401
    token = user_tokens[username]
    
    try:
        hr_response = requests.get(f"{HR_URL}/check_user/{username}", headers={'Authorization': f'Bearer {token}'})
        if hr_response.status_code != 200:
            return jsonify({'error': '用戶資格驗證失敗'}), 403
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'用戶資格驗證失敗：連接錯誤 - {str(e)}'}), 503
    
    try:
        library_response = requests.post(f"{LIBRARY_URL}/borrow_book", data={'username': username, 'book_id': book_id}, headers={'Authorization': f'Bearer {token}'})
        if library_response.status_code == 200:
            try:
                return jsonify(library_response.json())
            except ValueError:
                return jsonify({'error': '租書失敗：無法解析響應數據'}), 500
        else:
            return jsonify({'error': '租書失敗'}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'租書失敗：連接錯誤 - {str(e)}'}), 503

@app.route('/api/return_book', methods=['POST'])
def api_return_book():
    username = request.json['username']
    book_id = request.json['book_id']
    if username not in user_tokens:
        return jsonify({'error': '用戶未登錄'}), 401
    token = user_tokens[username]
    
    try:
        library_response = requests.post(f"{LIBRARY_URL}/return_book", data={'username': username, 'book_id': book_id}, headers={'Authorization': f'Bearer {token}'})
        if library_response.status_code == 200:
            try:
                return jsonify(library_response.json())
            except ValueError:
                return jsonify({'error': '還書失敗：無法解析響應數據'}), 500
        else:
            return jsonify({'error': '還書失敗'}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'還書失敗：連接錯誤 - {str(e)}'}), 503

if __name__ == '__main__':
    app.run(debug=True, port=5004)
