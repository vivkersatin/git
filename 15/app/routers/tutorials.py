from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter()

# 教程首頁
@router.get("/", response_class=HTMLResponse)
async def tutorials_home():
    return """
    <html>
        <head>
            <title>REST API 教程</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                h1, h2 { color: #2c3e50; }
                .tutorial { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
                .code-block { background: #2d2d2d; color: #f8f8f2; padding: 10px; border-radius: 3px; font-family: monospace; }
            </style>
        </head>
        <body>
            <h1>REST API 基礎教程</h1>
            
            <div class="tutorial">
                <h2>1. HTTP 方法</h2>
                <p>REST API 使用標準 HTTP 方法進行操作：</p>
                <ul>
                    <li><strong>GET</strong> - 獲取資源</li>
                    <li><strong>POST</strong> - 創建新資源</li>
                    <li><strong>PUT</strong> - 更新現有資源</li>
                    <li><strong>DELETE</strong> - 刪除資源</li>
                </ul>
            </div>
            
            <div class="tutorial">
                <h2>2. 狀態碼</h2>
                <p>API 響應包含狀態碼表示操作結果：</p>
                <div class="code-block">
                    200 OK - 請求成功<br>
                    201 Created - 資源創建成功<br>
                    400 Bad Request - 客戶端錯誤<br>
                    404 Not Found - 資源不存在<br>
                    500 Internal Server Error - 伺服器錯誤
                </div>
            </div>
            
            <div class="tutorial">
                <h2>3. 請求與響應格式</h2>
                <p>現代 REST API 通常使用 JSON 格式：</p>
                <div class="code-block">
                    // 請求範例<br>
                    POST /items<br>
                    Content-Type: application/json<br>
                    <br>
                    {<br>
                        "name": "新項目",<br>
                        "description": "項目描述"<br>
                    }<br>
                    <br>
                    // 響應範例<br>
                    HTTP/1.1 201 Created<br>
                    {<br>
                        "id": 123,<br>
                        "name": "新項目",<br>
                        "description": "項目描述"<br>
                    }
                </div>
            </div>
        </body>
    </html>
    """

# 詳細教程路由
@router.get("/{topic}")
async def tutorial_detail(topic: str):
    topics = {
        "http-methods": "HTTP方法詳細說明...",
        "status-codes": "狀態碼詳解...",
        "authentication": "API認證機制...",
        "best-practices": "REST API最佳實踐..."
    }
    
    if topic not in topics:
        raise HTTPException(status_code=404, detail="教程主題不存在")
    
    return {"topic": topic, "content": topics[topic]}