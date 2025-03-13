import requests
import json

# 定义要抓取的URL
url = "https://data.taipei/api/v1/dataset/296acfa2-5d93-4706-ad58-e83cc951863c?scope=resourceAquire"

# 发送HTTP请求获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析 JSON 数据
    data = json.loads(response.text)

    # 提取公司名称
    with open('companies_data.txt', 'a', encoding='utf-8') as file:
        for item in data['result']['results']:
            company_name = item['公司名稱']
            company_address = item.get('公司地址', '未提供')
            company_phone = item.get('公司電話', '未提供')
            file.write(f"公司名稱: {company_name}, 公司地址: {company_address}, 公司電話: {company_phone}\n")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
