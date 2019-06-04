import os
import itertools 
import cv2
from colorama import init, Fore, Back

init(convert = True)

def download(args, csv_data, folder, dataset_dir, classes, label_code):
    image_list = set(csv_data.ImageID[csv_data.LabelName == label_code].values)
    if args.download_limit is not None:
        print("Limiting to {}".format(args.download_limit)+' images')
        image_list = set(itertools.islice(image_list, int(args.download_limit)))
    
    download_images(dataset_dir, folder, classes, image_list)
    if args.image_labels.lower() == 'true':
        download_image_labels(dataset_dir, folder, classes, label_code, csv_data)
    if args.segmentation.lower() == 'true':
        download_segmentation_file(dataset_dir, folder, classes, label_code, csv_data)


def download_images(dataset_dir, folder, classes, image_list):
    target_dir = dataset_dir+"\\"+folder+"\\"+classes
    for image in image_list:
        path = folder+'/'+str(image)+'.jpg'+' "'+target_dir+'\\'+image+'.jpg"'
        aws_command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/'+path
        print(aws_command)
        if os.system(aws_command) != 0:       
            print(Fore.RED+"Error in downloading file -"+image+Fore.RESET)
            error_log(folder, classes, image)
    
    print(Fore.GREEN+"Downloading completed"+Fore.RESET)


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
    
def download_segmentation_file(dataset_dir, folder, classes, label_code, csv_data):
    print("in segmentation function")
            



     
