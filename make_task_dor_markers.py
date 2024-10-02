import os
import pandas as pd

# def create_description(row):
#     description = (
#         f"Common species: {row['common_species']}, "
#         f"Common variety: {row['common_variety']}, "
#         f"Disease: {row['disease']}, "
#         f"Rot: {row['rot']}, "
#         f"Image path: {row['image_path']}"
#     )
#     return description

def find_image_folders(root_folder):
    image_folders = []
    for root, dirs, files in os.walk(root_folder):
        if any(file.lower().endswith(('.png', '.jpg', '.jpeg')) for file in files):
            image_folders.append(root)
    return image_folders

def process_dataset(dataset_path, dataset_name, input_csv_path, output_csv_path, base_path='D:/Dataset processing', new_base_path='All_Agro_Datasets_Raw'):
    data = pd.read_csv(input_csv_path)

    data['folder_name_processed'] = data['folder_name'].str.replace(' ', '').replace(' ','').replace('-','').str.lower()
    # print(data['folder_name'].str.replace(' ', '').replace('_','').replace('-','').str.lower())

    subfolders = find_image_folders(dataset_path)

    new_data = []

    for subfolder in subfolders:
        plant_folder_name = os.path.basename(subfolder).replace(' ', '').replace('_','').replace('-','').lower()
        # print(plant_folder_name)
        
        matching_rows = data[
            (data['dataset_name'] == dataset_name) &
            (data['folder_name_processed'] == plant_folder_name)
        ]

        if matching_rows.empty:
            print(f"No matching rows found for dataset '{dataset_name}' and folder '{plant_folder_name}'")
            continue

        matching_row = matching_rows.iloc[0]

        image_files = [f for f in os.listdir(subfolder) if os.path.isfile(os.path.join(subfolder, f))]

        for image_file in image_files:
            old_image_path = os.path.join(subfolder, image_file)
            new_image_path = old_image_path.replace(base_path, new_base_path).replace('\\', '/')
            new_row = {
                'image_path': new_image_path,
                'common_species': matching_row['common_species'],
                'common_variety': matching_row['common_variety'],
                'disease': matching_row['disease'],
                'rot': matching_row['rot'],
                'description': None
            }
            new_data.append(new_row)

    new_df = pd.DataFrame(new_data)
    
    if not os.path.exists(output_csv_path):
        new_df.to_csv(output_csv_path, index=False)
    else:
        new_df.to_csv(output_csv_path, mode='a', header=False, index=False)

    print(f"Processed dataset '{dataset_name}' in '{dataset_path}'")

dataset_path = 'D:/Dataset processing/Wild Edible Plants'
dataset_name = 'Wild Edible Plants'
input_csv_path = 'D:/Dataset processing/merge_dataset_information.csv'
output_csv_path = 'task_for_markers.csv'

process_dataset(dataset_path, dataset_name, input_csv_path, output_csv_path)