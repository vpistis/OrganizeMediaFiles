#OrganizeMediaFiles Alpha

This project is a collection of Python scripts that help to organize media
files into a directory tree "year/month" based on file metadata, using [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/)

Used by me into my personal [Nextcloud](https://www.nextcloud.com) installation to organize unsorted files.
Strongly inspired by: https://github.com/OneLogicalMyth/Random-Scripts/blob/master/NextCloud/SortPictures.py

**Tested only with Linux/Debian python 2.7.9 and MacOS python 2.7.13**

**ATTENTION alpha version backup your files before use!**

This picture describe the final result:
![final result](final_result.png)

## Features
+ manages duplicate files due to milliseconds difference (the new file uses the same old name).
+ support all file types supported by [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/)
+ proccess video and photo at same time (see `config.json`)

## Getting OrganizeMediaFiles:
Clone the repository: `git clone https://github.com/vpistis/OrganizeMediaFiles.git`.
Alternatively download [tarball](https://github.com/vpistis/OrganizeMediaFiles/tarball/master) or [zip](https://github.com/vpistis/OrganizeMediaFiles/archive/master.zip). There haven't been any releases yet.

##Installation
No installation required, it's a simple python script :) It run in `python`.

##Requirements
Install [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/) commandline:
`sudo apt-get install exiftool`

##Usage
Open the script, adjust variables and run with python:
`python organize_media_files.py`

## Configuration
**Important**: process only photo/video/audio files with specified extensions
Use the `config.json` to change paths and other stuff.

# LICENSE
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
