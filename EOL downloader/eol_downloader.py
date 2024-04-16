import os
import pandas as pd
import requests

def check_finish():
    if len(os.listdir('EOL_DATASET'))==df.shape[0]:
        print('EOL DATASET HAS BEEN SUCCESSFULLY DOWNLOADED!')
        exit()
    

def download_file(url, directory, filename):
    response = requests.get(url)
    
    with open(os.path.join(directory, filename), 'wb') as f:
        f.write(response.content)


def mainn(prev_scientific_name, prev_directory):

    check_finish()
    
    for index, row in df.iterrows():
        if not os.path.exists(os.path.join(os.getcwd(), 'EOL_DATASET', row['scientific_name'], row['eol_full-size_copy_url'].rsplit('/', 1)[-1])):
            
            scientific_name = row['scientific_name']
            url = row['eol_full-size_copy_url']
            
            if scientific_name != prev_scientific_name:
                prev_scientific_name = scientific_name
                prev_directory = os.path.join(os.getcwd(), 'EOL_DATASET', scientific_name)
                if not os.path.exists(prev_directory):
                    os.makedirs(prev_directory)
            
            
            filename = url.split('/')[-1]
            download_file(url, prev_directory, filename)
            
            print('completed')


if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
    import threading
    
    if not os.path.exists('EOL_DATASET'):
        os.makedirs('EOL_DATASET')

    global df
    df = pd.read_csv('final_eol.csv')

    prev_scientific_name = None
    prev_directory = None

    threads = []
    for _ in range(10):  
        t = threading.Thread(target=mainn, args=(prev_scientific_name, prev_directory))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    