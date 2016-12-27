# -*- coding: utf-8 -*-

"""
Organize pictures file into directory tree with year and month.
Use perl exiftool to get creation date and filename from file metadata.

Strongly inspired from the project:
    https://github.com/OneLogicalMyth/Random-Scripts.git

Created on 27/12/16 15:53

@author: vpistis
"""
import filecmp
import datetime
import os
import shutil
import subprocess

# config no trailing slashes please
SOURCE_PATH = "/media/drivemount/user/files/FilesToSort"
DESTINATION_PATH = "/media/drivemount/user/files/FilesSorted"

# If false copy file and don't remove old file
REMOVE_OLD_FILES = False

APPEND_ORIG_FILENAME = False
# process only files with this extensions
FILES_EXTENSIONS = (".mp4", ".3gp")
# FILES_EXTENSIONS = (".jpg", ".gif", ".tiff")
FILENAME_SUFFIX = "VID_"
DATE_FORMAT_OUTPUT = "%Y%m%d_%H%M%S%f"

# in case you use nextcloud or owncloud, set NEXTCLOUD=True to rescan all files
NEXTCLOUD = True
NEXTCLOUD_PATH = "/var/www/html/nextcloud"
NEXTCLOUD_USER = "www-data"

# check if destination path is existing create if not
if not os.path.exists(DESTINATION_PATH):
    os.makedirs(DESTINATION_PATH)


def get_create_date(filename):
    """
    Get creation date from file metadata

    :param filename:
    :return:
    """
    # Read file
    # open_file = open(filename, 'rb')
    command = ["exiftool", "-CreateDate", "-s3", "-fast2", filename]
    metadata = subprocess.check_output(command)

    try:
        # Grab date taken
        datetaken_object = datetime.datetime.strptime(metadata.rstrip(), "%Y:%m:%d %H:%M:%S")

        # Date
        day = str(datetaken_object.day).zfill(2)
        month = str(datetaken_object.month).zfill(2)
        year = str(datetaken_object.year)

        # New Filename
        output = [day, month, year, datetaken_object.strftime(DATE_FORMAT_OUTPUT)]
        return output

    except Exception as e:
        print("{}".format(e))
        return None


def get_file_name(filename):
    """
    Get real filename from metadata

    :param filename:
    :return:
    """
    try:
        command = ["exiftool", "-filename", "-s3", "-fast2", filename]
        metadata = subprocess.check_output(command)
        return metadata.rstrip()
    except Exception as e:
        print("{}".format(e))
        return None


def get_file_ext(filename):
    """
    Return the file extension based on file name from metadata, include point.
    Example return: '.jpg'

    :param filename:
    :return:
    """
    extension = ".{}".format(get_file_name(filename).split(".")[-1])
    return extension


def organize_files():
    """
    Get all files from directory and process

    :return:
    """
    if len(os.listdir(SOURCE_PATH)) <= 0:
        print("No files in path: {}".format(SOURCE_PATH))
        exit()
    else:
        for file in os.listdir(SOURCE_PATH):
            if file.endswith(FILES_EXTENSIONS):

                filename = SOURCE_PATH + os.sep + file
                file_ext = get_file_ext(filename)
                dateinfo = get_create_date(filename)

                try:
                    out_filepath = DESTINATION_PATH + os.sep + dateinfo[2] + os.sep + dateinfo[1]
                    if APPEND_ORIG_FILENAME:
                        out_filename = out_filepath + os.sep + FILENAME_SUFFIX + dateinfo[3] + '_' + file
                    else:
                        out_filename = out_filepath + os.sep + FILENAME_SUFFIX + dateinfo[3] + file_ext

                    # check if destination path is existing create if not
                    if not os.path.exists(out_filepath):
                        os.makedirs(out_filepath)

                    # don't overwrite file if the name is the same
                    if not os.path.exists(out_filename):
                        # copy the file to the organised structure
                        shutil.copy2(filename, out_filename)
                        # verify if file is the same and display output
                        if filecmp.cmp(filename, out_filename):
                            print('File copied with success to {}'.format(out_filename))
                            if REMOVE_OLD_FILES:
                                os.remove(filename)
                                print('Removed old file {}'.format(filename))
                        else:
                            print('File failed to copy :( {}'.format(filename))
                    else:
                        duplicate_filename = out_filename + "_DUPLICATE"
                        shutil.copy2(filename, duplicate_filename)
                        # check if duplicates are the same file
                        if filecmp.cmp(out_filename, duplicate_filename):
                            os.remove(duplicate_filename)
                            print('File already exists: {}'.format(out_filename))
                            if REMOVE_OLD_FILES:
                                os.remove(filename)
                                print('Removed old file {}'.format(filename))
                        else:
                            print('ATTENTION! File and DUPLICATE not the same file: {}'.format(out_filename,
                                                                                               duplicate_filename))

                except Exception as e:
                    print("{}".format(e))
                    print("Exception occurred")
                    exit()
                except None:
                    print('File has no metadata skipped {}'.format(filename))
    return


# Nextcloud initiate a scan
def nextcloud_files_scan():
    if NEXTCLOUD:
        try:
            subprocess.Popen("sudo -u {} php {}/console.php files:scan --all".format(NEXTCLOUD_USER, NEXTCLOUD_PATH),
                             shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            print("{}".format(e))
            print("Exception occurred")
    return


# Execution
organize_files()
nextcloud_files_scan()
