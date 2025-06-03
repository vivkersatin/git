from fastapi import FastAPI
from app.core.config import settings
from app.routers import tutorials, examples, sandbox

app = FastAPI(
    title="REST API 學習平台",
    description="互動式 REST API 教學與實作平台",
    version="1.0.0"
)

# 包含核心功能路由
app.include_router(tutorials.router, prefix="/tutorials", tags=["教程"])
app.include_router(examples.router, prefix="/examples", tags=["範例"])
app.include_router(sandbox.router, prefix="/sandbox", tags=["測試沙盒"])

@app.get("/")
async def root():
    return {
        "message": "歡迎使用 REST API 學習平台",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)