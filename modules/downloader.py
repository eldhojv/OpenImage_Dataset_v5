import os
import itertools 
import cv2
import urllib.request
from modules.utils import *
from modules.csv_downloader import *
from colorama import init, Fore, Back


init(convert = True)

class_name_file_csv = 'class-descriptions-boxable.csv'

def download(args, csv_data, folder, dataset_dir, classes, label_code):
    image_list = set(csv_data.ImageID[csv_data.LabelName == label_code].values)
    if args.download_limit is not None:
        print("Limiting to {}".format(args.download_limit)+' images')
        image_list = set(itertools.islice(image_list, int(args.download_limit)))
    
    download_images(dataset_dir, folder, classes, image_list)
    if args.image_labels.lower() == 'true':
        download_image_labels(dataset_dir, folder, classes, label_code, csv_data)
    

def download_images(dataset_dir, folder, classes, image_list):
    target_dir = dataset_dir+"/"+folder+"/"+classes
    for image in image_list:
        path = folder+'/'+str(image)+'.jpg'+' "'+target_dir+'/'+image+'.jpg"'
        aws_command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/'+path
        print(aws_command)
        if os.system(aws_command) != 0:       
            print(Fore.RED+"Error in downloading file -"+image+Fore.RESET)
            error_log(folder, classes, image)
    
    print(Fore.GREEN+"Image downloading completed"+Fore.RESET)


def error_log(folder, classes, image):
    error_msg = "Error - Dataset: "+folder+" || Class: "+classes+" || ImageID: "+image+"\n"
    with open("error_log.log", "a+") as fileobject:
        fileobject.write(error_msg)



def download_image_labels(dataset_dir, folder, classes, label_code, csv_data):
    print(Fore.YELLOW+"Creating Labels for: "+classes+" "+Fore.RESET)
    dataset_dir = os.path.join(dataset_dir, folder, classes)
    label_directory = os.path.join(dataset_dir, 'Labels')
    downloaded_image_files =[images.split('.')[0] for images in os.listdir(dataset_dir) if images.endswith('.jpg')]
    
    for each_image_file in downloaded_image_files:
        try:               
            image_file = cv2.imread(os.path.join(dataset_dir, str(each_image_file+'.jpg')))
            image_bbox_data = csv_data.loc[(csv_data.ImageID == each_image_file) & (csv_data.LabelName == label_code)][['XMin','XMax','YMin','YMax']].values.tolist()
            file_name = each_image_file+'.txt'
            label_file_name = os.path.join(label_directory, file_name)

            if os.path.isfile(label_file_name):
                file_object = open(label_file_name, 'a+')
            else:
                file_object = open(label_file_name, 'w+')
            
            for each_bbox_data in image_bbox_data:
                each_bbox_data[0] *= image_file.shape[0]
                each_bbox_data[1] *= image_file.shape[0]
                each_bbox_data[2] *= image_file.shape[1]
                each_bbox_data[3] *= image_file.shape[1]
                #writing to file
                label_string = str('\n'+str(classes)+
                                ": XMin = "+str(each_bbox_data[0])+
                                ", XMax = "+str(each_bbox_data[1])+
                                ", YMin = "+str(each_bbox_data[2])+
                                ", YMax = "+str(each_bbox_data[3]))
                file_object.write(str(label_string))
            
            file_object.close()
                
        except Exception as e:
            print(e)
            print("Failed to write image label values")
    
    print(Fore.BLUE+"Labels creation completed"+Fore.RESET)
    
def download_segmentation_file(csv_directory, dataset_dir, folder, subset_classes, label_code, csv_data):
    if not os.path.exists(os.path.join(dataset_dir.split('/')[0], 'mask_images', folder)):
        os.makedirs(os.path.join(dataset_dir.split('/')[0], 'mask_images', folder))

    download_mask_images(dataset_dir, folder)
    extract_mask_images(dataset_dir, folder)
    delete_mask_images_zipfiles(dataset_dir, folder)

    header_value = None
    version_url = 'v5'
    label_csv_data = read_csv_file(csv_directory, class_name_file_csv, version_url, header_value)

    print(Fore.YELLOW+"Please wait while moving mask_images and creating segmentation mappings"+Fore.RESET)

    for classes in subset_classes:    
        label_code = label_csv_data.loc[label_csv_data[1] == classes].values[0][0]
        class_directory = os.path.join(dataset_dir, folder, classes)
        segmentation_directory = os.path.join(class_directory, 'Segmentation')
        downloaded_image_files = [images.split('.')[0] for images in os.listdir(class_directory) if images.endswith('.jpg')]
        for each_image_file in downloaded_image_files:
            segmentation_mask_data = csv_data.loc[(csv_data.LabelName == label_code) & (csv_data.ImageID == each_image_file)][['MaskPath','ImageID']].values.tolist()
            move_mask_images(dataset_dir, folder, classes, segmentation_mask_data)

    print(Fore.BLUE+"Moving mask_images and segmentation mapping completed"+Fore.RESET)


    
def download_mask_images(dataset_dir, folder):
    mask_suffix = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    mask_images_master_directory = os.path.join(dataset_dir.split('/')[0], 'mask_images', folder)
    zipfile_list = [zipfile_list for zipfile_list in os.listdir(mask_images_master_directory) if zipfile_list.endswith('.zip')]
    if not os.path.exists(mask_images_master_directory):
        os.makedirs(mask_images_master_directory)
    try:
        for each_mask_suffix in mask_suffix:
            file_name = str(folder)+'-masks-'+each_mask_suffix+'.zip'
            if file_name not in zipfile_list:
                file_path = mask_images_master_directory+'/'+file_name
                download_url = str(OPEN_IMAGE_DATASET_URL)+str(OID_VERSION_URL[1])+str(folder)+'-masks/'+str(file_name)
                print(Fore.YELLOW+'Downloading {}'.format(file_name))
                urllib.request.urlretrieve(download_url, file_path, reporthook = download_progress)
                print(Fore.BLUE+'\nSuccessfully downloaded {}'.format(file_name)+Fore.RESET)
    except Exception as e:
        print(e)
        print(Fore.RED+"Mask Images downloading failed"+Fore.RESET) 
        download_failed_file = mask_images_master_directory+file_name    
        delete_failed_download(download_failed_file)
        print("Do you want to continue download"+Fore.BLUE+"[Y/N]"+Fore.RESET)        
        user_response = input()
        if user_response.lower() == 'y':
            download_mask_images(dataset_dir, folder)
        else:    
            exit(1)


     
