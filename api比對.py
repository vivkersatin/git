from bs4 import BeautifulSoup

# 讀取本機HTML檔案
with open("C:\\learn\\外1150324.html", "r", encoding='utf-8') as file:

    content = file.read()

# 解析HTML內容
soup = BeautifulSoup(content, "html.parser")

# 提取 <h5> 標籤的資料
tags = soup.find_all('h5')

# 打開一個文件來寫入
with open("output.txt", "w", encoding='utf-8') as file:
    for tag in tags:
        # 將每個標籤的文本內容寫入文件
        file.write(tag.get_text() + "\n")

print("資料已經寫入 output.txt")
