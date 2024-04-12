from concurrent.futures import ThreadPoolExecutor
from LxmlSoup import LxmlSoup
from urllib.parse import urlparse
import requests
import json
import os
import wikipedia

url = "https://en.wikipedia.org/wiki/List_of_culinary_fruits"
clsas_tables = "wikitable sortable sticky-header"
html = requests.get(url).text
soup = LxmlSoup(html)
links = []
name_folder = "List_of_culinary_fruits_wikipedia"
if not os.path.exists(name_folder):
    os.mkdir(name_folder)

def search_links(wiki_url):
    trimmed_link = wiki_url.rslit('/', 1)[-1]
    wiki_links = []
    if trimmed_link:
        page = wikipedia.page(trimmed_link)
        wiki_links.append(page)
        scraper_page(wiki_links)

def scraper_page(links: list):
    wikipedia.set_lang("en")
    for link in links:
        try:
            pythin_page = wikipedia.page(f"{link}")
            result_dict = {}
            result_dict['title'] = pythin_page.original_title
            result_dict['summary'] = pythin_page.summary
            result_dict['Origins'] = pythin_page.section("Origins")
            result_dict['Description'] = pythin_page.section("Description")
            result_dict['Characteristics'] = pythin_page.section("Characteristics")
            result_dict['Cultivars'] = pythin_page.section("Cultivars")
            result_dict['Botany'] = pythin_page.section("Botany")
            keys_to_remove = []
            for key, value in result_dict.items():
                if not value:
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                del result_dict[key]

            if len(result_dict) > 1:
                with open(f'name_folder/{result_dict["title"]}.json','w') as json_file: 
                    json.dump(result_dict,json_file) 
        except:
            print("Ошибка при обработке ссылки")

tables = soup.find_all('table')
for table in tables:
    if (table.get("class") and str(table.get("class")) == clsas_tables):
        table_links = table.find_all('tr')
        for table_link in table_links:
            a_element = table_link.find_all('a')
            if a_element:
                links.append(a_element[0].get('href'))

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(search_links, links)
