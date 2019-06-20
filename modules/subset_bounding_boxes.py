import os
import pandas as pd
from modules.utils import *
from modules.downloader import *
from modules.csv_downloader import *
from colorama import init, Fore, Back, Style


init(convert = True)

def subset_bounding_boxes(args, DEFAULT_DATASET_DIRECTORY):
    if not args.target_dir:
        dataset_dir = DEFAULT_DATASET_DIRECTORY+'/'+'Dataset'
        csv_directory = DEFAULT_DATASET_DIRECTORY+'/'+'csv_folder'
    else:
        dataset_dir = DEFAULT_DATASET_DIRECTORY+'/'+args.target_dir
        csv_directory = DEFAULT_DATASET_DIRECTORY+'/'+'csv_folder'
    
    class_name_file_csv = 'class-descriptions-boxable.csv'
    CSV_FILE = os.path.join(csv_directory, class_name_file_csv)


    if args.tool == 'downloader':
        print(Back.RED+"Downloader - Subset with Bounding Boxes(600 classes)"+Back.RESET)
        folder = ['train', 'test', 'validation']
        csv_file_list = ['train-annotations-bbox.csv', 'test-annotations-bbox.csv','validation-annotations-bbox.csv']
        segmentation_csv_file_list = ['train-annotations-object-segmentation.csv', 'test-annotations-object-segmentation.csv', 'validation-annotations-object-segmentation.csv']
        if args.segmentation != None:
            if args.segmentation.lower() == 'true':
                segmentation_dataset = args.dataset
        
        if args.subset.endswith('.txt'):
            with open(args.subset) as file_object:
                contents = file_object.readlines()
                subset_classes = [x.strip('\n') for x in contents]
        else:
            subset_classes = args.subset.split(',')
            
        

        make_folder_directory(dataset_dir, csv_directory, subset_classes, args) 


        #reading class-descriptions-boxable.csv
        header_value = None
        version_url = 'v5'
        label_csv_data = read_csv_file(csv_directory, class_name_file_csv, version_url, header_value) 

        #-------------------------------Dataset Image download (train, test and validation) ----------------------------
        if args.dataset == 'all':
            header_value = 0
            for each_folder in folder:
                if each_folder == 'train':
                    version_url = 'v4'
                else:
                    version_url = 'v5'

                csv_file = csv_file_list[folder.index(each_folder)]
                csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)

                for classes in subset_classes:
                    print(Fore.YELLOW+"Downloading:  {}".format(classes))
                    label_code = label_csv_data.loc[label_csv_data[1] == classes].values[0][0]
                    download(args, csv_data, each_folder, dataset_dir, classes, label_code)


        elif args.dataset in folder:
            each_folder = args.dataset
            header_value = 0
            if each_folder == 'train':
                version_url = 'v4'
            else:
                version_url = 'v5'
            
            csv_file = csv_file_list[folder.index(each_folder)]
            csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)

            for classes in subset_classes:
                print(Fore.YELLOW+"Downloading:  {}".format(classes))
                label_code = label_csv_data.loc[label_csv_data[1] == classes].values[0][0]
                download(args, csv_data, each_folder, dataset_dir, classes, label_code)

        else:
            print(Fore.RED+"Dataset ERROR - please check dataset"+Fore.RESET)
        
        #-------------------------------End Dataset Image download (train, test and validation) ----------------------------

        #-------------------------------Start Segmentation Image download----------------------------
        if args.segmentation == 'true':      
            if args.dataset == 'all':
                for each_folder in folder:
                    csv_file = segmentation_csv_file_list[folder.index(each_folder)]
                    header_value = 0
                    version_url = 'v5'
                    csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
                    download_segmentation_file(csv_directory, dataset_dir, each_folder, subset_classes, label_code, csv_data, args.segmentation_type)

            elif args.dataset in folder:
                each_folder = args.dataset
                csv_file = segmentation_csv_file_list[folder.index(each_folder)]
                header_value = 0
                version_url = 'v5'  
                csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
                download_segmentation_file(csv_directory, dataset_dir, each_folder, subset_classes, label_code, csv_data, args.segmentation_type)

            else:
                print(Fore.RED+"Segmentation ERROR - please check dataset"+Fore.RESET)

            #-------------------------------End Segmentation Image download----------------------------



     #-------------------------------Start Image Level downloader----------------------------
    if args.tool == 'ill-downloader':
        print(Back.RED+"Downloader - Subset with Image-Level-Labels")
        print(Back.RED+"Will include in next release")
        # will include in next release



'''
#-------old code for downloading dataset images-----------------

        if args.dataset == 'train':
            csv_file = csv_file_list[0]
            header_value = 0
            version_url = 'v4'
            csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
            for classes in subset_classes:
                print(Fore.YELLOW+"Downloading:  {}".format(classes))
                label_code = label_csv_data.loc[label_csv_data[1] == classes].values[0][0]
                download(args, csv_data, folder[0], dataset_dir, classes, label_code)

        elif args.dataset == 'test':
            csv_file = csv_file_list[1]
            header_value = 0
            version_url = 'v5'
            csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
            for classes in subset_classes:
                print(Fore.YELLOW+"Downloading:  {}".format(classes))
                label_code = label_csv_data.loc[label_csv_data[1] == classes].values[0][0]
                download(args, csv_data, folder[1], dataset_dir, classes, label_code)

        elif args.dataset == 'validation':
            csv_file = csv_file_list[2]
            header_value = 0
            version_url = 'v5'
            csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
            for classes in subset_classes:
                print(Fore.YELLOW+"Downloading:  {}".format(classes))
                label_code = label_csv_data.loc[label_csv_data[1] == classes].values[0][0]
                download(args, csv_data, folder[2], dataset_dir, classes, label_code)

        elif args.dataset == 'all':
            for i in range(len(folder)):
                header_value = 0
                if folder[i] == 'train':
                    version_url = 'v4'
                else:
                    version_url = 'v5'
                csv_file = csv_file_list[i]
                csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
                for classes in subset_classes:
                    print(Fore.YELLOW+"Downloading:  {}".format(classes))
                    label_code = label_csv_data.loc[label_csv_data[1] == classes].values[0][0]
                    download(args, csv_data, folder[i], dataset_dir, classes, label_code)
        else:
            print(Fore.RED+"Something went wrong"+Fore.RESET)
'''


                

                    
            
        
        









    





