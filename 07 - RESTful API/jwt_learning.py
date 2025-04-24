import jwt
import time
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 確保 JSON 回應使用 UTF-8 編碼
app.config['TEMPLATES_AUTO_RELOAD'] = True  # 自動重新載入模板

# JWT 基礎介紹
# JWT 由三部分組成：Header, Payload, Signature
# Header: 指定演算法和類型
# Payload: 包含聲明，例如用戶ID、到期時間
# Signature: 用來驗證Token的完整性
# 進階：處理過期 Token 和用戶登入
# 實際運用：使用 Token 來保護資源，例如 /protected 端點，只允許特定 user_id 訪問
# 如何在另一個系統驗證 Token：在另一個系統中，使用相同的 secret_key 來解碼 Token，並檢查 user_id 是否等於 allowed_user_id。如果是的，則允許訪問；否則，拒絕。
# 如果對方系統不可改寫：您可以建立一個中介系統來處理驗證，然後與對方系統整合。例如，創建一個 API 來驗證 Token，並在對方系統中呼叫這個 API。
# 範例：以下是另一個系統的簡單驗證程式範例（靜態代碼，不可修改的範例）：

allowed_user_id = 'authorized_user'  # 設定允許的 user_id，僅此 ID 能訪問受保護資源

def generate_token(user_id):
    payload = {
        'user_id': user_id,  # 範例用戶ID
        'exp': time.time() + 3600  # 到期時間，1小時後
    }
    secret_key = 'your_secret_key'  # 應在實際應用中安全儲存
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_token(token):
    try:
        secret_key = 'your_secret_key'
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        if decoded['exp'] < time.time():
            return None  # Token 已過期
        return decoded
    except:
        return None

# 網頁路由
@app.route('/')
def home():
    return """
    <h1>歡迎使用 JWT 學習應用程式</h1>
    <p>要生成 Token，請訪問 <a href='/generate?user_id=your_user_id'>/generate?user_id=your_user_id</a>。例如：<a href='/generate?user_id=test_user'>/generate?user_id=test_user</a></p>
    <p>要模擬登入，請訪問 <a href='/login'>/login</a>。這會生成一個固定 user_id 的 Token。</p>
    <p>差異說明：</p>
    <ul>
        <li>/generate：允許您指定自定義 user_id，因此每個 Token 可以有不同的 user_id。請在 URL 中添加 ?user_id=您的ID，例如 /generate?user_id=test_user。</li>
        <li>/login：使用固定的 user_id ('user_from_login')，模擬標準登入流程，不需要額外參數。</li>
    </ul>
    <p>實際運用範例：要訪問受保護資源，請先生成 Token，然後訪問 <a href='/protected?token=your_token'>/protected?token=your_token</a>。只有使用特定 user_id ('authorized_user') 生成的 Token 才能訪問。</p>
    <p>如何在另一個系統驗證 Token：在另一個系統中，使用相同的 secret_key 來解碼 Token，並檢查 user_id 是否等於 'authorized_user'。如果是的，則允許訪問；否則，拒絕。</p>
    <p>如果對方系統不可改寫：您可以建立一個中介系統來處理驗證。以下是範例中介驗證程式（您可以複製到另一個檔案中運行）：</p>
    <pre>
import jwt
import time  # 如果需要處理到期時間

def verify_external_token(token):
    secret_key = 'your_secret_key'  # 使用相同的 secret_key
    try:
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        if decoded['user_id'] == 'authorized_user' and decoded['exp'] > time.time():
            return "訪問允許"  # 呼叫這個函數來驗證 Token
        else:
            return "未授權訪問"
    except:
        return "Token 無效"

# 範例呼叫：
# token = '您的 Token'
# result = verify_external_token(token)
# print(result)  # 輸出：訪問允許 或 未授權訪問
    </pre>
    <p>要展示呼叫 API：您可以運行這個中介程式作為一個簡單的 Script，然後從這個應用程式中模擬呼叫它（例如，通過輸入 Token 手動驗證）。</p>
    """

@app.route('/generate', methods=['GET'])
def route_generate_token():
    user_id = request.args.get('user_id', '123')  # 從URL獲取user_id
    token = generate_token(user_id)
    return jsonify({"token": token, "user_id": user_id})

@app.route('/verify', methods=['POST'])
def route_verify_token():
    token = request.json.get('token')
    decoded = verify_token(token)
    if decoded:
        return jsonify({"message": "Token 有效", "decoded": decoded})
    else:
        return jsonify({"message": "Token 無效或已過期"}), 401

@app.route('/login', methods=['GET'])
def login():
    # 簡單的登入模擬
    token = generate_token('user_from_login')
    return jsonify({"token": token, "user_id": 'user_from_login'})

@app.route('/protected', methods=['GET'])
def protected():
    token = request.args.get('token')
    decoded = verify_token(token)
    if decoded and decoded['user_id'] == allowed_user_id:
        return jsonify({"message": "歡迎訪問受保護資源", "user_id": decoded['user_id']})
    else:
        return jsonify({"message": "未授權訪問"}), 401

if __name__ == '__main__':
    app.run(debug=True)
