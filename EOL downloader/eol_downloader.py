import os
import pandas as pd
import requests
import logging


def download_file(url, directory, filename):

    header = requests.utils.default_headers()
    headers.update(
        {
        'User-Agent': 'My User Agent 1.0',
        }
    )
        
        
    response = requests.get(url, headers=headers)
    
    with open(os.path.join(directory, filename), 'wb') as f:
        f.write(response.content)


def main(prev_scientific_name, prev_directory):
    global thread_terminate
    #check_finish()
    #print(1)
    #print(thread_terminate)
    while not thread_terminate:
        #print(thread_terminate, 2)
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
                
                #print('completed')
                eol_size = sum(len(files) for _, _, files in os.walk('EOL_DATASET'))
                if eol_size%1000==0:
                    logging.info(f'we have processed {eol_size} files.')
                    print(f'we have processed {eol_size} files.')

                if eol_size>=df.shape[0]:
                    print('EOL DATASET HAS BEEN SUCCESSFULLY DOWNLOADED!')
                    logging.info('EOL DATASET HAS BEEN SUCCESSFULLY DOWNLOADED!')
                    thread_terminate = True
                    for t in threads:
                        t.join()


if __name__ == '__main__':
    logging.basicConfig(filename='EOL_LOG.txt', level=logging.INFO, format='%(asctime)s — %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    print('program has been started.')
    logging.info('program has been started.')

    from concurrent.futures import ThreadPoolExecutor
    import threading

    global df

    thread_terminate = False
    prev_scientific_name = None
    prev_directory = None
    try:
        if not os.path.exists('EOL_DATASET'):
            os.makedirs('EOL_DATASET')

        df = pd.read_csv('final_eol.csv')
            
        threads = []
        for _ in range(10):  
            t = threading.Thread(target=main, args=(prev_scientific_name, prev_directory))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    except Exception as e:
        logging.error(e)

    #python eol_downloader.py