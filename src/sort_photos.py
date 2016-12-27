# -*- coding: utf-8 -*-

"""
Forked and inspired from the project:
    https://github.com/OneLogicalMyth/Random-Scripts.git

Created on 27/12/16 15:53

@author: vpistis
"""

import exifread
import datetime
import hashlib
import os
import shutil
import subprocess

# config no trailing slashes please
SOURCE_PATH = "/media/drivemount/user/files/PhotosToSort"
DESTINATION_PATH = "/media/drivemount/user/files/PhotosSorted"

# If false copy file and don't remove old file
REMOVE_OLD_FILES = False

# various configurations
APPEND_ORIG_FILENAME = False
FILENAME_SUFFIX = "IMG_"
DATE_FORMAT_OUTPUT = "%Y%m%d_%H%M%S"

# in case you use nextcloud or owncloud, set NEXTCLOUD=True to rescan all files
NEXTCLOUD = True
NEXTCLOUD_PATH = "/var/www/html/nextcloud"
NEXTCLOUD_USER = "www-data"

# check if destination path is existing create if not
if not os.path.exists(DESTINATION_PATH):
    os.makedirs(DESTINATION_PATH)


# file hash function
def hash_file(filename):
    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


# picture date taken function
def date_taken_info(filename):
    # Read file
    open_file = open(filename, 'rb')

    # Return Exif tags
    tags = exifread.process_file(open_file, stop_tag='Image DateTime')
    # .strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Grab date taken
        datetaken_string = tags['Image DateTime']
        datetaken_object = datetime.datetime.strptime(datetaken_string.values, '%Y:%m:%d %H:%M:%S')

        # Date
        day = str(datetaken_object.day).zfill(2)
        month = str(datetaken_object.month).zfill(2)
        year = str(datetaken_object.year)
        # # Time
        # second = str(datetaken_object.second).zfill(2)
        # minute = str(datetaken_object.minute).zfill(2)
        # hour = str(datetaken_object.hour).zfill(2)

        # New Filename
        output = [day, month, year, datetaken_object.strftime(DATE_FORMAT_OUTPUT)]
        return output

    except Exception as e:
        print("{}".format(e))
        return None


# get all picture files from directory and process

if len(os.listdir(SOURCE_PATH)) <= 0:
    print("No files in path: {}".format(SOURCE_PATH))
    exit()
else:
    for file in os.listdir(SOURCE_PATH):
        if file.endswith('.jpg'):
            filename = SOURCE_PATH + os.sep + file
            dateinfo = date_taken_info(filename)
            try:
                out_filepath = DESTINATION_PATH + os.sep + dateinfo[2] + os.sep + dateinfo[1]
                if APPEND_ORIG_FILENAME:
                    out_filename = out_filepath + os.sep + FILENAME_SUFFIX + dateinfo[3] + '_' + file
                else:
                    out_filename = out_filepath + os.sep + FILENAME_SUFFIX + dateinfo[3] + '.jpg'

                # check if destination path is existing create if not
                if not os.path.exists(out_filepath):
                    os.makedirs(out_filepath)

                # copy the picture to the organised structure
                shutil.copy2(filename, out_filename)

                # verify if file is the same and display output
                if hash_file(filename) == hash_file(out_filename):
                    print('File copied with success to ' + out_filename)
                    if REMOVE_OLD_FILES:
                        os.remove(filename)
                        print('Removed old file' + filename)
                else:
                    print('File failed to copy :( ' + filename)

            except Exception as e:
                print("{}".format(e))
                print("Exception occurred")
                exit()
            except None:
                print('File has no exif data skipped ' + filename)
                exit()

# Nextcloud initate a scan
if NEXTCLOUD:
    try:
        subprocess.Popen("sudo -u {} php {}/console.php files:scan --all".format(NEXTCLOUD_USER, NEXTCLOUD_PATH),
                         shell=True, stdout=subprocess.PIPE)
    except Exception as e:
        print("{}".format(e))

exit()
