# -*- coding: utf-8 -*-

"""
Organize pictures file into directory tree with year and month.
Use perl exiftool to get creation date and filename from file metadata.

Strongly inspired from the project:
    https://github.com/OneLogicalMyth/Random-Scripts.git

Created on 27/12/16 15:53

@author: vpistis
"""

import datetime
import filecmp
import os
import shutil
import subprocess
import sys
import timeit
from utils import Logger, get_setting, which

sys.stdout = Logger()

PROCESS_IMAGES = get_setting("PROCESS_IMAGES")
PROCESS_VIDEOS = get_setting("PROCESS_VIDEOS")

IMAGES_SOURCE_PATH = get_setting("IMAGES_SOURCE_PATH")
IMAGES_DESTINATION_PATH = get_setting("IMAGES_DESTINATION_PATH")
IMAGE_FILES_EXTENSIONS = tuple(get_setting("IMAGE_FILES_EXTENSIONS"))
IMAGE_FILENAME_SUFFIX = get_setting("IMAGE_FILENAME_SUFFIX")

VIDEOS_SOURCE_PATH = get_setting("VIDEOS_SOURCE_PATH")
VIDEOS_DESTINATION_PATH = get_setting("VIDEOS_DESTINATION_PATH")
VIDEO_FILES_EXTENSIONS = tuple(get_setting("VIDEO_FILES_EXTENSIONS"))
VIDEO_FILENAME_SUFFIX = get_setting("VIDEO_FILENAME_SUFFIX")

# If false copy file and don't remove old file
REMOVE_OLD_FILES = get_setting("REMOVE_OLD_FILES")
APPEND_ORIG_FILENAME = get_setting("APPEND_ORIG_FILENAME")
# if RENAME_SORTED_FILES=False, use this date format for naming files
DATE_FORMAT_OUTPUT = get_setting("DATE_FORMAT_OUTPUT")
# if false, sorted files keep their original name, else rename using CreateDate
RENAME_SORTED_FILES = get_setting("RENAME_SORTED_FILES")
# in case you use nextcloud or owncloud, set NEXTCLOUD=True to rescan all files
NEXTCLOUD = get_setting("NEXTCLOUD")
NEXTCLOUD_PATH = get_setting("NEXTCLOUD_PATH")
NEXTCLOUD_USER = get_setting("NEXTCLOUD_USER")


def get_create_date(filename):
    """
    Get creation date from file metadata

    :param filename:
    :return: [day, month, year, "%Y:%m:%d %H:%M:%S"]
    """
    command = ["exiftool", "-CreateDate", "-s3", "-fast2", filename]
    create_date = subprocess.check_output(command, universal_newlines=True)

    if not create_date:
        command = ["exiftool", "-DateTimeOriginal", "-s3", "-fast2", filename]
        datetime_original = subprocess.check_output(command, universal_newlines=True)
        metadata = datetime_original
    if not metadata:
        command = ["exiftool", "-filemodifydate", "-s3", "-fast2", filename]
        file_modify_date = subprocess.check_output(command, universal_newlines=True)
        metadata = file_modify_date.split("+")[0]

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
        print("exiftool is not installed or datetime is unknown")
        return None


def get_sub_sec_time_original(filename):
    """
    Get SubSecTimeOriginal from file metadata if exists

    :param filename:
    :return:
    """
    try:
        command = ["exiftool", "-SubSecTimeOriginal", "-s3", "-fast2", filename]
        metadata = subprocess.check_output(command, universal_newlines=True)
        # print(str(metadata.rstrip()))
        return metadata.rstrip()
    except Exception as e:
        print("{}".format(e))
        print("exiftool is installed?")
        return None


def get_file_name(filename):
    """
    Get real filename from metadata

    :param filename:
    :return:
    """
    try:
        command = ["exiftool", "-filename", "-s3", "-fast2", filename]
        metadata = subprocess.check_output(command, universal_newlines=True)
        # print(str(metadata.rstrip()))
        return metadata.rstrip()
    except Exception as e:
        print("{}".format(e))
        print("exiftool is installed?")
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


