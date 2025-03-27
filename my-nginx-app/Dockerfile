# 使用官方的Ubuntu映像作為基礎映像
FROM ubuntu:latest

# 維護者資訊
MAINTAINER Your Name <your.email@example.com>

# 更新apt-get並安裝nginx
RUN apt-get update && apt-get install -y nginx

# 複製nginx的預設配置檔案
COPY default /etc/nginx/sites-available/default

# 更改/var/www/html目錄的權限
RUN chown -R www-data:www-data /var/www/html
RUN chown www-data:www-data /etc/nginx/sites-available/default

# 暴露80端口
EXPOSE 80

# 啟動nginx
CMD ["nginx", "-g", "daemon off;"]