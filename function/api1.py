# coding=gb2312
import os
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, jsonify

app = Flask(__name__)


def setting(driver):
    options = Options()
    options.add_argument('--headless')  # ��ͷģʽ
    options.add_argument('--no-sandbox')  # Ϊ�˼��ݷ���������
    options.add_argument('--disable-dev-shm-usage')  # ������Դ����
    driver = webdriver.Chrome(options=options)

def crawl():
    # ��ȡ�������
    data = request.json
    phone = request.json.get('phone')
    password = request.json.get('password')
    if not phone or not password:
        return jsonify({"error": "Missing required parameters"}), 400


@app.route('/crawl', methods=['POST'])
# ��ʼ�� WebDriver
def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# ��¼����
def login_to_mooc(driver, phone, password):
    driver.get("https://www.icourse163.org/member/login.htm?returnUrl=aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcvaW5kZXguaHRt#/webLoginIndex&#34;")
    time.sleep(2)

    # ��λ���л��� iframe
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # �����û���������
    username_input = driver.find_element(By.XPATH, '//*[@id="phoneipt"]')
    username_input.send_keys(phone)
    password_input = driver.find_element(By.XPATH, '//input[@placeholder="����������"]')
    password_input.send_keys(password)

    # �����¼��ť
    login_button = driver.find_element(By.XPATH, '//*[@id="submitBtn"]')
    login_button.click()

    # �л�����ҳ��
    driver.switch_to.default_content()
    time.sleep(5)

# ��ת���ҵĿγ�ҳ��
def go_to_my_courses(driver):
    # ������˽����
    privacy_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="privacy-ok"]'))
    )
    privacy_button.click()
    time.sleep(2)

    # ������ҵĿγ̡���ť
    my_courses_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[text()="�ҵĿγ�"]'))
    )
    my_courses_button.click()
    time.sleep(5)

# ��ת���ض��γ�ҳ��
def go_to_spoc_course(driver):
    current_url = driver.current_url
    new_url = current_url.rsplit("/", 1)[0] + "/spocCourse"
    driver.get(new_url)
    time.sleep(5)
    element = driver.find_element(By.XPATH, "//a[text()='���ڽ���']")
    element.click()

# ��ȡ�γ�����
def get_course_data(driver):
    data = {'name': [], 'ddl': []}
    divs = driver.find_elements(By.CLASS_NAME, "course-card-wrapper")

    for div in divs:
        # ����γ̿�Ƭ
        link_element = div.find_element(By.CLASS_NAME, "j-course-card-box")
        link_element.click()
        time.sleep(5)

        # �л����´���
        driver.switch_to.window(driver.window_handles[-1])

        # ��ת������ҳ��
        current_url = driver.current_url
        test_url = current_url.rsplit("/", 1)[0] + "/testlist"
        driver.get(test_url)
        time.sleep(5)

        # ��ȡ�γ����ƺͽ�ֹʱ��
        units = driver.find_elements(By.CSS_SELECTOR, ".u-quizHwListItem")
        for unit in units:
            name = unit.find_element(By.CLASS_NAME, "j-name").text
            data['name'].append(name)

            ddl_text = unit.find_element(By.CLASS_NAME, "j-submitTime").text
            match = re.search(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2})', ddl_text)
            if match:
                data['ddl'].append(match.group(1))

        # ���ص�������
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)

    return data

# �������ݵ� JSON �ļ�
def save_to_json(data, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print("�����ѱ��浽 JSON �ļ���", file_path)
    except IOError as e:
        print("��������ʧ�ܣ�", e)

# ������
def main():
    phone = "17707697453"
    password = "9987606a"
    directory = 'C:\\Users\\17434\\mooc'
    filename = 'a.json'

    driver = init_driver()

    try:
        login_to_mooc(driver, phone, password)
        go_to_my_courses(driver)
        go_to_spoc_course(driver)
        course_data = get_course_data(driver)
        save_to_json(course_data, directory, filename)
    finally:
        driver.quit()
        app.run(host='0.0.0.0', port=5000)
if __name__ == "__main__":
    main()
