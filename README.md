#OrganizeMediaFiles Alpha

This project is a collection of Python scripts that help to organize media
files into a directory tree "year/month" based on file metadata, using [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/)

Used by me into my personal [Nextcloud](https://www.nextcloud.com) installation to organize unsorted files.
Strongly inspired by: https://github.com/OneLogicalMyth/Random-Scripts/blob/master/NextCloud/SortPictures.py

**Tested only with Linux python3**

![final result](final_result.png)

## Features
+ Check duplicate files due to milliseconds difference (the new file uses the same old name).
+ support all file types supported by [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/)

# ATTENTION alpha version
**Allways backup all your files before use!**

## Getting OrganizeMediaFiles:
Clone the repository: `git clone https://github.com/vpistis/OrganizeMediaFiles.git`.
Alternatively download [tarball](https://github.com/vpistis/OrganizeMediaFiles/tarball/master) or [zip](https://github.com/vpistis/OrganizeMediaFiles/archive/master.zip). There haven't been any releases yet.

##Installation:
No installation required, it's a simple python script :) It run in `python`.

##Requirements
Install [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/) commandline:
`sudo apt-get install exiftool`

##Usage:
Open the script, adjust variables and run with python:
`python organize_media_files.py`

## Configuration
**Important**: process only photo/video/audio files with specified extensions
```
# config no trailing slashes please
SOURCE_PATH = "/media/drivemount/user/files/FilesToSort"
DESTINATION_PATH = "/media/drivemount/user/files/FilesSorted"

# If false copy file and don't remove old file
REMOVE_OLD_FILES = False

APPEND_ORIG_FILENAME = False
# process only files with this extensions
FILES_EXTENSIONS = tuple(".mp4", ".3gp")
# FILES_EXTENSIONS = tuple(".jpg", ".gif", ".tiff")
FILENAME_SUFFIX = "VID_"
DATE_FORMAT_OUTPUT = "%Y%m%d_%H%M%S"

# in case you use nextcloud or owncloud, set NEXTCLOUD=True to rescan all files
NEXTCLOUD = True
NEXTCLOUD_PATH = "/var/www/html/nextcloud"
NEXTCLOUD_USER = "www-data"

```

# LICENSE:
MIT License

Copyright (c) 2016 Valentino Pistis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
