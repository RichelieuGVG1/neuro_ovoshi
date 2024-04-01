from LxmlSoup import LxmlSoup 
import requests 
import json 
 
for i in range(6): 
 
    res = requests.get(F"https://plantpad.samlab.cn/api/disease/findById/{i}?fields=disease_info") 
    data =res.json() 
 
    if(data["disease_info"]): 
        title=data["disease"]["name"] 
        definition_types=data["disease_info"]["definition_types"] 
        structure_mode=data["disease_info"]["structure_mode"] 
        period_environmental=data["disease_info"]["period_environmental"] 
        overwintering=data["disease_info"]["overwintering"] 
        chemical_control=data["disease_info"]["chemical_control"] 
        physical_measures=data["disease_info"]["physical_measures"] 
        biological_control=data["disease_info"]["biological_control"] 
        symptoms=data["disease_info"]["symptoms"] 
        signs=data["disease_info"]["signs"] 
        resistance_level=data["disease_info"]["resistance_level"] 
        apid_detection=data["disease_info"]["apid_detection"] 
        infection_mechanism=data["disease_info"]["infection_mechanism"] 
        stri= str(definition_types +"\n"+ structure_mode + "\n"+  period_environmental + "\n"+ overwintering + "\n"+ chemical_control  + "\n"+ physical_measures  + "\n"+  biological_control  + "\n" +symptoms + "\n" +  signs + "\n"+  resistance_level + "\n"+  apid_detection + "\n"+ infection_mechanism) 
        while(stri.find("<a") != -1): 
          start_index = stri.find("<a") 
          end_index = stri.find("a>") 
          stri = stri[:start_index] + stri[end_index + 2:] 
           
        with open(f"scraper/text_daset/{title}.txt", 'w', encoding="utf-8") as file: 
            file.write(stri) 
