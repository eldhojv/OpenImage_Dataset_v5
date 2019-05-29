import argparse

def parser_arguments():
    parser = argparse.ArgumentParser(description = "Downloader tool for OpenImage Dataset v4 and v5")
    parser.add_argument("--tool", required = True, 
                        metavar = 'downloader, ill-downloader', choices = ['downloader', 'ill-downloader'],
                        help = "<downloader> Subset with BBox /OR/ <ill-downloader> for image-level-labels subset")
    parser.add_argument("--version", required = False, default = 'v5', choices = ['v4', 'v5'],
                        metavar = "v4 or v5", help = "OpenImage Dataset version" )
    parser.add_argument("--target_dir", required = False, 
                        metavar = "[target-directory]/OpenImageDataset", 
                        help = "Directory to save OpenImage dataset")
    parser.add_argument("--dataset", required = True, choices = ['train', 'test', 'validation', 'all'],
                        metavar = "[train, test, validation, all]",
                        help = "Specify which dataset is needed (training, test, validation or all )")
    parser.add_argument("--subset", required = True, 
                        metavar = "[Apple, Orange]", 
                        help = "Specify which subset of data to download")
    parser.add_argument("--segmentation", required = False, choices = ['true','false'],
                        metavar = "true or false",
                        help = "download segmentation files(related to subset)")

    # ----------- not needed -----------------------                    
    # parser.add_argument("--relationship", required = False, choices = ['true','false'],
    #                     metavar = "true or false",
    #                     help = "download relationship files(related to subset)")
    # parser.add_argument("--imagelabels", required = False, choices = ['true', 'false'],
    #                     metavar = "true or false",
    #                     help = "download Image Labels(related to subset)")
    # ----------------------------------------------


    #result = parser.parse_args()
    #print(result.version)
    return parser.parse_args()


parser_arguments()