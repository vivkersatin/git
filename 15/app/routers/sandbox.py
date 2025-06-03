from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import json

router = APIRouter()

class SandboxRequest(BaseModel):
    method: str = "GET"
    path: str = "/"
    headers: dict = {}
    body: dict | None = None

# 沙盒測試頁面
@router.get("/", response_class=HTMLResponse)
async def sandbox_home():
    return """
    <html>
        <head>
            <title>API 測試沙盒</title>
            <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
            <style>
                body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
                .container { display: flex; gap: 20px; }
                .panel { flex: 1; background: #f8f9fa; padding: 15px; border-radius: 5px; }
                .code-block { background: #2d2d2d; color: #f8f8f2; padding: 10px; border-radius: 3px; font-family: monospace; }
                textarea, input { width: 100%; padding: 8px; margin-bottom: 10px; }
                button { background: #4CAF50; color: white; border: none; padding: 10px 15px; cursor: pointer; }
                .response { white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>API 測試沙盒</h1>
            <div class="container">
                <div class="panel">
                    <h2>請求設置</h2>
                    <div>
                        <label>方法:</label>
                        <select id="method">
                            <option>GET</option>
                            <option>POST</option>
                            <option>PUT</option>
                            <option>DELETE</option>
                        </select>
                    </div>
                    <div>
                        <label>路徑:</label>
                        <input type="text" id="path" value="/examples/items">
                    </div>
                    <div>
                        <label>請求頭 (JSON):</label>
                        <textarea id="headers" rows="3">{}</textarea>
                    </div>
                    <div>
                        <label>請求體 (JSON):</label>
                        <textarea id="body" rows="5"></textarea>
                    </div>
                    <button onclick="sendRequest()">發送請求</button>
                </div>
                
                <div class="panel">
                    <h2>響應結果</h2>
                    <div id="response" class="response"></div>
                </div>
            </div>
            
            <script>
                function sendRequest() {
                    const method = document.getElementById('method').value;
                    const path = document.getElementById('path').value;
                    const headers = JSON.parse(document.getElementById('headers').value || '{}');
                    const body = document.getElementById('body').value;
                    
                    const config = {
                        method: method.toLowerCase(),
                        url: path,
                        headers: headers
                    };
                    
                    if (body) {
                        try {
                            config.data = JSON.parse(body);
                        } catch (e) {
                            alert('請求體不是有效的 JSON');
                            return;
                        }
                    }
                    
                    document.getElementById('response').innerHTML = "發送請求中...";
                    
                    axios(config)
                        .then(response => {
                            const formatted = JSON.stringify(response.data, null, 2);
                            document.getElementById('response').innerHTML = 
                                `狀態碼: ${response.status}\n\n${formatted}`;
                        })
                        .catch(error => {
                            let message = "錯誤: ";
                            if (error.response) {
                                message += `狀態碼 ${error.response.status}\n`;
                                message += JSON.stringify(error.response.data, null, 2);
                            } else {
                                message += error.message;
                            }
                            document.getElementById('response').innerHTML = message;
                        });
                }
            </script>
        </body>
    </html>
    """

# 測試API端點
@router.api_route("/test", methods=["GET", "POST", "PUT", "DELETE"])
async def sandbox_test(request: Request):
    # 獲取請求信息
    request_info = {
        "method": request.method,
        "path": request.url.path,
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "body": await request.json() if request.method in ["POST", "PUT"] else None
    }
    
    # 返回模擬響應
    return JSONResponse(content={
        "message": "沙盒測試成功",
        "request": request_info,
        "server_info": {
            "framework": "FastAPI",
            "version": "0.95.0"
        }
    })