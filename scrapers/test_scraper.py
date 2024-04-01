from LxmlSoup import LxmlSoup 
import requests 
import json 
import time
 
for i in range(255400, 255800): 
    timestart = time.time()
    res = requests.post(f"https://plantpad.samlab.cn/api/disease/image/{i}") 
    data = res.json() 
  
    if(data["species"]): 
        title = data["species"]
        discription = data["discription"]
        symptoms = data["symptoms"]
        signs = data["signs"]
        type_of_disease = data["type_of_disease"]
        mode_of_transmission = data["mode_of_transmission"]
        development_process = data["development_process"]
        environmental_conditions = data["environmental_conditions"]
        overwintering = data["overwintering"]
        chemical_control = data["chemical_control"]
        physical_measures = data["physical_measures"]
        biological_control = data["biological_control"]
        agricultural_control = data["agricultural_control"]
        resistance_level = data["resistance_level"]
        apid_detection = data["apid_detection"]
        infection_mechanism = data["infection_mechanism"]
        genes_bacteria = data["genes_bacteria"]

        words= str("name: " + title + "\n" + "discription: " + discription + "\n" 
                  + "disease_symptoms: " + symptoms + "\n" + "signs_of_disease: " + signs + "\n"
                  + "type_of_disease:" + chemical_control + "\n" + "mode_of_transmission: " + mode_of_transmission + "\n"
                  + "development_process: " + development_process 
                  + "environmental_conditions: " + "\n" + environmental_conditions + "\n" 
                  + "overwintering_method: " + overwintering + "\n" + "prevention_strategies: " + "\n" 
                  + "chemical_control: "+ chemical_control + "\n" 
                  + "physical_measures: " + physical_measures + "\n" + "biological_control" + biological_control 
                  + "agricultural_control: " + agricultural_control + "\n" + "pathogenic_mechanism:" + "\n" 
                  + "resistance_level: " + resistance_level + "\n" + "apid_detection: " + apid_detection + "\n" 
                  + "infection_mechanism: " + infection_mechanism + "\n" + "genes_bacteria: " + genes_bacteria) 
        
        while(words.find("<a") != -1): 
          start_index = words.find("<a") 
          end_index = words.find("a>") 
          words = words[:start_index] + words[end_index + 2:] 
        
        words = words.replace('<p>', '')
        words = words.replace('</p>', '')
        words = words.replace('["', '')
        words = words.replace('"]', '')
           
        with open(f"scraper/text_daset/{title}.txt", 'w', encoding="utf-8") as file: 
            file.write(words) 
        timestop = time.time()
        print(timestop - timestart)
    else:
        print("NO fail")
