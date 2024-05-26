import os
from typing import Dict
import pandas as pd
import shutil
import zipfile
from PIL import Image

def subshard_path(root: str, shard_id: int, subshard_id: int) -> str:
    return os.path.join(root, "{:04d}_{:04d}".format(shard_id, subshard_id))

def zip_shard(shard_dir: str) -> None:
    zip_filename = shard_dir + '.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(shard_dir):
            for file in files:
                zipf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file), os.path.join(shard_dir, '..')))

def add_to_shard(image_path: str, dataset_name: str, shard_root: str, taxonomy_df: pd.DataFrame) -> None:
    shard_id = os.path.basename(shard_root)
    subshard_id = 0
    columns = [
        'dataset_name', 'common_species', 'common_variety', 'kingdom', 'phylum',
        'class', 'order', 'family', 'subfamily', 'genus', 'species',
        'image_path', 'height', 'width', 'disease', 'rot', 'age', 'maturity', 'quantity', 'weight',
        'part_of_a_plant', 'background_type'
    ]

    while True:
        subshard_dir = subshard_path(shard_root, int(shard_id), subshard_id)
        csv_file = os.path.join(shard_root, f"{shard_id}_{subshard_id:04d}.csv")

        if not os.path.exists(csv_file):
            os.makedirs(subshard_dir, exist_ok=True)
            pd.DataFrame(columns=columns).to_csv(csv_file, index=False)
            break
        else:
            subshard_data = pd.read_csv(csv_file)
            if len(subshard_data) < 1000:
                break
            else:
                subshard_id += 1

    csv_data = pd.read_csv(csv_file)

    species_folder = os.path.basename(os.path.dirname(image_path))
    taxonomy_row = None
    if 'common_variety' in taxonomy_df.columns:
        taxonomy_row = taxonomy_df[taxonomy_df['common_variety'] == species_folder]
    if taxonomy_row is None or taxonomy_row.empty:
        if 'common_species' in taxonomy_df.columns:
            taxonomy_row = taxonomy_df[taxonomy_df['common_species'] == species_folder]

    if taxonomy_row is None or taxonomy_row.empty:
        print(f"Ошибка: Таксономическая информация для {species_folder} не найдена.")
        return

    taxonomy_info = taxonomy_row.iloc[0]
    species_info: Dict[str, any] = {
        'dataset_name': dataset_name,
        'image_path': os.path.relpath(image_path, shard_root),
        'height': None,
        'width': None
    }
    for column in csv_data.columns:
        if column not in ['dataset_name', 'image_path', 'height', 'width']:
            species_info[column.lower().replace(' ', '_')] = taxonomy_info.get(column, None)

    img = Image.open(image_path)
    width, height = img.size
    species_info['height'] = height
    species_info['width'] = width

    image_filename = os.path.basename(image_path)
    target_image_path = os.path.join(subshard_dir, image_filename)
    shutil.copy(image_path, target_image_path)

    new_row = pd.DataFrame([species_info], columns=[col.lower().replace(' ', '_') for col in columns])
    csv_data = pd.concat([csv_data, new_row], ignore_index=True)
    csv_data.to_csv(csv_file, index=False)

    csv_file_parent = os.path.join(os.path.dirname(shard_root), f"{shard_id}.csv")
    if not os.path.exists(csv_file_parent):
        pd.DataFrame(columns=[col.lower().replace(' ', '_') for col in columns]).to_csv(csv_file_parent, index=False)
    csv_data_parent = pd.read_csv(csv_file_parent)
    csv_data_parent = pd.concat([csv_data_parent, new_row], ignore_index=True)
    csv_data_parent.to_csv(csv_file_parent, index=False)

    if len(csv_data) == 1000:
        zip_shard(subshard_dir)

def main(dataset_name: str, shard_root: str, taxonomy_file: str, image_dir: str) -> None:
    taxonomy_df = pd.read_csv(taxonomy_file)
    for column in taxonomy_df.columns:
        if column != 'image_path' and taxonomy_df[column].dtype == 'object':
            taxonomy_df[column] = taxonomy_df[column].str.replace(' ', '_').str.lower()

    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith(".jpg"):
                image_path = os.path.join(root, file)
                add_to_shard(image_path, dataset_name, shard_root, taxonomy_df)

if __name__ == "__main__":
    dataset_name = "tomato_cultivars"
    shard_root = "/Users/romeo/Desktop/Dataset Processing/0000"
    taxonomy_file = "/Users/romeo/Desktop/Dataset Processing/tomato_cultivars/taxonomy.csv"
    image_dir = "/Users/romeo/Desktop/Dataset Processing/tomato_cultivars"
    main(dataset_name, shard_root, taxonomy_file, image_dir)
