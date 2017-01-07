# -*- coding: utf-8 -*-

"""
Created on 30/12/16 21:42

@author: vpistis
"""
import json
import os

import sys


def get_setting(key):
    """Get the secret variable or return explicit exception."""

    base_dir = str(os.path.dirname(__file__))

    with open(base_dir + "/config.json") as f:
        config_json = json.loads(f.read())

    try:
        return config_json[key]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(key)
        raise Exception(error_msg)


def which(program):
    """
    Check if a program/executable exists

    :param program:
    :return:
    """

    def is_exe(f_path):
        return os.path.isfile(f_path) and os.access(f_path, os.X_OK)

    fpath, fname = os.path.split(program)

    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


class Logger(object):
    """
    http://stackoverflow.com/a/14906787/5941790
    """

    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(get_setting("LOG_FILE"), "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass
