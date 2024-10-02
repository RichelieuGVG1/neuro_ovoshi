import pandas as pd

def replace_base_path(input_csv_path, output_csv_path, old_base_path='All_Agro_Datasets_Raw/A Benchmark Dataset for Apple Detection and Segmentation', new_base_path='All_Agro_Datasets_Raw/034_A Benchmark Dataset for Apple Detection and Segmentation'): 
    data = pd.read_csv(input_csv_path)
    
    data['image_path'] = data['image_path'].str.replace(old_base_path, new_base_path)
    
    data.to_csv(output_csv_path, index=False)
    print(f"Processed and saved new CSV to '{output_csv_path}'")

# Пример использования
input_csv_path = 'D:/Dataset processing/task_for_markers_with_dimensions_updated.csv'
output_csv_path = 'D:/Dataset processing/task_for_markers_with_dimensions_updated.csv'

replace_base_path(input_csv_path, output_csv_path)