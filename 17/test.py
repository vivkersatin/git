import google.generativeai as genai

# 配置 API Key (如果您沒有設定環境變數)
genai.configure(api_key="AIzaSyDzjP_8V2wF0JPdPILUeCCijP8FmBbV3o0")

# 初始化 Gemini 模型
# 您可以選擇不同的模型，例如 'gemini-pro' 用於文本，'gemini-pro-vision' 用於多模態（文本+圖片）
model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

# 發送請求並生成內容
response = model.generate_content("寫一篇關於夏天旅行的短文。")

# 打印生成的內容
print(response.text)