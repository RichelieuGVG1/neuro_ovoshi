import os
import shutil


root_folder = 'D:/Datasets(59-113)/resize_iNaturalist/resized_train_mini'


def create_folder_structure(root_folder):

    for folder_name in os.listdir(root_folder):

        current_folder = os.path.join(root_folder, folder_name)

        if os.path.isdir(current_folder) and '_' in folder_name:

            folder_parts = folder_name.split('_')
            folder_parts = folder_parts[1:]
            destination_folder = root_folder

            for part in folder_parts[:-1]:
                destination_folder = os.path.join(destination_folder, part)
                if not os.path.exists(destination_folder):
                    os.mkdir(destination_folder)

            destination_folder = os.path.join(destination_folder, folder_parts[-1])

            if not os.path.exists(destination_folder):
                os.mkdir(destination_folder)

            for file_name in os.listdir(current_folder):
                source_file = os.path.join(current_folder, file_name)
                shutil.copy(source_file, destination_folder)
            print(f"Создана структура для {folder_name}")

create_folder_structure(root_folder)