def organize_files(src_path, dest_path, files_extensions, filename_suffix=""):
    """
    Get all files from directory and process

    :return:
    """
    _src_path = src_path
    _dest_path = dest_path
    _files_extensions = files_extensions
    _filename_suffix = filename_suffix

    # check if destination path is existing create if not
    if not os.path.exists(_dest_path):
        os.makedirs(_dest_path)
        print("Destination path created: {}".format(_dest_path))

    if len(os.listdir(_src_path)) <= 0:
        print("No files in path: {}".format(_src_path))
        return 0, 0, 0
    else:
        num_files_processed = 0
        num_files_removed = 0
        num_files_copied = 0
        num_files_skipped = 0

        for file in os.listdir(_src_path):

            abs_file_path = "{}/{}".format(_src_path, file)

            if os.path.isdir(abs_file_path):
                print("Found a directory {} ...searching in it for new files.".format(abs_file_path))
                _num_files_processed, _num_files_removed, _num_files_copied, _num_files_skipped = organize_files(
                    abs_file_path, _dest_path, _files_extensions, _filename_suffix)

                num_files_processed += _num_files_processed
                num_files_removed += _num_files_removed
                num_files_copied += _num_files_copied
                num_files_skipped += _num_files_skipped

            elif os.path.isfile(abs_file_path) and file.lower().endswith(_files_extensions):

                num_files_processed += 1

                filename = _src_path + os.sep + file
                file_ext = get_file_ext(filename)
                date_info = get_create_date(filename)
                if not date_info:
                    print("Skipped No Creation Date metadata for file: {}".format(abs_file_path))
                    continue
                try:
                    out_filepath = _dest_path + os.sep + date_info[2] + os.sep + date_info[1]
                    if RENAME_SORTED_FILES:
                        if APPEND_ORIG_FILENAME:
                            out_filename = out_filepath + os.sep + _filename_suffix + date_info[3] \
                                           + get_sub_sec_time_original(filename) + '_' + file
                        else:
                            out_filename = out_filepath + os.sep + _filename_suffix + date_info[3] \
                                           + get_sub_sec_time_original(filename) + file_ext
                    else:
                        if APPEND_ORIG_FILENAME:
                            out_filename = out_filepath + os.sep + get_file_name(filename) + '_' + file
                        else:
                            out_filename = out_filepath + os.sep + get_file_name(filename)

                    # check if destination path is existing create if not
                    if not os.path.exists(out_filepath):
                        os.makedirs(out_filepath)

                    # don't overwrite files if the name is the same
                    if os.path.exists(out_filename):
                        shutil.copy2(filename, out_filename + '_duplicate')
                        if filecmp.cmp(filename, out_filename + '_duplicate', shallow=False):
                            # the old file name exists...skip file
                            os.remove(out_filename + '_duplicate')
                            num_files_skipped += 1
                            print("Skipped file: {}".format(filename))
                            continue
                        else:
                            # new dest path but old filename, file duplicate i the destination
                            out_filename = out_filepath + os.sep + file

                            if os.path.exists(out_filename):
                                shutil.copy2(filename, out_filename + '_duplicate')
                                if filecmp.cmp(filename, out_filename + '_duplicate', shallow=False):
                                    # the old file name exists...skip file
                                    os.remove(out_filename + '_duplicate')
                                    num_files_skipped += 1
                                    print("Skipped file: {}".format(filename))
                                    continue

                    # copy the file to the organised structure
                    shutil.copy2(filename, out_filename)
                    if filecmp.cmp(filename, out_filename, shallow=False):
                        num_files_copied += 1
                        print('File copied with success to {}'.format(out_filename))
                        if REMOVE_OLD_FILES:
                            os.remove(filename)
                            num_files_removed += 1
                            print('Removed old file {}'.format(filename))
                    else:
                        print('File failed to copy :( {}'.format(filename))

                except Exception as e:
                    print("{}".format(e))
                    print("Exception occurred")
                    return num_files_processed, num_files_removed, num_files_copied, num_files_skipped
                except None:
                    print('File has no metadata skipped {}'.format(filename))

    return num_files_processed, num_files_removed, num_files_copied, num_files_skipped


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


def main():
    # check if exiftool is installed
    if not which("exiftool"):
        print("Please...install exiftool first")
        return

    print("======== {} =======".format(datetime.datetime.now()))
    if PROCESS_IMAGES:
        print("Start process images...")
        start_time = timeit.default_timer()
        processed, removed, copied, skipped = organize_files(IMAGES_SOURCE_PATH, IMAGES_DESTINATION_PATH,
                                                             IMAGE_FILES_EXTENSIONS, IMAGE_FILENAME_SUFFIX)
        elapsed = timeit.default_timer() - start_time
        print("End process images in: {} seconds.".format(elapsed))
        print("Proccessed: {}. Removed: {}. Copied: {}. Skipped: {}".format(processed,
                                                                            removed, copied, skipped))
    if PROCESS_VIDEOS:
        print("Start process videos...")
        start_time = timeit.default_timer()
        processed, removed, copied, skipped = organize_files(VIDEOS_SOURCE_PATH, VIDEOS_DESTINATION_PATH,
                                                             VIDEO_FILES_EXTENSIONS, VIDEO_FILENAME_SUFFIX)
        elapsed = timeit.default_timer() - start_time
        print("End process videos in: {} seconds.".format(elapsed))
        print("Proccessed: {}. Removed: {}. Copied: {}. Skipped: {}".format(processed,
                                                                            removed, copied, skipped))

    return


# Execution
main()
nextcloud_files_scan()
