from LxmlSoup import LxmlSoup  
import requests  
import json  
import threading 
import os

def validator(item): 
  item = item.replace('<p>', '').replace("</p>", '')
  item = item.replace('["', '').replace('"]', '')
  item = item.replace('\\', '').replace('"', '')

  while(str(item).find("<a") != -1):    
    start_index = item.find("<a")  
    end_index = item.find("a>")  
    item = item[:start_index] + item[end_index + 2:] 

  return item
  
def parsing(start , end ): 
    url_1 = "https://plantpad.samlab.cn/api/disease/image/"
    url_2 = "https://plant-1302037000.cos.na-siliconvalley.myqcloud.com/data//"
    for i in range(start, end):  
        res = requests.post(f"{url_1}{i}")  
        try:
          data = res.json()
        except:
            continue  
     
        if(data["species"]):
            name = data["name"]
            path = data["path"]  
            title = validator(data["species"]) 
            signs = validator(data["signs"]) 

            words= { 
                "title":title, 
                "signs":signs, 
            } 

            link = (f"{url_2}{name}/{path}")
            res1 = requests.get(link)

            if (title == '' and signs == ''):
               continue
            else:
              with open(f"{folder_summary}/{title}.json", 'w', encoding="utf-8") as file:  
                  json.dump(words, file) 
            
              with open(f"{folder_summary}/{title}.jpg", "wb") as f:
                f.write(res1.content) 
        else: 
            print("NO fail") 

folder_summary = "plantpad_summary_dataset"

def main():
  if os.path.exists(folder_summary) == False:
    os.mkdir(folder_summary)

  for i in range(10): 
      thread = threading.Thread(target = parsing,args = (i*30000+1,(i+1)*30000), name = f"Thread-{i}") 
      thread.start() 
  
  thread.join()

if __name__ == "__main__":
   main()
