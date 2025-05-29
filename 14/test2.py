import re
import random
import pandas as pd
from collections import Counter

# 讀取文本內容
def read_text(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

# 清理文本並提取關鍵字
def extract_keywords(text, top_n=30):
    text = re.sub(r'[^\w\s]', '', text)  # 去除標點符號
    words = text.split()  # 分割單字
    word_count = Counter(words)  # 計算詞頻
    keywords = [word for word, freq in word_count.most_common(top_n)]  # 取前 top_n 個關鍵字
    return keywords

# 生成測驗題目
def generate_questions(keywords):
    true_false = [f"{kw} 是正確的概念嗎？ (Y/N)" for kw in keywords[:10]]
    single_choice = [f"以下哪個選項與 '{kw}' 最相關？" for kw in keywords[10:20]]
    multiple_choice = [f"下列哪些概念與 '{kw}' 相關？" for kw in keywords[20:30]]
    return {"是非題": true_false, "單選題": single_choice, "複選題": multiple_choice}

# 儲存到 Excel
def save_to_excel(questions, output_path="測驗題目.xlsx"):
    df = pd.DataFrame.from_dict(questions, orient='index').transpose()
    df.to_excel(output_path, index=False)
    print(f"測驗題目已成功儲存到 {output_path}！")

# 執行流程
if __name__ == "__main__":
    file_path = "output.txt"  # 這裡換成你的 TXT 檔案路徑
    text = read_text(file_path)
    keywords = extract_keywords(text)
    questions = generate_questions(keywords)
    save_to_excel(questions)