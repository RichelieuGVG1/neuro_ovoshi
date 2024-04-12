from concurrent.futures import ThreadPoolExecutor
from LxmlSoup import LxmlSoup
import requests
import json
import os
import wikipedia

def search_and_scrape(wiki_url):
    try:
        trimmed_link = wiki_url.rsplit('/', 1)[-1]
        page = wikipedia.page(trimmed_link)
        result_dict = {}
        result_dict['title'] = page.original_title
        result_dict['summary'] = page.summary
        result_dict['Origins'] = page.section("Origins")
        result_dict['Description'] = page.section("Description")
        result_dict['Characteristics'] = page.section("Characteristics")
        result_dict['Cultivars'] = page.section("Cultivars")
        result_dict['Botany'] = page.section("Botany")
        result_dict = {k: v for k, v in result_dict.items() if v}

        if len(result_dict) > 1:
            with open(f'{name_folder}/{result_dict["title"]}.json', 'w') as json_file:
                json.dump(result_dict, json_file)
    except Exception:
        print(f"Error getting page: {wiki_url}")

url = "https://en.wikipedia.org/wiki/List_of_culinary_fruits"
clsas_tables = "wikitable sortable sticky-header"
html = requests.get(url).text
soup = LxmlSoup(html)
links = []
name_folder = "List_of_culinary_fruits_wikipedia"

if not os.path.exists(name_folder):
    os.mkdir(name_folder)

tables = soup.find_all('table')
for table in tables:
    if (table.get("class") and str(table.get("class")) == clsas_tables):
        table_links = table.find_all('tr')
        for table_link in table_links:
            a_element = table_link.find_all('a')
            if a_element:
                links.append(a_element[0].get('href'))

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(search_and_scrape, links)
