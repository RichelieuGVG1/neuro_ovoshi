import requests
from bs4 import BeautifulSoup
import re

url = 'https://en.wikipedia.org/wiki/Lists_of_plants'
base_url = 'https://en.wikipedia.org'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    with open('plant_names.txt', 'w', encoding='utf-8') as file:
        for link in links:
            text = link.get_text()
            if text.startswith("List"):
                full_url = base_url + link.get('href') 
                response_plant_page = requests.get(full_url)  

                if response_plant_page.status_code == 200:
                    plant_soup = BeautifulSoup(response_plant_page.text, 'html.parser')

                    
                    plant_links = plant_soup.find_all('a', {'title': re.compile('.*')})
                    
                    
                    for plant_link in plant_links:
                        plant_name = plant_link.get('title')
                        if plant_name:
                            file.write(plant_name + '\n')
else:
    print(f"Error {response.status_code}")


import re
unique_lines = set()


with open('plant_names.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()


with open('cleaned_plant_names.txt', 'w', encoding='utf-8') as clean_file:
    for line in lines:
        
        words = line.split()
        if len(words) > 3:
            continue
            
        words_to_remove = ['(alga)', '(biology)', '(green alga)']
        for word in words_to_remove:
            line = line.replace(word, '')

        if any(char in line for char in ['[', ']', '!', ':', ';', ',']):
            continue

        if any(stop_word in words for stop_word in ['Wikipedia', 'Edit', 'links', "The", "the", "List", "list", "of", "Lists", '(identifier)', 'description', "AlgaeBase"]):
            continue

        if re.search(r'\b\w\b', line):
            continue

        unique_line = line.strip()
        if unique_line not in unique_lines:
            unique_lines.add(unique_line)
            clean_file.write(unique_line + '\n')
