import os
import csv

dataset = '_dataset_information.csv'
dataset_name = 'Tomato Cultivars'
directory = 'D:/Dataset processing/Tomato Cultivars'
folder_names = []
name_csv = f'D:/Dataset processing/Tomato Cultivars/Tomato Cultivars{dataset}'

for root, dirs, files in os.walk(directory):
    if any(file.endswith('.jpg') for file in files):
        folder_name = os.path.basename(root).lower().replace("_", " ")
        
        if folder_name not in folder_names:
            folder_names.append(folder_name)

with open(name_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(['folder_name', 'dataset_name','common_species',
                     'common_variety', 'kingdom', 'phylum', 'class',
                     'order', 'family', 'subfamily', 'genus',
                     'species', 'image_path', 'height', 'width', 
                     'disease', 'rot', 'age', 'maturity', 'quantity',
                     'weight', 'part_of_a_plant', 'background_type'])

    for name in folder_names:
        writer.writerow([name.replace(" ", "_"), dataset_name, name])