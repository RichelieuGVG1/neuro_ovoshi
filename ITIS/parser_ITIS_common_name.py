import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time


def find_plant(filtered_lines):
    keywords_order = ["Variety", "Species", "Genus"]
    
    for keyword in keywords_order:
        matching_lines = [line for line in filtered_lines if keyword in line]
        if len(matching_lines) == 1:
            return matching_lines[0]
    
    return None


def find_name(plants):
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    url = 'https://www.itis.gov/servlet/SingleRpt/SingleRpt'
    max_attempts = 3
    attempt = 0
    success = False

    while attempt < max_attempts and not success:
        attempt += 1
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        try:
            time.sleep(1)
            button_1 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='RADIO' and @name='search_topic' and @value='Common_Name']"))
            )
            print("ЧЕКБОКС")

            select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_kingdom"))
            )
            select = Select(select_element)
            select.select_by_visible_text('Plant')

            button_1.click()

            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_value"))
            )
            input_field.send_keys(plants)

            print("Текст успешно введен в поле ввода.")

            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Go"))
            )
            button.click()
            print("Кнопка успешно нажата.")

            time.sleep(1)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "smwhiteboxhead"))
            )
            element = driver.find_element(By.CLASS_NAME, "smwhiteboxhead")
            result_text = element.text

            lines = result_text.split("\n")

            filtered_lines = [line for line in lines if line.endswith("accepted") and "not accepted"
                            not in line and line.split("–")[0].replace(" ", "") == plants]

            line = find_plant(filtered_lines)
            if line:
                print("Найдено соответствующая строка:")
                print(line)
            else:
                print("Соответствующая строка не найдена.")

            start_word_1 = "–"
            end_word_1 = ":"
            start_word_2 = "–"
            end_word_2 = "accepted"

            start_index_1 = line.find(start_word_1)
            end_index_1 = line.find(end_word_1, start_index_1)

            if start_index_1 != -1 and end_index_1 != -1:
                line = line[:start_index_1] + ":" + line[end_index_1 + len(end_word_1):]

            start_index_2 = line.find(start_word_2)
            end_index_2 = line.find(end_word_2, start_index_2)

            if start_index_2 != -1 and end_index_2 != -1:
                line = line[:start_index_2] + line[end_index_2 + len(end_word_2):]

            with open('common_name.txt', 'a') as f:
                f.write(f'{line}\n')

            success = True
        except Exception as e:
            print(f"Попытка {attempt} не удалась. Ошибка: {e}")
        finally:
            driver.quit()

    if not success:
        print("Не удалось выполнить задачу за 3 попытки.")

dir_path = 'C:\\Users\\nleon\\YandexDisk\\All_Agro_Datasets_Raw\\test'
folder_names = [name for name in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, name))]

for palenet in folder_names:
    palenet = palenet.lower()
    find_name(palenet)
