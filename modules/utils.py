import os
import sys
import cv2
import shutil
import numpy as np
from tqdm import tqdm
from zipfile import ZipFile
from colorama import Fore, Back


def error_log(folder, classes, image):
    error_msg = "Error - Dataset: "+folder+" || Class: "+classes+" || ImageID: "+image+"\n"
    with open("error_log.log", "a+") as fileobject:
        fileobject.write(error_msg)


def make_folder_directory(dataset_dir, csv_directory, subset_classes, args):

    directory_list = ['train', 'test', 'validation']
    dataset = args.dataset

    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    if dataset.lower() == 'all':
        for directory in directory_list:
            for classes in subset_classes: 
                if classes != '':
                    folder_loc = os.path.join(dataset_dir, directory, classes, 'Labels')
                    instance_segmentation_folder_loc = os.path.join(dataset_dir, directory, classes, 'Instance Segmentation')
                    instance_segmentation_mapping_folder_loc = os.path.join(dataset_dir, directory, classes, 'Instance Segmentation Mapping')
                    semantic_segmentation_folder_loc = os.path.join(dataset_dir, directory, classes, 'Semantic Segmentation')
                    dummy_mask_combine_folder_loc = os.path.join(dataset_dir.split('/')[0], 'dummy_mask_combine')

                if not os.path.exists(folder_loc):
                    os.makedirs(folder_loc)
                if args.segmentation.lower() == 'true':
                    if args.segmentation_type.lower() == 'instance':    
                        if not os.path.exists(segmentation_folder_loc):
                            os.mkdir(segmentation_folder_loc)
                        if not os.path.exists(segmentation_mapping_folder_loc):
                            os.mkdir(segmentation_mapping_folder_loc)
                    elif args.segmentation_type.lower() == 'semantic':
                        if not os.path.exists(semantic_segmentation_directory):
                            os.mkdir(semantic_segmentation_directory)
                        if not os.path.exists(dummy_mask_combine_path):
                            os.mkdir(dummy_mask_combine_path)
                    else:
                        pass
                        
                
    else:
        for classes in subset_classes:
            if classes != '':
                folder_loc = os.path.join(dataset_dir, dataset, classes, 'Labels')
                segmentation_folder_loc = os.path.join(dataset_dir, dataset, classes, 'Instance Segmentation')
                segmentation_mapping_folder_loc = os.path.join(dataset_dir, dataset, classes, 'Instance Segmentation Mapping')
                semantic_segmentation_folder_loc = os.path.join(dataset_dir, dataset, classes, 'Semantic Segmentation')
                dummy_mask_combine_folder_loc = os.path.join(dataset_dir.split('/')[0], 'dummy_mask_combine')

            if not os.path.exists(folder_loc):
                os.makedirs(folder_loc)
                
            if args.segmentation.lower() == 'true':
                if args.segmentation_type.lower() == 'instance':    
                    if not os.path.exists(segmentation_folder_loc):
                        os.mkdir(segmentation_folder_loc)
                    if not os.path.exists(segmentation_mapping_folder_loc):
                        os.mkdir(segmentation_mapping_folder_loc)
                elif args.segmentation_type.lower() == 'semantic':
                    if not os.path.exists(semantic_segmentation_folder_loc):
                        os.mkdir(semantic_segmentation_folder_loc)
                    if not os.path.exists(dummy_mask_combine_folder_loc):
                        os.mkdir(dummy_mask_combine_folder_loc)
                else:
                    pass





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
    segmentation_directory = os.path.join(dataset_dir, folder, classes, 'Instance Segmentation')
    png_image_list = [png_image_list for png_image_list in os.listdir(mask_images_master_directory) if png_image_list.endswith('.png')]
    
    for each_segmentation_mask_data in segmentation_mask_data:
        if each_segmentation_mask_data[0] in png_image_list:
            source_file = mask_images_master_directory+'/'+each_segmentation_mask_data[0]
            destination_file = segmentation_directory+'/'+each_segmentation_mask_data[0]
            shutil.copy(source_file, destination_file)
            write_segmentation_mapping(dataset_dir, folder, classes, each_segmentation_mask_data[0], each_segmentation_mask_data[1])
        else:
            pass  

