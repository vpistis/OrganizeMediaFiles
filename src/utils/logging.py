import logging
import os
from datetime import date, datetime
from pathlib import WindowsPath

"""
Internal Module Logger
"""
from src.utils.generic import get_setting

BASEPATH = os.path.dirname(__file__)
print("BASEPATH: {}".format(BASEPATH))
LOG_DIR = os.path.join(os.path.dirname(BASEPATH), "logs", date.today().strftime("%Y-%m-%d"))
POSIX = 'posix'
# LOG_LEVEL_INFO = logging.INFO
# LOG_LEVEL_DEBUG = logging.DEBUG
LOGGER_DATEFORMAT = "%Y:%m:%d %H:%M:%S"
try:
    LOG_LEVEL = get_setting("LOG_LEVEL")
except:
    LOG_LEVEL = "DEBUG"


class MainLogger(object):
    """
    holds the logger reference
    """
    logger = None
    file = None


def check_dir_exists(dir_path, raise_exception=False):
    """
    Checks if a directory exists; otherwise it tries to create the directory
    :param dir_path:
    :param raise_exception:
    :return:
    """
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("dir {} CREATED!".format(dir_path))
        else:
            print("Dir  {} EXISTS!".format(dir_path))
    except Exception as e:
        print("dir not created: {}".format(dir_path))
        print("Exception: {}".format(e))
        if raise_exception:
            raise e


def get_logger_file(log_name):
    check_dir_exists(LOG_DIR)
    get_logger(log_name)
    return MainLogger.file


def get_logger(log_name):
    """
    Return logger reference
    :return:
    """
    try:
        check_dir_exists(LOG_DIR)
        print("Logging logger: {}".format(logging.getLogger(log_name)))
        # if logging.getLogger(log_name) is None:
        if MainLogger.logger is None or MainLogger.logger != logging.getLogger(log_name):
            print("Regenerate Logger")
            logger = logging.getLogger(log_name)
            logger.setLevel(LOG_LEVEL)

            if os.name == POSIX:
                print("LOG_DIR: {}".format(LOG_DIR))
                log_file = "{}/{}_{}.log".format(LOG_DIR, log_name,
                                                 datetime.now()).replace(" ", "_").replace(":", "")
                print("LOG FILE: {}".format(log_file))
                log_file_path = log_file
            else:
                print("LOG_DIR: {}".format(LOG_DIR))
                log_file = "{}_{}.log".format(log_name,
                                              datetime.now()).replace(" ", "_").replace(":", "")
                print("LOG FILE: {}".format(log_file))
                log_file_path = WindowsPath(os.path.join(LOG_DIR, log_file))

            file = logging.FileHandler(log_file_path)
            file.setLevel(LOG_LEVEL)
            fileformat = logging.Formatter(
                "%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s",
                datefmt=LOGGER_DATEFORMAT)
            file.setFormatter(fileformat)
            logger.addHandler(file)
            MainLogger.logger = logger
            MainLogger.file = log_file
        print("Main logger: {}".format(MainLogger.logger))
        return MainLogger.logger
    except Exception as e:
        print("Exception occurred: {}".format(e))
        return None
