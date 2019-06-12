import os
import sys
import time
import pandas as pd
import urllib.request
from colorama import init, Fore, Back, Style

OPEN_IMAGE_DATASET_URL = 'https://storage.googleapis.com/openimages/'
OID_VERSION_URL = ['2018_04/','v5/']   

init(autoreset = True)

def read_csv_file(csv_directory, file_name, version_url, header_value = None):
    check_file_present(csv_directory, file_name, version_url)
    csv_file = os.path.join(csv_directory, file_name)
    if os.path.isfile(os.path.join(csv_directory, file_name)):
        print(Fore.YELLOW+'Please wait while parsing: '+file_name+' '+Fore.RESET)
        csv_data = pd.read_csv(csv_file, header = header_value)
        print(Fore.BLUE+'Parsing '+file_name+' completed')
        return csv_data

def check_file_present(csv_directory, file_name, version_url):

    if file_name == 'train-annotations-bbox.csv':
        if version_url == 'v4':
            version_url = OID_VERSION_URL[0]+file_name.split('-')[0]+'/'
        else:
            version_url = OID_VERSION_URL[0]
    else:
        version_url = OID_VERSION_URL[1]
    
    if not os.path.isfile(os.path.join(csv_directory, file_name)):
        print(Fore.RED+ '>>File not present: '+Fore.RESET+file_name)
        print('Do you want to download the file '+Fore.BLUE+'[Y/N]')
        user_response = input()
        if user_response.lower() == 'y':
            download_url = str(OPEN_IMAGE_DATASET_URL+version_url+file_name)
            print(download_url)    # to delete for testing purpose
            file_path = os.path.join(csv_directory, file_name)
            download_csv_file(download_url, file_path)
        else:
            print(Fore.RED+' ** Exiting program **')
            exit(1)


def download_csv_file(download_url, file_path):
    try:
        print('Downloading: '+os.path.split(file_path)[-1])
        urllib.request.urlretrieve(download_url, file_path, reporthook = download_progress)
        print('\nSuccessfully downloaded file {}'.format(file_path))
    except Exception as e:
        print(Fore.RED+'\nDownloading failed')
        delete_failed_download(file_path)
        print(e)
        exit(1)


    
def download_progress(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / ((1024 * duration) + 1e-5))
    percent = int(count * block_size * 100 / (total_size + 1e-5))
    sys.stdout.write(Fore.BLUE+"\r\r%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration)+"\r\r")
    sys.stdout.flush()
    
    

def delete_failed_download(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

