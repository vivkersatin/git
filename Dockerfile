# 使用官方 Python 映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製當前目錄內容到工作目錄
COPY . /app

# 安裝所需的 Python 套件
RUN pip install flask

# 暴露 Flask 預設的埠
EXPOSE 5000

# 設定啟動命令
CMD ["python", "1234.py"]
