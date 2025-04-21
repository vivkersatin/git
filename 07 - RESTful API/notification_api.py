# 模擬的外部通知系統 API
from flask import Flask, jsonify, request
from datetime import datetime

# 創建 Flask 應用程式
app = Flask(__name__)

# 儲存接收到的通知（模擬資料庫）
notifications = []

# 定義路由：接收通知
@app.route('/notify', methods=['POST'])
def receive_notification():
    try:
        # 獲取 JSON 資料
        data = request.get_json()
        if not data or 'event' not in data or 'todo' not in data:
            return jsonify({"error": "無效的請求，必須包含 event 和 todo 欄位"}), 400
        
        # 記錄通知
        notification = {
            'event': data['event'],
            'todo': data['todo'],
            'received_at': datetime.utcnow().isoformat()
        }
        notifications.append(notification)
        
        # 回傳成功訊息
        return jsonify({"message": "通知已接收", "notification": notification}), 200
    except Exception as e:
        return jsonify({"error": f"處理通知失敗: {str(e)}"}), 500

# 定義路由：查看所有通知（用於測試）
@app.route('/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications)

# 啟動應用程式，運行在端口 5001
if __name__ == '__main__':
    app.run(port=5001, debug=True)