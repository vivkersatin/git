# 使用官方 Python 基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄內容到工作目錄
COPY . /app

# 安裝 Flask
RUN pip install Flask

# 指定容器啟動時運行的命令
CMD ["python", "app.py"]
