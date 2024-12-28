# coding=gb2312
import requests  # 用于发送HTTP请求

# 定义接口的URL
url = "http://192.168.72.119:5000"  # 替换为你的实际接口地址

# 定义请求头，表明数据格式是 JSON
headers = {
    "Content-Type": "application/json"
}

# 定义发送的数据（JSON 格式）
data = {
    "phone": "17707697453",  # 替换为你的实际数据键值
    "password": "9987606a"
}

# 发送POST请求
try:
    response = requests.post(url, json=data, headers=headers)  # 使用 requests 库发送请求

    # 打印状态码
    print("Status Code:", response.status_code)

    # 打印返回的内容（JSON 格式）
    print("Response JSON:", response.json())
except Exception as e:
    print("Error occurred:", e)
