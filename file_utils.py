#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: Alexander Bikadorov

Some functions not tested with Python 3
"""

import logging
import os
import re
import shutil
import glob
import fnmatch


def split_path(path):
    """Return a list of componenents of string 'path'"""
    folders = []
    while True:
        path, folder = os.path.split(path)
        if not folder:
            if path:
                folders.append(path)
            break
        folders.append(folder)

    folders.reverse()
    return folders


def _rename(file_path_str):
    dir_name, fname = os.path.split(file_path_str)
    bname, ext = os.path.splitext(fname)
    bname_pre = re.split('_[0-9]+$', bname)[0]
    num_files = len(files_in_dir(dir_name, bname_pre + '_[0-9]+' + ext))
    while True:
        file_path_str = os.path.join(dir_name, bname_pre + '_' + str(num_files) + ext)
        if not os.path.exists(file_path_str):
            break
        num_files += 1
    return file_path_str


def move(src_str, dest_str, rename=False, into_folder=True):
    """Move an existing file or directory from 'src_str' to 'dest_str'.
       If 'rename' is true and the destination exists already the target will be renamed.
       'into_folder' is used for that to determine if source should be moved into a destination
       directory or source should be renamed instead.
    """
    if not os.path.exists(src_str):
        logging.warning('does not exist (can not move): ' + src_str)
        return False
    if not os.path.isdir(os.path.dirname(dest_str)):
        logging.warning('does not exist (can not move): ' + os.path.dirname(dest_str))
        return False
    if into_folder and os.path.isdir(dest_str):
        if os.path.samefile(src_str, dest_str):
            logging.warning('can not move directory into itself: ' + src_str)
            return False
        dest_str = os.path.join(dest_str, os.path.basename(src_str))
    if os.path.exists(dest_str):
        if rename:
            logging.info('does already exist (renaming): ' + dest_str)
            dest_str = _rename(dest_str)
        else:
            logging.warning('does already exist (not moving):' + dest_str)
            return False
    logging.info('moving ' + src_str + ' to ' + dest_str)
    shutil.move(src_str, dest_str)
    return True


def write_file(file_path_str, str_, append=False, rename=True, verbose=True):
    """Write string to file.
       If 'append' is false an existing file will not be overwritten. Instead the existing file
       will be renamed. If 'append' is true the string is appended to file if it already exists,
       the file is created otherwise.
       Returns the file path the file was written to.
    """
    dir_name, fname = os.path.split(file_path_str)
    if not append and os.path.exists(file_path_str):
        if rename:
            logging.info('file already exists (renaming): ' + file_path_str)
            file_path_str = _rename(file_path_str)
        else:
            logging.warning('file already exists (not overwriting): ' + file_path_str)
            return None
    if dir_name and not os.path.isdir(dir_name):
        logging.warning('directory does not exist (can not create file)): ' + file_path_str)
        return None
    mode = 'a' if append else 'w'
    with open(file_path_str, mode) as f:
        f.write(str_)
    if verbose:
        logging.info("wrote " + str(len(str_)) + " bytes to file: " + file_path_str)
    return file_path_str


def read_file(file_path):
    """Read content of file.
       Return content of file as string or 'None' if reading failed.
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except IOError:
        logging.warning('can not read file: ' + file_path)
        return None


def read(f):
    """Read content of file.
       Return content of file as string or 'None' if reading failed.
    """
    try:
        return f.read()
    except IOError:
        logging.warning('can not read from file: ' + f)
        return None


def read_file_lines(file_):
    """Read lines of file
       file_: either path to file or a file (like) object.
       Return list of lines read or 'None' if file does not exist.
    """
    cont_str = read_file(file_)
    if cont_str is None:
        return None
    return [url_str.rstrip() for url_str in cont_str.splitlines()]


def files_in_dir(dir_, regex='*.*'):
    """Return a list of all files in 'dir_' matching 'regex' with absolute path"""
    abs_path = os.path.abspath(dir_)
    if not os.path.isdir(abs_path):
        logging.warning('does not exist/is not a directory: ' + abs_path)
    return glob.glob(os.path.join(abs_path, regex))


def find_files(dir_, regex='*.*'):
    """Walk recursively through all dirs in 'dir_'.
       Yield all files in 'dir_' matching 'regex' with absolute path
    """
    abs_path = os.path.abspath(dir_)
    if not os.path.isdir(abs_path):
        logging.warning('does not exist/is not a directory: ' + abs_path)
    for root, dirnames, filenames in os.walk(abs_path):
        for filename in fnmatch.filter(filenames, regex):
            yield os.path.join(root, filename)


def create_dirs(dir_list):
    """Create all directories listed as path string in 'dir_list'."""
    for dir_ in dir_list:
        if not os.path.exists(dir_):
            logging.info('INIT: create directory: ' + dir_)
            os.makedirs(dir_)


# ############
# OLD STUFF...
# ############


def removeFile(file_str):
    if not os.path.exists(file_str):
        print('warning, file does not exists (can not remove): ' + file_str)
        return False
    os.remove(file_str)
    return True
