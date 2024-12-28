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
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--no-sandbox')  # 为了兼容服务器环境
    options.add_argument('--disable-dev-shm-usage')  # 避免资源问题
    driver = webdriver.Chrome(options=options)

def crawl():
    # 获取请求参数
    data = request.json
    phone = request.json.get('phone')
    password = request.json.get('password')
    if not phone or not password:
        return jsonify({"error": "Missing required parameters"}), 400


@app.route('/crawl', methods=['POST'])
# 初始化 WebDriver
def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# 登录操作
def login_to_mooc(driver, phone, password):
    driver.get("https://www.icourse163.org/member/login.htm?returnUrl=aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcvaW5kZXguaHRt#/webLoginIndex&#34;")
    time.sleep(2)

    # 定位并切换到 iframe
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    # 输入用户名和密码
    username_input = driver.find_element(By.XPATH, '//*[@id="phoneipt"]')
    username_input.send_keys(phone)
    password_input = driver.find_element(By.XPATH, '//input[@placeholder="请输入密码"]')
    password_input.send_keys(password)

    # 点击登录按钮
    login_button = driver.find_element(By.XPATH, '//*[@id="submitBtn"]')
    login_button.click()

    # 切换回主页面
    driver.switch_to.default_content()
    time.sleep(5)

# 跳转到我的课程页面
def go_to_my_courses(driver):
    # 接受隐私政策
    privacy_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="privacy-ok"]'))
    )
    privacy_button.click()
    time.sleep(2)

    # 点击“我的课程”按钮
    my_courses_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[text()="我的课程"]'))
    )
    my_courses_button.click()
    time.sleep(5)

# 跳转到特定课程页面
def go_to_spoc_course(driver):
    current_url = driver.current_url
    new_url = current_url.rsplit("/", 1)[0] + "/spocCourse"
    driver.get(new_url)
    time.sleep(5)
    element = driver.find_element(By.XPATH, "//a[text()='正在进行']")
    element.click()

# 获取课程数据
def get_course_data(driver):
    data = {'name': [], 'ddl': []}
    divs = driver.find_elements(By.CLASS_NAME, "course-card-wrapper")

    for div in divs:
        # 点击课程卡片
        link_element = div.find_element(By.CLASS_NAME, "j-course-card-box")
        link_element.click()
        time.sleep(5)

        # 切换到新窗口
        driver.switch_to.window(driver.window_handles[-1])

        # 跳转到测验页面
        current_url = driver.current_url
        test_url = current_url.rsplit("/", 1)[0] + "/testlist"
        driver.get(test_url)
        time.sleep(5)

        # 获取课程名称和截止时间
        units = driver.find_elements(By.CSS_SELECTOR, ".u-quizHwListItem")
        for unit in units:
            name = unit.find_element(By.CLASS_NAME, "j-name").text
            data['name'].append(name)

            ddl_text = unit.find_element(By.CLASS_NAME, "j-submitTime").text
            match = re.search(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2})', ddl_text)
            if match:
                data['ddl'].append(match.group(1))

        # 返回到主窗口
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(3)

    return data

# 保存数据到 JSON 文件
def save_to_json(data, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            print("数据已保存到 JSON 文件：", file_path)
    except IOError as e:
        print("保存数据失败：", e)

# 主程序
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
