import os

def make_folder_directory(dataset_dir, csv_dir, subset_classes, dataset):

    directory_list = ['train', 'test', 'validation']

    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    if dataset == 'all':
        for directory in directory_list:
            for classes in subset_classes: 
                if classes != '':
                    folder_loc = os.path.join(dataset_dir, classes, 'Labels')
                if not os.path.exists(folder_loc):
                    os.makedirs(folder_loc)
                
    else:
        for classes in subset_classes:
            if classes != '':
                folder_loc = os.path.join(dataset_dir, classes, 'Labels')
            if not os.path.exists(folder_loc):
                os.makedirs(folder_loc)



