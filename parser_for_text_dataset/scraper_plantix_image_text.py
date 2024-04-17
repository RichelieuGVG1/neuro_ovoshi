from concurrent.futures import ThreadPoolExecutor 
from concurrent.futures import ThreadPoolExecutor 
from LxmlSoup import LxmlSoup 

import re 
import requests 
import json 
import os 
 
folder_text = "plantix_text" 
folder_image = "palntix_image" 
 
def validator(item): 
    item = re.sub(r'[^\x00-\x7F]+', '', str(item)) 
    return item 
 
def parsing(start, end): 
    for i in range(start, end): 
        text = [] 
        url = "https://plantix.net/en/library/plant-diseases/" 
        html = requests.get(f"{url}{i}").text 
        url_match = re.search(r'<meta http-equiv="refresh" content="0;url=(.*?)"', html) 
 
        if url_match: 
            redirected_url = url_match.group(1) 
            name = redirected_url.rsplit('/')[-2] 
            html_2 = requests.get(f'{redirected_url}').text 
            soup_2 = LxmlSoup(html_2) 
            p_tags = soup_2.find_all('p') 
            p_tags = p_tags[10:] 
            for p_tag in p_tags[:-2]: 
                text.append(p_tag.text()) 
            if(text[0]): 
                symptoms = validator(text[0]) 
                organic_control = validator(text[1]) 
                chemical_control = validator(text[3]) 
                caused = validator(text[-1]) 
 
            words = { 
                "title":name, 
                "symptoms":symptoms, 
                "organic_control":organic_control, 
                "chemical_control":chemical_control, 
                "caused":caused 
            } 
 
            with open(f'{folder_text}/{name}.json', 'w') as json_file: 
                json.dump(words, json_file) 
 
            piture = soup_2.find_all('div', class_="sld-img img wrp active")[1].find_all("img")[0].get('src') 
            image = requests.get(f'{piture}')     
            if image.status_code == 200: 
                try: 
                     with open(f"{folder_image}/{name}.jpg", "wb") as f: 
                        f.write(image.content)  
                        f.close() 
                except: 
                    print("error file") 
             
        else: 
            print("URL not found in HTML.") 
 
def make_folder(): 
 
    if not os.path.exists(folder_text): 
        os.mkdir(folder_text) 
    if not os.path.exists(folder_image): 
        os.mkdir(folder_image) 
 
def main(): 
 
    make_folder() 
 
    with ThreadPoolExecutor(max_workers=10) as executor: 
        for i in range(10): 
            start = i * 10000 + 100000 
            end = (i + 1) * 40000 + 400000 
            executor.submit(parsing, start, end) 
         
if __name__ == "__main__": 
    main()
