# -*- coding: utf-8 -*-

"""
Created on 27/12/16 15:31

@author: vpistis
"""

import exiftool

files = ["a.jpg", "b.png", "c.tif"]
with exiftool.ExifTool() as et:
    metadata = et.get_metadata_batch(files)
for d in metadata:
    print("{:20.20} {:20.20}".format(d["SourceFile"],
                                     d["EXIF:DateTimeOriginal"]))

# config no trailing slashes please
source_path = '/media/drivemount/user/files/PhotosToSort'
destin_path = '/media/drivemount/user/files/Photos'

# Il false copy file and dont' remove old
remove_old_files = False

# various configurations
append_original_filename = False
pre_filename = 'IMG_'
