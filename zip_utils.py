#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: Alexander Bikadorov

Some functions not tested with Python 3
"""

import logging
import os
import zipfile
import datetime


def open_archive(arch_path_str, verbose=False):
    """Open an existing archive for reading.
       Return a ZipFile object.
    """
    if not os.path.exists(arch_path_str):
        if verbose:
            logging.warning('archive does not exist: ' + os.path.abspath(arch_path_str))
        return None
    try:
        # bug in python zip lib: can't open empty archive
        if os.path.getsize(arch_path_str) <= 22:
            return None
        return zipfile.ZipFile(arch_path_str, 'r')
    except IOError:
        logging.warning('could not open archive ' + os.path.abspath(arch_path_str))
        return None

def get_from_archive(archive, filename):
    """Read file from archive.
       archive: ZipFile object or path to zip archive.
       Return tuple (zipInfo, data) or (None, None) if something went wrong.
    """
    if type(archive) is str:
        if not os.path.exists(archive):
            return (None, None)
        archive = zipfile.ZipFile(archive, 'r')
    try:
        info_entry = archive.getinfo(filename)
    except (KeyError, AttributeError):  # not in archive, archive does not exist
        return (None, None)
    data_str = archive.read(filename)
    return (info_entry, data_str)


def add_to_archive(archive, file_str, file_is_path=True, name=None):
    """Add file or string to archive.
       archive: ZipFile or path to ZipFile. If archive does not exist it is created.
       file_str: path to file or string to be written to file.  If 'file_str' is not a path
       'file_is_path' must be set to "False".
       name: will be used to set the name of the file in archive. It can be a
       string or ZipInfo instance. If not specified and 'file_' is a string to be written a
       ValueError is raised.
    """
    if not file_is_path and name is None:
        raise ValueError('No filename given (can not add to archive)')
    if type(archive) is str:
        archive = zipfile.ZipFile(archive, 'a', zipfile.ZIP_DEFLATED)
    if type(name) is zipfile.ZipInfo:
        arch_filename_str = name.filename
    elif type(name) is str:
        arch_filename_str = name
    else:
        arch_filename_str = os.path.basename(file_str)
    # writing a file that already exists does NOT OVERWRITE!
    # the file is archived two times and on file overwrites the other when extracting
    if arch_filename_str in archive.namelist():
        logging.warning('file already in archive (skipping): ' + arch_filename_str)
        return False
    if file_is_path:
        archive.write(file_str, arcname=arch_filename_str)
    else:
        archive.writestr(name, file_str)
    return True


def datetime_from_zipinfo(z_info):
    """Return date/time string from a zipinfo file object."""
    #(year, month, day, h, m, s) = z_info.date_time if z_info else (2000, 1, 1, 0, 0, 0)
    #date_time = datetime.datetime(year, month, day, h, m, s)
    return datetime.datetime(*(z_info.date_time)).strftime('%Y-%m-%d %H:%M:%S')
