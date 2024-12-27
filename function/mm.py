# coding=gb2312
import os
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_browser():
    """Initialize the browser."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def login(driver, phone, password):
    """Log in to the website."""
    login_url = "https://www.icourse163.org/member/login.htm?returnUrl=aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcvaW5kZXguaHRt#/webLoginIndex"
    driver.get(login_url)
    time.sleep(2)

    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)

    username_input = driver.find_element(By.XPATH, '//*[@id="phoneipt"]')
    username_input.click()
    username_input.send_keys(phone)
    time.sleep(2)

    password_input = driver.find_element(By.XPATH, '//input[@placeholder="请输入密码"]')
    password_input.click()
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, '//*[@id="submitBtn"]')
    login_button.click()
    driver.switch_to.default_content()
    time.sleep(10)

def get_course_info(driver):
    """Retrieve course information and deadlines."""
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="privacy-ok"]'))).click()
    time.sleep(3.5)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[text()="我的课程"]'))).click()
    time.sleep(10)

    driver.find_element(By.XPATH, "//a[text()='正在进行']").click()
    time.sleep(10)

    course_data = {"name": [], "ddl": []}
    divs = driver.find_elements(By.CLASS_NAME, "course-card-wrapper")
    for div in divs:
        link_element = div.find_element(By.CLASS_NAME, "j-course-card-box")
        link_element.click()
        time.sleep(7)

        driver.switch_to.window(driver.window_handles[-1])
        new_url = driver.current_url.rsplit("/", 1)[0] + "/testlist"
        driver.get(new_url)
        time.sleep(5)

        units = driver.find_elements(By.CSS_SELECTOR, ".u-quizHwListItem")
        for unit in units:
            name = unit.find_element(By.CLASS_NAME, "j-name").text
            ddl_text = unit.find_element(By.CLASS_NAME, "j-submitTime").text
            match = re.search(r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2})', ddl_text)
            if match:
                course_data["name"].append(name)
                course_data["ddl"].append(match.group(1))

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

    return course_data

def save_to_json(data, directory, filename):
    """Save data to a JSON file."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Data saved to", file_path)
    except IOError as e:
        print("Failed to save file:", e)

def load_from_json(directory, filename):
    """Load data from a JSON file."""
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("Data loaded successfully:", data)
        return data
    except Exception as e:
        print("Failed to load file:", e)
        return None

def main():
    phone = "17707697453"
    password = "9987606a"
    save_dir = 'C:\\Users\\17434\\mooc'
    save_file = 'a.json'

    driver = init_browser()
    try:
        login(driver, phone, password)
        course_data = get_course_info(driver)
        save_to_json(course_data, save_dir, save_file)
        loaded_data = load_from_json(save_dir, save_file)
        print("Loaded data:", loaded_data)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
