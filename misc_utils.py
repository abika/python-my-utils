#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: Alexander Bikadorov

Some functions not tested with Python 3
"""

import logging
import hashlib
import random
import importlib
import os
import subprocess
import functools
import fractions
import string


def md5sum(str_):
    """Return the md5 hash of a string in hex."""
    sanitized_str = ''.join([c for c in str_ if ord(c) < 128])
    md5sum_str = hashlib.md5(sanitized_str).hexdigest()
    return md5sum_str


def load_object(path_str):
    """Load an object given its path as string"""
    mod_str, _, obj_str = path_str.partition('.')
    try:
        mod = importlib.import_module(mod_str)
    except ImportError as e:
        raise ImportError("Error loading module '%s': %s" % (path_str, e))
    try:
        obj = getattr(mod, obj_str)
    except AttributeError:
        raise NameError("Error loading object '%s' doesn't define any"
        " object named ""'%s'" % (obj_str, mod_str))
    return obj


def is_executable(exe_name_str):
    """Return true if executable 'exe_name_str' can be executed, else false."""
    devnull = open(os.devnull, 'w')
    try:
        popen = subprocess.Popen(exe_name_str, stdout=devnull, stderr=devnull)
    except OSError as e:
        logging.warning('"' + exe_name_str + '" is not executable, OSError was: ' + str(e))
        return False
    finally:
        devnull.close()
    popen.kill()
    return True


def nCk(n, k):
    """Return the binomial coefficient of n and k"""
    return int(functools.reduce(
            lambda x, y: x * y,
            (fractions.Fraction(n - i, i + 1) for i in range(k)),
            1))


def rand_str(n=6, chars=string.ascii_uppercase + string.digits):
    """Get a string of 'n' random characters choosen out of 'chars'"""
    return ''.join(random.choice(chars) for _ in range(n))


# ############
# OLD STUFF...
# ############


""" DEPRECATED
def group(iterable, size):
    sourceiter = iter(iterable)
    while True:
        batchiter = islice(sourceiter, size)
        yield chain([batchiter.next()], batchiter)
"""


def chunkIt(seq, num):
    """Return a list containing the elements in seq divided into num evenly sized chunks."""
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out
