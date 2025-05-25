@echo off
REM IAM-HR集成環境 Windows安裝腳本

echo ==========================================
echo  IAM與人事系統串接環境 - Windows安裝腳本
echo ==========================================

REM 檢查Docker是否已安裝
echo 檢查Docker安裝...
docker --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] Docker未安裝或未運行
    echo 請訪問 https://www.docker.com/products/docker-desktop/ 安裝Docker Desktop for Windows
    echo 安裝後請重新運行此腳本
    exit /b
)

REM 檢查Docker Compose是否已安裝
echo 檢查Docker Compose安裝...
docker-compose --version > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [錯誤] Docker Compose未安裝
    echo Docker Desktop for Windows應包含Docker Compose
    echo 請確認Docker Desktop安裝正確並重新運行此腳本
    exit /b
)

echo [信息] Docker環境檢查完成

REM 創建必要的目錄結構
echo 創建目錄結構...
if not exist nginx\conf.d mkdir nginx\conf.d
if not exist nginx\certs mkdir nginx\certs
if not exist scripts mkdir scripts

REM 複製配置文件
echo 複製配置文件...
copy nginx-config nginx\conf.d\default.conf
copy sync_users.py scripts\

REM 啟動環境
echo 啟動Docker環境...
docker-compose up -d

echo 等待服務初始化，這可能需要幾分鐘...
timeout /t 30

REM 檢查服務運行狀態
echo 檢查服務運行狀態...
docker ps

echo ==========================================
echo 環境設置完成！
echo 訪問Keycloak: http://localhost:8080
echo - 用戶名: admin
echo - 密碼: admin
echo 訪問OrangeHRM: http://localhost:8081
echo - 用戶名: admin
echo - 密碼: admin123
echo ==========================================

echo 要運行同步腳本，請使用以下命令:
echo docker run --rm -v "%CD%\scripts:/scripts" --network iam-hr-network python:3.9-slim python /scripts/sync_users.py
echo ==========================================