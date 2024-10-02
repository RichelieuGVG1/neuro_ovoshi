import pandas as pd

dataset_file = 'D:/Dataset processing/Tomato Cultivars/Tomato Cultivars_dataset_information.csv'
dataset_df = pd.read_csv(dataset_file)

reference_file = 'D:/Dataset processing/merge_csv.csv' 
reference_df = pd.read_csv(reference_file)

reference_df = reference_df.drop_duplicates(subset='common_species', keep='first')

reference_dict = reference_df.set_index('common_species').to_dict('index')

columns_to_update = ['kingdom', 'phylum', 'class', 'order', 'family', 'subfamily', 'genus', 'species']

for index, row in dataset_df.iterrows():
    common_species = row['common_species']
    if common_species in reference_dict:
        for column in columns_to_update:
            dataset_df.at[index, column] = reference_dict[common_species][column]

dataset_df.to_csv(dataset_file, index=False)