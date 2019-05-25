import os
import sys
import time
import pandas as pd
import urllib.request
from colorama import init, Fore, Back, Style

OPEN_IMAGE_DATASET_URL = 'https://storage.googleapis.com/openimages/2018_04/test/'

########################################################################################################
#contains information about the bounding boxes

BOXES_TRAIN = 'https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv'
BOXES_VALIDATION = 'https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv'
BOXES_TEST = 'https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv'

########################################################################################################
#contains segmentation datas

SEGMENTATION_TRAIN = 'https://storage.googleapis.com/openimages/v5/train-masks/train-masks-0.zip'
SEGMENTATION_TRAIN_MASK = 'https://storage.googleapis.com/openimages/v5/train-annotations-object-segmentation.csv'

SEGMENTATION_VALIDATION = 'https://storage.googleapis.com/openimages/v5/validation-masks/validation-masks-0.zip'
SEGMENTATION_VALIDATION_MASK = 'https://storage.googleapis.com/openimages/v5/validation-annotations-object-segmentation.csv'

SEGMENTATION_TEST = 'https://storage.googleapis.com/openimages/v5/test-masks/test-masks-0.zip'
SEGMENTATION_TEST_MASK = 'https://storage.googleapis.com/openimages/v5/test-annotations-object-segmentation.csv'

########################################################################################################
#not needed
IMAGE_LABELS_TRAIN = 'https://storage.googleapis.com/openimages/v5/train-annotations-human-imagelabels-boxable.csv'
IMAGE_LABELS_VALIDATION = 'https://storage.googleapis.com/openimages/v5/validation-annotations-human-imagelabels-boxable.csv'
IMAGE_LABELS_TEST = 'https://storage.googleapis.com/openimages/v5/test-annotations-human-imagelabels-boxable.csv'

########################################################################################################
#contains url to download the image file

IMAGE_ID_TRAIN = 'https://storage.googleapis.com/openimages/2018_04/train/train-images-boxable-with-rotation.csv'
IMAGE_ID_VALIDATION = 'https://storage.googleapis.com/openimages/2018_04/validation/validation-images-with-rotation.csv'
IMAGE_ID_TEST = 'https://storage.googleapis.com/openimages/2018_04/test/test-images-with-rotation.csv'

########################################################################################################
METADATA_CLASS_NAME = 'https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv'


csv_directory = os.path.join(os.path.dirname(os.getcwd()),'OpenImageDataset\csv_folder')
file_name = 'test-images-with-rotation.csv'

init(autoreset = True)

def read_csv_file(csv_directory, file_name):
    check_file_present(csv_directory, file_name)
    csv_file = os.path.join(csv_directory, file_name)
    #csv_data = pd.read_csv(csv_file)
    #return csv_data

def check_file_present(csv_directory, file_name):
    if not os.path.isfile(os.path.join(csv_directory, file_name)):
        print(Fore.RED+ '** File not present **')
        print('Do you want to download the file '+Fore.BLUE+'[Y/N]')
        user_response = input()
        if user_response.lower() == 'y':
            download_url = str(OPEN_IMAGE_DATASET_URL+file_name)
            file_path = os.path.join(csv_directory, file_name)
            download_csv_file(download_url, file_path)
        else:
            print(Fore.RED+' ** Exiting program **')
            exit(1)


def download_csv_file(download_url, file_path):
    try:
        print('Downloading: '+os.path.split(file_path)[-1])
        urllib.request.urlretrieve(download_url, file_path, reporthook = download_progress)
    except Exception as e:
        print(Fore.RED+'\nDownloading failed')
        delete_failed_download(file_path)
        print(e)


    
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




        




read_csv_file(csv_directory, file_name)

