#!/bin/bash

# 多操作系統環境設置腳本
# 此腳本檢測操作系統並安裝必要的依賴

# 顏色設定
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 顯示標題
echo -e "${BLUE}===========================================${NC}"
echo -e "${BLUE}  IAM與人事系統串接環境 - 安裝助手    ${NC}"
echo -e "${BLUE}===========================================${NC}"

# 檢測操作系統
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux系統
    echo -e "${BLUE}檢測到Linux操作系統${NC}"
    
    # 檢測發行版
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
        echo -e "${BLUE}發行版: $OS $VER${NC}"
        
        # CentOS安裝流程
        if [[ $OS == *"CentOS"* ]]; then
            echo -e "${YELLOW}正在為CentOS設置環境...${NC}"
            
            # 檢查是否為root用戶
            if [ "$EUID" -ne 0 ]; then
                echo -e "${RED}請使用root權限運行此腳本 (sudo ./os_setup.sh)${NC}"
                exit 1
            fi
            
            # 安裝Docker
            echo -e "${BLUE}安裝Docker...${NC}"
            yum install -y yum-utils
            yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            yum install -y docker-ce docker-ce-cli containerd.io
            
            # 安裝Docker Compose
            echo -e "${BLUE}安裝Docker Compose...${NC}"
            curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            chmod +x /usr/local/bin/docker-compose
            
            # 啟動Docker服務
            echo -e "${BLUE}啟動Docker服務...${NC}"
            systemctl start docker
            systemctl enable docker
            
            # 設定防火牆
            echo -e "${BLUE}設定防火牆...${NC}"
            firewall-cmd --permanent --add-port=8080-8081/tcp
            firewall-cmd --reload
            
        # Ubuntu安裝流程
        elif [[ $OS == *"Ubuntu"* ]]; then
            echo -e "${YELLOW}正在為Ubuntu設置環境...${NC}"
            
            # 檢查是否為root用戶
            if [ "$EUID" -ne 0 ]; then
                echo -e "${RED}請使用root權限運行此腳本 (sudo ./os_setup.sh)${NC}"
                exit 1
            fi
            
            # 安裝Docker
            echo -e "${BLUE}安裝Docker...${NC}"
            apt update
            apt install -y apt-transport-https ca-certificates curl software-properties-common
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
            add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
            apt update
            apt install -y docker-ce
            
            # 安裝Docker Compose
            echo -e "${BLUE}安裝Docker Compose...${NC}"
            curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            chmod +x /usr/local/bin/docker-compose
            
            # 啟動Docker服務
            echo -e "${BLUE}啟動Docker服務...${NC}"
            systemctl start docker
            systemctl enable docker
            
            # 設定防火牆
            echo -e "${BLUE}設定防火牆...${NC}"
            if command -v ufw &> /dev/null; then
                ufw allow 8080/tcp
                ufw allow 8081/tcp
            fi
        else
            echo -e "${YELLOW}未識別的Linux發行版。請手動安裝Docker和Docker Compose。${NC}"
        fi
    else
        echo -e "${RED}無法確定Linux發行版。請手動安裝Docker和Docker Compose。${NC}"
    fi
    
    # 設置非root用戶可以執行docker命令
    echo -e "${BLUE}設置用戶權限...${NC}"
    if [ "$SUDO_USER" ]; then
        usermod -aG docker $SUDO_USER
        echo -e "${GREEN}已將用戶 $SUDO_USER 添加到docker組。請重新登入以應用更改。${NC}"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS系統
    echo -e "${BLUE}檢測到macOS操作系統${NC}"
    echo -e "${YELLOW}請按照以下步驟手動安裝Docker Desktop for Mac:${NC}"
    echo -e "1. 訪問 https://www.docker.com/products/docker-desktop/"
    echo -e "2. 下載並安裝Docker Desktop for Mac"
    echo -e "3. 啟動Docker Desktop應用程式"
    echo -e "4. 安裝完成後，您可以繼續執行setup.sh腳本"
    
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows系統
    echo -e "${BLUE}檢測到Windows操作系統${NC}"
    echo -e "${YELLOW}請按照以下步驟手動安裝Docker Desktop for Windows:${NC}"
    echo -e "1. 訪問 https://www.docker.com/products/docker-desktop/"
    echo -e "2. 下載並安裝Docker Desktop for Windows"
    echo -e "3. 確保啟用WSL 2功能"
    echo -e "4. 安裝完成後，重啟電腦"
    echo -e "5. 啟動Docker Desktop應用程式"
    echo -e "6. 安裝完成後，您可以使用Git Bash或WSL執行setup.sh腳本"
    
else
    # 其他操作系統
    echo -e "${RED}未支援的操作系統: $OSTYPE${NC}"
    echo -e "${YELLOW}請手動安裝Docker和Docker Compose。${NC}"
fi

# 檢查Docker是否安裝成功
echo -e "${BLUE}檢查Docker安裝...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}Docker已安裝: $(docker --version)${NC}"
else
    echo -e "${RED}Docker安裝失敗或未安裝${NC}"
fi

# 檢查Docker Compose是否安裝成功
echo -e "${BLUE}檢查Docker Compose安裝...${NC}"
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}Docker Compose已安裝: $(docker-compose --version)${NC}"
else
    echo -e "${RED}Docker Compose安裝失敗或未安裝${NC}"
fi

echo -e "${BLUE}===========================================${NC}"
echo -e "${GREEN}環境設置完成！${NC}"
echo -e "${BLUE}請執行 ./setup.sh 來啟動IAM與HR系統整合環境${NC}"
echo -e "${BLUE}===========================================${NC}"