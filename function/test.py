# coding=gb2312
import requests  # ���ڷ���HTTP����

# ����ӿڵ�URL
url = "http://192.168.72.119:5000"  # �滻Ϊ���ʵ�ʽӿڵ�ַ

# ��������ͷ���������ݸ�ʽ�� JSON
headers = {
    "Content-Type": "application/json"
}

# ���巢�͵����ݣ�JSON ��ʽ��
data = {
    "phone": "17707697453",  # �滻Ϊ���ʵ�����ݼ�ֵ
    "password": "9987606a"
}

# ����POST����
try:
    response = requests.post(url, json=data, headers=headers)  # ʹ�� requests �ⷢ������

    # ��ӡ״̬��
    print("Status Code:", response.status_code)

    # ��ӡ���ص����ݣ�JSON ��ʽ��
    print("Response JSON:", response.json())
except Exception as e:
    print("Error occurred:", e)
