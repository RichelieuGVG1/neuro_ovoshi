from PIL import Image
import os
import time

def resize_images(source_dir, max_size=640):
  
    if not os.path.exists(source_dir):
        raise FileNotFoundError("Source directory not found.")
    
    print("Working with directory started. Processing:")
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
                    img = img.convert('RGB')  

                    img.save(destination_file_path.replace('.png', '.jpg'), format='JPEG')
                    print(destination_file_path)

    print("\n\nProgram finished. Final dataset is available with the root:", destination_dir)

if __name__ == "__main__":
    source_folder = input("Enter path to source directory: ")
    start = time.time()

    try:
        resize_images(source_folder)
        print('\nThe program worked normally.')
        print('Time taken:', time.time() - start, 'seconds.\n')

    except Exception as e:
        print('Something went wrong.\n', e)
    finally:
        input('Press Enter to continue...')
