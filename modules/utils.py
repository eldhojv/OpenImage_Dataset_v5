import os
import sys
import shutil
from tqdm import tqdm
from zipfile import ZipFile
from colorama import Fore, Back


def make_folder_directory(dataset_dir, csv_directory, subset_classes, args):

    directory_list = ['train', 'test', 'validation']
    dataset = args.dataset

    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    if dataset == 'all':
        for directory in directory_list:
            for classes in subset_classes: 
                if classes != '':
                    folder_loc = os.path.join(dataset_dir, directory, classes, 'Labels')
                    segmentation_folder_loc = os.path.join(dataset_dir, directory, classes, 'Segmentation')
                    segmentation_mapping_folder_loc = os.path.join(dataset_dir, directory, classes, 'Segmentation Mapping')
                if not os.path.exists(folder_loc):
                    os.makedirs(folder_loc)
                if args.segmentation.lower() == 'true':
                    if not os.path.exists(segmentation_folder_loc):
                        os.mkdir(segmentation_folder_loc)
                    if not os.path.exists(segmentation_mapping_folder_loc):
                        os.mkdir(segmentation_mapping_folder_loc)
                    
                
    else:
        for classes in subset_classes:
            if classes != '':
                folder_loc = os.path.join(dataset_dir,dataset, classes, 'Labels')
                segmentation_folder_loc = os.path.join(dataset_dir, dataset, classes, 'Segmentation')
                segmentation_mapping_folder_loc = os.path.join(dataset_dir, dataset, classes, 'Segmentation Mapping')
            if not os.path.exists(folder_loc):
                os.makedirs(folder_loc)
            if args.segmentation.lower() == 'true':
                if not os.path.exists(segmentation_folder_loc):
                    os.mkdir(segmentation_folder_loc)
                if not os.path.exists(segmentation_mapping_folder_loc):
                    os.mkdir(segmentation_mapping_folder_loc)

def extract_mask_images(dataset_dir, folder):
    mask_images_master_directory = os.path.join(dataset_dir.split('/')[0], 'mask_images', folder)
    zipfile_list = [zipfile_list for zipfile_list in os.listdir(mask_images_master_directory) if zipfile_list.endswith('.zip')]
    for each_zipfile in zipfile_list:
        try:
            file_path = mask_images_master_directory+'/'+each_zipfile
            zipfile_object = ZipFile(file_path)
            uncompressed_size = sum(each_file.file_size for each_file in zipfile_object.infolist())
            extracted_size = 0
            print(Fore.YELLOW+'Extracting: '+each_zipfile+Fore.RESET)
            for each_file in zipfile_object.infolist():
                extracted_size +=each_file.file_size
                percentage_extracted = int(extracted_size*100 / uncompressed_size)
                sys.stdout.write(Fore.BLUE+'\r\r%s %%'%percentage_extracted+" completed \r\r")
                sys.stdout.flush()
                zipfile_object.extract(member = each_file, path = mask_images_master_directory)
        except Exception as e:
            print(Fore.RED+'\nExtraction failed'+Fore.RESET)
            print(e)
            exit(1)

        print(Fore.BLUE+'Extracting: '+each_zipfile+' completed'+Fore.RESET)

    print(Fore.BLUE+'\nAll files Extraction completed'+Fore.RESET)

def delete_mask_images_zipfiles(dataset_dir, folder):
    mask_images_master_directory = os.path.join(dataset_dir.split('/')[0], 'mask_images', folder)
    zipfile_list = [zipfile_list for zipfile_list in os.listdir(mask_images_master_directory) if zipfile_list.endswith('.zip')]
    for each_zipfile in zipfile_list:
        file_path = mask_images_master_directory+'/'+each_zipfile
        if os.path.exists(file_path):
            os.remove(file_path)


def move_mask_images(dataset_dir, folder, classes, segmentation_mask_data):
    mask_images_master_directory = os.path.join(dataset_dir.split('/')[0], 'mask_images', folder)
    segmentation_directory = os.path.join(dataset_dir, folder, classes, 'Segmentation')
    png_image_list = [png_image_list for png_image_list in os.listdir(mask_images_master_directory) if png_image_list.endswith('.png')]
    
    for each_segmentation_mask_data in segmentation_mask_data:
        if each_segmentation_mask_data[0] in png_image_list:
            source_folder = mask_images_master_directory+'/'+each_segmentation_mask_data[0]
            destination_folder = segmentation_directory+'/'+each_segmentation_mask_data[0]
            shutil.move(source_folder, destination_folder)
            write_segmentation_mapping(dataset_dir, folder, classes, each_segmentation_mask_data[0], each_segmentation_mask_data[1])
        else:
            pass  

def write_segmentation_mapping(dataset_dir, folder, classes, mask_id, image_id):
    segmentation_mapping_folder_loc = os.path.join(dataset_dir, folder, classes, 'Segmentation Mapping')
    file_name = image_id+'.txt'
    segmentation_file_name = os.path.join(segmentation_mapping_folder_loc, file_name)
    if os.path.isfile(segmentation_file_name):
        file_object = open(segmentation_file_name, 'a+')
    else:
        file_object = open(segmentation_file_name, 'w+')

    segmentation_mapping_string ="\nDataset: "+folder+" || Subset: "+classes+" || ImageID = "+image_id+" || MaskID = "+mask_id
    file_object.write(str(segmentation_mapping_string))

