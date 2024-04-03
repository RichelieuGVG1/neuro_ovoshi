import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import time
from urllib.parse import urlparse

url = "https://ieee-dataport.org/topic-tags/artificial-intelligence"

username = ""
password = ""

driver = webdriver.Chrome()

try:
    driver.get(url)

    login_link = driver.find_element(By.LINK_TEXT, "Login")
    login_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    sign_in_button = driver.find_element(By.ID, "modalWindowRegisterSignInBtn")
    sign_in_button.click()

    time.sleep(5)

    search_input = driver.find_element(By.ID, "edit-title")

    search_input.send_keys("LEAVES: INDIA’S MOST FAMOUS BASIL PLANT LEAVES QUALITY DATASET")

    search_input.send_keys(Keys.RETURN)

    time.sleep(5)

    dataset_link = driver.find_element(By.XPATH, "//a[contains(@href, '/open-access/leaves-india%E2%80%99s-most-famous-basil-plant-leaves-quality-dataset')]")
    dataset_link.click()

    time.sleep(5)

    folders = driver.find_elements(By.CLASS_NAME, "caret")

    for folder in folders:
        folder_name = folder.text.strip()

        if not folder_name:
            continue

        print(f"Найдена папка: {folder_name}")

        if folder_name == "Basil":
            driver.execute_script("arguments[0].click();", folder)  
            time.sleep(2)  
            continue

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        folder.click()

        time.sleep(2)

        images = driver.find_elements(By.XPATH, "//a[contains(@href, '.jpeg')]")
        if not images:
            print(f"В папке {folder_name} нет изображений.")
            continue

        for img_link in images:
            img_url = img_link.get_attribute("href")

            img_name = os.path.basename(urlparse(img_url).path)

            img_data = requests.get(img_url).content

            with open(os.path.join(folder_name, img_name), 'wb') as img_file:
                img_file.write(img_data)

    print("Загрузка завершена.")
except Exception as e:
    print(f"Произошла ошибка: {e}")

finally:
    driver.quit()
