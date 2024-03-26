import requests
from bs4 import BeautifulSoup
import re
global final
final=[]
import time
try:
    def clear(st):
        if (len(st)>50 and not ' ' in st) or len(st)>80:
            return None
        #if not any(char.isdigit() for char in st):
        #    return None
        st=re.sub(r'\[.*?\]', '', st)
        st=re.sub(r'\(.*?\)', '', st)
        st=st.replace('\n', '')
        st = st[st.find(',') + 2:] if 'genus' in st else st
            
        if 'spp.' in st:
            st=st[st.find('spp.')+5:]
            if len(st)<4:
                return None
                         
        if '=' in st:
            st=st.split(' = ')
            final.extend(st)
        else:
            final.append(st)
        
    def download(href):
        href='https://en.wikipedia.org/'+href
        response = requests.get(href)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        ban=['unknown','scientific name','common name', 'name', 'gtp','determined', 'physiological','temperature','phytoplasma','not known', 'high ', 'low ','senescence','mlo', 'genetic','imbalance', 'etc.','species']
        for table in tables:
            
            rows=table.find_all('tr')
            try:
                num_rows=len(rows[1].find_all(['td', 'th']))
                #print(num_rows, href)
            except IndexError:
                continue
            
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                
                for i in range(len(columns)):
                    if len(columns[i].text)>3 and i%num_rows==1 and not any(_ in str(columns[i].text).lower() for _ in ban):
                        #result_string = re.sub(r'\[.*?\]', '', columns[i].text)
                        clear(columns[i].text)

    def get_links(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if '/wiki/List' in href:
                #print(href)
                download(href)
                
    start_time = time.time()
    print('Counting...')
    get_links('https://en.wikipedia.org/wiki/Lists_of_plant_diseases')
    with open ('parsed_text.txt', 'w', encoding='utf-8') as file:
        for _ in final:
            _=_.replace('=','')
            _ = _[1:] if _.startswith(' ') else _
            file.write(_+'\n')
        file.close()
    print('Elapsed time: ', time.time()-start_time)
                              
except Exception as e:
    print(e)
finally:
    import os
    os.system('pause')
