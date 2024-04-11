from concurrent.futures import ThreadPoolExecutor
from LxmlSoup import LxmlSoup
from urllib.parse import urlparse
import requests 
import json 
import os
import wikipedia

wiki_links = []

def search_links(wikipedia_urls):
    trimmed_link = wikipedia_urls.rsplit('/', 1)[-1] 

    if trimmed_link:
        try:
            page = wikipedia.page(trimmed_link)
            wiki_links.append(page)
            scraper_page(wiki_links)
        except wikipedia.exceptions.PageError:
            print("Страница не найдена.")

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
                with open(f'csydes_miraheze/{result_dict["title"]}.json','w') as json_file: 
                    json.dump(result_dict,json_file) 
        except:
            print("Ошибка при обработке ссылки")

url = "https://csydes.miraheze.org/wiki/List_of_Fruits_and_Vegetables"
html_text = requests.get(url).text
soup = LxmlSoup(html_text)
link = []

if not os.path.exists('csydes_miraheze'):
    os.mkdir('csydes_miraheze')

table_links = soup.find_all('tr')
for table_link in table_links:
    a_elements = table_link.find_all('a')
    if a_elements:
        link.append(a_elements[1].get('href'))

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(search_links, link)
