import os
import glob
import re
import numpy as np
import pydicom
from pydicom.filereader import read_dicomdir

data_dir = '/Volumes/My4TB/CQ500/'

def RenameFolders():
    for dir_entry in os.scandir(path = data_dir):
        if dir_entry.is_dir():
            dir_re = re.search(pattern = "CQ500CT([0-9]*) CQ500CT([0-9]*)", string = dir_entry.name)
            dir_new = "CQ500-CT-%s" % dir_re.group(1)
            os.rename(data_dir + dir_entry.name, data_dir + dir_new)


# create a dictionary of all the sub directories for each subject directory
# loop through subject directories
for dir_entry in os.scandir(path = data_dir):
    subject_dir_dict = dict()
    if dir_entry.is_dir() and re.match("CQ500-CT-([0-9]*)", dir_entry.name):
        subject_dir_dict[dir_entry.name] = list()
        # print(dir_entry.name)
        
        # loop through sub-directories and exclude some by name
        for sub_dir in os.scandir(dir_entry.path + "/Unknown Study/"):
            if sub_dir.is_dir() and not re.search("(POST|(?<!PRE )CONTRAST|BONE)", sub_dir.name):
                dcm_files = glob.glob(sub_dir.path + "/*.dcm")
                dicom_data = pydicom.read_file(dcm_files[0])

                # add info for these sub-directories to a dictionary
                sub_info = [sub_dir.name, float(dicom_data.PixelSpacing[0]), float(dicom_data.PixelSpacing[1]), float(dicom_data.SliceThickness), len(dcm_files)]
                subject_dir_dict[dir_entry.name].append(sub_info)
                # print(" -{}".format(subject_dir_dict[dir_entry.name][-1]))

        # warn if no usable directories found
        if(len(subject_dir_dict[dir_entry.name]) < 1):
            print("Warning: {subject} found no usable subdirectories".format(subject=dir_entry.name))
            subject_dir_dict.pop(dir_entry.name)    # remove the entry from the dict

        elif(len(subject_dir_dict[dir_entry.name]) > 1):
            
            # parse the remaining directories to find the best candidate scan
            subject_scans = subject_dir_dict[dir_entry.name]

            scans_info = np.array(subject_scans)
            sorted_idx = np.argsort(scans_info[:, 3])

            # check for a 5mm slice scan
            if(scans_info[sorted_idx[-1], 3] == 5.0):
                scans_info_5 = scans_info[scans_info[:, 3] == 5.0]
                print(scans_info_5)
                
                # check if there are two 5mm slice scans
                if(float(scans_info[sorted_idx[-2], 3]) == 5.0):
                    # if more than one 5mm slice scan, use the study with fewest slices
                    sorted_slices_idx = np.argsort(scans_info[:, 4])
                    subject_dir_dict[dir_entry.name] = subject_dir_dict[dir_entry.name][sorted_slices_idx[-1]]  # replace with fewest slices study
                    if(subject_dir_dict[dir_entry.name][4] < 32):
                        print("Warning: Fewer than 32 slices for {}".format(dir_entry.path + "/" + subject_dir_dict[dir_entry.name][0]))
                else:
                    subject_dir_dict[dir_entry.name] = subject_dir_dict[dir_entry.name][sorted_idx[-1]]         # replace entries with the 5mm study

            else:   # no 5mm slice scans, so choose the smallest
                subject_dir_dict[dir_entry.name] = subject_dir_dict[dir_entry.name][sorted_idx[0]]     # replace with the small slice scan


    # convert the chosen study folder to nifti for further processing
    # print(dir_entry.path + "/" + dir_entry.name)

