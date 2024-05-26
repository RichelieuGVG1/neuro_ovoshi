import re
import os
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

file_path = "dataset_information.csv"


def conect_to_site():

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    url = 'https://www.itis.gov/servlet/SingleRpt/SingleRpt'

    return url,chrome_options


def find_plant_common_name(filtered_lines):
    keywords_order = ["Variety", "Species", "Genus"]
    
    for keyword in keywords_order:
        matching_lines = [line for line in filtered_lines if keyword in line]
        if len(matching_lines) == 1:
            return matching_lines[0]
    
    return None


def clear_plants_common_name(line):
    line = re.sub(r'\([^)]*\)', '', line)
    
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

    pattern = r"(\s[A-Za-z]+\s*)\."
    cleaned_lines = re.sub(pattern, "", line).strip()

    return cleaned_lines


def find_plant_scientific_name(filtered_lines, plants):
    for line in filtered_lines:
        if ':' in line:
            name_part = line.split(':')[0].strip()
            if name_part in plants:
                return line
    return None


def clear_plants_scientific_name(line):
    line = re.sub(r'\([^)]*\)', '', line)
    line = re.sub(r"–.*?accepted", ":", line)
    line = re.sub(r"–", "", line)
    line = re.sub(r"\s[A-Za-z]+\s*\.", "", line).strip()
    return line


def add_scientific(cleaned_lines):
    dictionary = {}

    for item in cleaned_lines.split("\n"):
        if item.strip():
            key, value = item.split(":")
            dictionary[key.strip()] = value.strip()

    df = pd.read_csv(file_path)

    for index, row in df.iterrows():
        for key in dictionary.keys():
            if key in row['common_species']:
                df.at[index, 'species'] = dictionary[key]

    df.to_csv(file_path, index=False)


def add_common(cleaned_lines):
    dictionary = {}

    for item in cleaned_lines.split("\n"):
        if item.strip():
            key, value = item.split(":")
            dictionary[key.strip()] = value.strip()

    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        for key in dictionary.keys():
            if key in row['species']:
                df.at[index, 'common_species'] = dictionary[key]

    df.to_csv(file_path, index=False)


def convert_common_to_scientific(data_common_names):
    for data_common_name in data_common_names:
        url,chrome_options = conect_to_site()

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

                select_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "search_kingdom"))
                )
                select = Select(select_element)
                select.select_by_visible_text('Plant')

                button_1.click()

                input_field = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "search_value"))
                )
                input_field.send_keys(data_common_name)

                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "Go"))
                )
                button.click()

                time.sleep(1)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "smwhiteboxhead"))
                )
                element = driver.find_element(By.CLASS_NAME, "smwhiteboxhead")
                result_text = element.text

                lines = result_text.split("\n")

                filtered_lines = [line for line in lines if line.endswith("accepted")
                                and "not accepted" not in line 
                                and line.split("–")[0].replace(" ", "") == data_common_name]

                line = find_plant_common_name(filtered_lines)
                

                if line:
                    plants_dictionary = clear_plants_common_name(line)
                    add_scientific(plants_dictionary)
                    success = True

            except Exception as e:
                print(f"Попытка {attempt} не удалась. Ошибка: {e}")
            finally:
                driver.quit()

def convert_scientific_to_common(data_scientific_names):
    for data_scientific_name in data_scientific_names:
        url,chrome_options = conect_to_site()
    
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
                EC.presence_of_element_located((By.XPATH, "//input[@type='RADIO' and @name='search_topic' and @value='Scientific_Name']"))
            )

            select_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_kingdom"))
            )
            select = Select(select_element)
            select.select_by_visible_text('Plant')

            button_1.click()

            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_value"))
            )
            input_field.send_keys(data_scientific_name)

            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Go"))
            )
            button.click()

            time.sleep(1)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "smwhiteboxhead"))
            )
            element = driver.find_element(By.CLASS_NAME, "smwhiteboxhead")
            result_text = element.text

            lines = result_text.split("\n")
            pattern = r"(\s[A-Za-z]+\s*)\."

            filtered_lines = [re.sub(pattern, "", line) for line in lines if "– accepted –" in line 
                              and "not accepted" not in line]

            clear_names = [clear_plants_scientific_name(line) for line in filtered_lines]

            line = find_plant_scientific_name(clear_names, data_scientific_names)

            if line:
                add_common(line)
                success = True

        except Exception as e:
            print(f"Попытка {attempt} не удалась. Ошибка: {e}")
        finally:
            driver.quit()
    

def main():
    data_common_name = pd.read_csv(file_path, 
                                   usecols= ['common_species'])
    data_common_name = data_common_name.drop_duplicates()

    data_scientific_name = pd.read_csv(file_path, 
                                        usecols= ['species'])
    data_scientific_name = data_scientific_name.drop_duplicates()

    if ('common_species' in data_common_name.columns 
        and data_common_name['common_species'].count() > 0):
        convert_common_to_scientific(data_common_name['common_species'].values)
    elif ('species' in data_scientific_name.columns 
          and data_scientific_name['species'].count() > 0):
        convert_scientific_to_common(data_scientific_name['species'].values)
    else:
        print("Empty columns 'common_species' and 'species'")
        

if __name__ == "__main__": 
    main()