def write_segmentation_mapping(dataset_dir, folder, classes, mask_id, image_id):
    segmentation_mapping_folder_loc = os.path.join(dataset_dir, folder, classes, 'Instance Segmentation Mapping')
    file_name = image_id+'.txt'
    segmentation_file_name = os.path.join(segmentation_mapping_folder_loc, file_name)
    if os.path.isfile(segmentation_file_name):
        file_object = open(segmentation_file_name, 'a+')
    else:
        file_object = open(segmentation_file_name, 'w+')

    segmentation_mapping_string ="Dataset: "+folder+" || Subset: "+classes+" || ImageID = "+image_id+" || MaskID = "+mask_id+'\n'
    file_object.write(str(segmentation_mapping_string))

def combine_mask_images(dataset_dir, folder, classes, segmentation_mask_data):
    mask_images_master_directory = dataset_dir.split('/')[0]+'/'+'mask_images'+'/'+folder
    semantic_segmentation_directory = dataset_dir+'/'+folder+'/'+classes+'/'+'Semantic Segmentation'
    dummy_mask_combine_path = dataset_dir.split('/')[0]+'/'+'dummy_mask_combine'
    each_mask_image_path = dummy_mask_combine_path+'/'+'each_mask_image.png'

    if not os.path.exists(semantic_segmentation_directory):
        os.mkdir(semantic_segmentation_directory)

    if not os.path.exists(dummy_mask_combine_path):
        os.mkdir(dummy_mask_combine_path)


    if len(segmentation_mask_data) > 1:
        source_file = mask_images_master_directory+'/'+segmentation_mask_data[0][0]
        source_file = cv2.imread(source_file)

        for each_segmentation_mask_data in segmentation_mask_data[1:]:
            each_segmentation_file_path = mask_images_master_directory+'/'+ each_segmentation_mask_data[0]
            each_segmentation_image_file = cv2.imread(each_segmentation_file_path)
            if os.path.isfile(each_mask_image_path):
                source_file = cv2.imread(each_mask_image_path)
            source_file = cv2.bitwise_or(source_file, each_segmentation_image_file, mask = None)
            cv2.imwrite(each_mask_image_path,source_file)

        destination_file_name = semantic_segmentation_directory+'/'+segmentation_mask_data[0][1]+'.png'
        source_file = each_mask_image_path
        shutil.copy(source_file, destination_file_name)
        os.remove(each_mask_image_path)
        

    elif len(segmentation_mask_data) == 1:
        source_file = mask_images_master_directory+'/'+segmentation_mask_data[0][0]  
        destination_file = semantic_segmentation_directory+'/'+segmentation_mask_data[0][1]+'.png'
        shutil.copy(source_file, destination_file)
    else:
        pass

            




    '''
    for each_segmentation_mask_data in segmentation_mask_data:
        destination_folder = semantic_segmentation_directory+'/'+each_segmentation_mask_data[1]+'.png'
        if each_segmentation_mask_data[0] in png_image_list:
            if len(each_segmentation_mask_data > 1):    

                source_folder = mask_images_master_directory+'/'+each_segmentation_mask_data[0]
    
            else:
                source_folder = mask_images_master_directory+'/'+each_segmentation_mask_data[0]    
                shutil.move(source_folder, destination_folder)

    





    segmentation_directory = os.path.join(dataset_dir, folder, classes, 'Segmentation')
    png_image_list = [png_image_list for png_image_list in os.listdir(segmentation_directory) if png_image_list.endswith('.png')]
    combined_image = np.zeros((512,512,3))
    for each_segmentation_mask_data in segmentation_mask_data:
        destination_folder = segmentation_directory+'/Instance'+'/'+each_segmentation_mask_data[1]
        if each_segmentation_mask_data[0] in png_image_list:
            source_folder = segmentation_directory+'/'+each_segmentation_mask_data[0]
            combined_image = cv2.bitwise_or(combined_image, source_folder, mask = None)

        cv2.imwrite(combined_image, destination_folder)        
    '''       
        

