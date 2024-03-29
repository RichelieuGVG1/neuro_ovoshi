import os
from PIL import Image
import time
import sys

def f(source_dir, max_size=640):
    
    if not os.path.exists(source_dir):
        raise FileNotFoundError
        exit()
        
    print("working with directory started. processing:")
    destination_dir = os.path.join(os.path.dirname(source_dir), 'resized_' + os.path.basename(source_dir))
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')):
                
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_file_path, source_dir)
                destination_file_path = os.path.join(destination_dir, relative_path)

                
                os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

                
                with Image.open(source_file_path) as img:
                    width, height = img.size

                    if width > height:
                        new_width = max_size
                        new_height = int(height * (max_size / width))
                    else:
                        new_width = int(width * (max_size / height))
                        new_height = max_size

                    
                    img = img.resize((new_width, new_height), Image.LANCZOS)

                    img.save(destination_file_path)
                    print(source_file_path)

    print("\n\nprogramm finished. final dataset is avaliable with the root: ", destination_dir)


start=time.time()
try:
    f(sys.argv[1])
    print('\nthe program worked normally')
    print('counted in:', time.time()-start, 'sec.\n')

except Exception as e:
    print('something went wrong.\n', e)

finally:
    os.system('pause')
