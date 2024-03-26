

# Путь к папкам train и train_mini
train_dir = '/Users/romeo/Desktop/test_merge_inaturalist/train'
train_mini_dir = '/Users/romeo/Desktop/test_merge_inaturalist/train_mini'

import os
from PIL import Image
from imagehash import phash
from collections import defaultdict

def get_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]



train_folders = os.listdir(train_dir)
train_mini_folders = os.listdir(train_mini_dir)

common_images_count = defaultdict(int)

for folder in train_folders:
    if folder in train_mini_folders:
        train_images = get_files_in_directory(os.path.join(train_dir, folder))
        train_mini_images = get_files_in_directory(os.path.join(train_mini_dir, folder))
        
        train_hashes = {image: phash(Image.open(os.path.join(train_dir, folder, image))) for image in train_images}
        train_mini_hashes = {image: phash(Image.open(os.path.join(train_mini_dir, folder, image))) for image in train_mini_images}
        
        for image_name, hash_value in train_hashes.items():
            image_path = os.path.join(train_dir, folder, image_name)
            with Image.open(image_path) as img:
                img_hash = phash(img)
                if any(img_hash - mini_hash < 5 for mini_hash in train_mini_hashes.values()):
                    common_images_count[folder] += 1

for folder, count in common_images_count.items():
    print(f"В папке {folder} содержится {count} общих фотографий.")
