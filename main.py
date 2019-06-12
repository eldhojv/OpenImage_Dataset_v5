#---------------------------------------------------------
#
# Author : Eldho
# Contibutors : 
# Written Date   : 27/05/2019
# Modified date :
# Project to download OpenImage Dataset version 5
# 
#---------------------------------------------------------

import os
#from modules.csv_downloader import *
from modules.command_line_parser import *
from modules.subset_bounding_boxes import *

ROOT_DIR = ''
DEFAULT_DATASET_DIRECTORY = os.path.join(ROOT_DIR,'OpenImageDataset')


if __name__ == "__main__":
    args = parser_arguments()

if args.tool == 'downloader':
    subset_bounding_boxes(args, DEFAULT_DATASET_DIRECTORY)
    # if args.version == 'v5':
    #     subset_bounding_boxes(args, DEFAULT_DATASET_DIRECTORY)
    # elif args.version == 'v4':
    #     print("version v4 not available")
    #     exit(1)
    # else:
    #     print("Enter version v4 or v5")
