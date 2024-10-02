import pandas as pd
from PIL import Image

def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            return img.width, img.height
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
        return None, None

def add_image_dimensions(input_csv_path, output_csv_path):
    data = pd.read_csv(input_csv_path)

    data['width'] = None
    data['height'] = None

    for idx, row in data.iterrows():
        image_path = row['image_path']
        width, height = get_image_dimensions(image_path)
        data.at[idx, 'width'] = width
        data.at[idx, 'height'] = height

    data.to_csv(output_csv_path, index=False)
    print(f"Processed and saved new CSV with image dimensions to '{output_csv_path}'")
    
input_csv_path = 'task_for_markers_updated.csv'
output_csv_path = 'task_for_markers_with_dimensions.csv'

add_image_dimensions(input_csv_path, output_csv_path)