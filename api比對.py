from bs4 import BeautifulSoup
import os

# 讀取本機HTML檔案
input_file_path = "C:\\learn\\1140508out.html"

with open(input_file_path, "r", encoding='utf-8') as file:
    content = file.read()

# 解析HTML內容
soup = BeautifulSoup(content, "html.parser")

# 提取 <h5> 標籤的資料
tags = soup.find_all('h5')

# 生成輸出檔案名稱
output_file_path = os.path.splitext(input_file_path)[0] + ".txt"

# 打開一個文件來寫入
with open(output_file_path, "w", encoding='utf-8') as file:
    for tag in tags:
        # 將每個標籤的文本內容寫入文件
        file.write(tag.get_text() + "\n")

print(f"資料已經寫入 {output_file_path}")
