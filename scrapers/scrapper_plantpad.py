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
    for i in range(start, end):  
        res = requests.post(f"https://plantpad.samlab.cn/api/disease/image/{i}")  
        try:
          data = res.json()
        except:
            continue  
     
        if(data["species"]):  
            title = validator(data["species"]) 
            discription = validator(data["discription"]) 
            symptoms = validator(data["symptoms"]) 
            signs = validator(data["signs"]) 
            type_of_disease = validator(data["type_of_disease"]) 
            mode_of_transmission = validator(data["mode_of_transmission"]) 
            development_process = validator(data["development_process"]) 
            environmental_conditions = validator(data["environmental_conditions"]) 
            overwintering = validator(data["overwintering"]) 
            chemical_control = validator(data["chemical_control"]) 
            physical_measures = validator(data["physical_measures"]) 
            biological_control = validator(data["biological_control"]) 
            agricultural_control = validator(data["agricultural_control"]) 
            resistance_level = validator(data["resistance_level"]) 
            apid_detection = validator(data["apid_detection"]) 
            infection_mechanism = validator(data["infection_mechanism"]) 
            genes_bacteria = validator(data["genes_bacteria"])

            words= { 
                "title":title, 
                "discription":discription, 
                "symptoms":symptoms, 
                "signs":signs, 
                "type_of_disease":type_of_disease, 
                "mode_of_transmission":mode_of_transmission, 
                "development_process":development_process, 
                "environmental_conditions":environmental_conditions, 
                "overwintering":overwintering, 
                "chemical_control":chemical_control, 
                "physical_measures":physical_measures, 
                "biological_control": biological_control, 
                "agricultural_control":agricultural_control, 
                "resistance_level":resistance_level, 
                "apid_detection":apid_detection, 
                "infection_mechanism":infection_mechanism, 
                "genes_bacteria":genes_bacteria 
            } 

            if (title == '' and discription == '' and symptoms == '' and signs == ''):
               continue
            else:
              with open(f"plantpad/{str(i)}_{title}.json", 'w', encoding="utf-8") as file:  
                  json.dump(words, file)  
        else: 
            print("NO fail") 

def main():
  if os.path.exists('plantpad') == False:
    os.mkdir('plantpad')

  for i in range(10): 
      thread = threading.Thread(target=parsing,args=(i*30000+1,(i+1)*30000), name=f"Thread-{i}") 
      thread.start() 
  
  thread.join()

if __name__ == "__main__":
   main()
