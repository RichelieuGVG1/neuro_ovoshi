from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup 
from LxmlSoup import LxmlSoup
from tqdm import tqdm 
import requests 
import json 
import os
import wikipedia

def filter_role_attribute(value): 
    return value is None or value != 'presentation' 
 
def next_step(link): 
    links = [] 
    html = requests.get(f'https://en.wikipedia.org{link}').text 
    soup = BeautifulSoup(html, 'html.parser')   

    link_dir = link.rsplit('/', 1)[-1]
    os.mkdir(link_dir) 

    no_table_presentation_nnot_valid = soup.find_all('table', role=filter_role_attribute) 
    no_table_presentation = [] 
    for table in no_table_presentation_nnot_valid: 
         if ("border-spacing:0;background:transparent;color:inherit" not in table.get("style", "")) and ("nowraplinks" not in table.get("class", "")): 
            no_table_presentation.append(table) 
    if (len(no_table_presentation) == 0): 
        if(len(soup.find_all('div', class_="div-col")) == 0): 
            container = soup.find_all('li') 
        else: 
            container = soup.find_all('div', class_="div-col") 
        for links_L in container: 
            links_ = links_L.find_all("a") 
            for link in links_: 
                if(str(link.get('href')).find("/wiki/")!=-1): 
                    links.append(link.get('href')) 
 
    else:  
        for table in no_table_presentation: 
            TRs = table.find_all('tr')   
            for tr in TRs: 
                if(str(tr).find("class=\"navbox-list navbox-odd\""))!=-1: 
                    break 
                a_elements = tr.find_all('a') 
 
                if(a_elements and str(a_elements[0].get('href')).find(".")==-1): 
                    if(str(a_elements[0].get('href')).find("/wiki/")!=-1 and str(a_elements[0].get('href')).find("Wine")==-1): 
                        link = a_elements[0].get('href') 
                        links.append(link) 
                elif(len(a_elements)>=2 and str(a_elements[1].get('href')).find(".")==-1): 
                     if(str(a_elements[1].get('href')).find("/wiki/")!=-1 and str(a_elements[0].get('href')).find("Wine")==-1): 
                        link = a_elements[1].get('href') 
                        links.append(link) 
    links=set(links) 
    links=list(links) 
    trimmed_links = [] 
 
    for link in links: 
        trimmed_link = link.rsplit('/', 1)[-1] 
        trimmed_links.append(trimmed_link) 
    parsing_page(trimmed_links, link_dir) 
    
def parsing_page(links:list, link_dir:str): 
    counter = 0 
    wikipedia.set_lang("en") 
    for link in links: 
        counter+=1 
        try : 
            pythin_page = wikipedia.page(f'{link}') 
            result_dict = {} 
            result_dict['title'] = pythin_page.original_title 
            result_dict['summary'] = pythin_page.summary 
            result_dict['Origins'] = pythin_page.section("Origins") 
            result_dict['Description'] = pythin_page.section("Description") 
            result_dict['Characteristics'] = pythin_page.section( "Characteristics") 
            keys_to_remove = [] 
            for key , value in  result_dict.items(): 
               if not value: 
                   keys_to_remove.append(key) 
            for key in keys_to_remove: 
                del result_dict[key] 
             
            if len(result_dict) ==1: 
                continue 
            else: 
                with open(f'{link_dir}/{result_dict['title']}.json','w') as json_file: 
                    json.dump(result_dict,json_file) 
        except: 
            print("eror link") 
 
html = requests.get('https://en.wikipedia.org/wiki/Lists_of_plants').text   
soup = LxmlSoup(html)   
 
li_elements = soup.find_all('li')   
links=[] 
 
for li in li_elements: 
    a_elements = li.find_all('a') 
 
    for a in a_elements: 
        link = a.get('href') 
        if ((a.get('class') and str(a.get('class'))!="mw-redirect") 
            or str(link).find("List_of")==-1 or str(link).lower().find("tree")!=-1): 
            continue 
        else: 
            links.append(link) 
 
links=links[3:] 
links.remove("/wiki/List_of_banana_cultivars") 
links=set(links) 
links=list(links) 

with ThreadPoolExecutor(max_workers=12) as executor:
    executor.map(next_step, links)
