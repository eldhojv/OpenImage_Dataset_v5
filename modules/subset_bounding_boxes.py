import os
import pandas as pd
from modules.utils import *
from modules.downloader import *
from modules.csv_downloader import *
from colorama import init, Fore, Back, Style


init(convert = True)

def subset_bounding_boxes(args, DEFAULT_DATASET_DIRECTORY):
    if not args.target_dir:
        dataset_dir = os.path.join(DEFAULT_DATASET_DIRECTORY, 'Dataset')
        csv_directory = os.path.join(DEFAULT_DATASET_DIRECTORY, 'csv_folder')
    else:
        dataset_dir = os.path.join(DEFAULT_DATASET_DIRECTORY, args.target_dir)
        csv_directory = os.path.join(DEFAULT_DATASET_DIRECTORY, 'csv_folder')
    
    name_file_csv = 'class-descriptions-boxable.csv'
    CSV_FILE = os.path.join(csv_directory, name_file_csv)


    if args.tool == 'downloader':
        print(Back.RED+"Downloader - Subset with Bounding Boxes(600 classes)"+Back.RESET)
        folder = ['train', 'test', 'validation']
        csv_file_list = ['train-annotations-bbox.csv', 'test-annotations-bbox.csv','validation-annotations-bbox.csv']
        if args.segmentation != None:
            if args.segmentation.lower() == 'true':
                segmentation_dataset = args.dataset
        
        if args.subset.endswith('.txt'):
            with open(args.subset) as file_object:
                contents = file_object.readlines()
                subset_classes = [x.strip('\n') for x in contents]
        else:
            subset_classes = args.subset
            print(subset_classes)    #to delete for testing purpose

        make_folder_directory(dataset_dir, csv_directory, subset_classes, args.dataset) 

        for classes in subset_classes:
            header_value = None
            version_url = 'v5'
            csv_data = read_csv_file(csv_directory, name_file_csv, version_url, header_value) 
            label_code = csv_data.loc[csv_data[1] == classes].values[0][0]

            if args.dataset == 'train':
                csv_file = csv_file_list[0]
                header_value = 0
                version_url = 'v4'
                csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
                print(Fore.YELLOW+"Downloading:  {}".format(classes))
                download(args, csv_data, folder[0], dataset_dir, classes, label_code)

            elif args.dataset == 'test':
                csv_file = csv_file_list[1]
                header_value = 0
                version_url = 'v5'
                csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
                print(Fore.YELLOW+"Downloading:  {}".format(classes))
                download(args, csv_data, folder[1], dataset_dir, classes, label_code)

            elif args.dataset == 'validation':
                csv_file = csv_file_list[2]
                header_value = 0
                version_url = 'v5'
                csv_data = read_csv_file(csv_directory, csv_file, version_url, header_value)
                print(Fore.YELLOW+"Downloading: {}".format(classes))
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
                    print(Fore.YELLOW+"Downloading: {}".format(classes))
                    download(args, csv_data, folder[i], dataset_dir, classes, label_code)
            else:
                print(Fore.RED+"Something went wrong"+Fore.RESET)

                    
            
        
        









    if args.tool == 'ill-downloader':
        print(Back.RED+"Downloader - Subset with Image-Level-Labels")
        print(Back.RED+"Will include in next release")
        # will include in next release





