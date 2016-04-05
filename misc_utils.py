

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
import fractions
import string


def md5sum(str_):
    """Return the md5 hash of a string in hex."""
    sanitized_str = ''.join([c for c in str_ if ord(c) < 128])
    md5sum_str = hashlib.md5(sanitized_str).hexdigest()
    return md5sum_str


def group_it(l, n):
    """Yield successive 'n'-sized chunks from sequence 'l'.
       The last chunk contains len('l') modulo 'n' elements.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


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


def remove_dups(some_list, comp_item_index=None):
    """Remove duplicate items in list, preserves order.
       If 'comp_item' is given 'some_list' is treated as list of sequences, the duplicates
       will be found by comparing the items at 'comp_item_index' position in the sequences.
    """
    seen = set()
    seen_add = seen.add
    if comp_item_index is None:
        filt_list = [x for x in some_list
                     if x not in seen and not seen_add(x)]
    else:
        filt_list = [t for t in some_list
                     if t[comp_item_index] not in seen and not seen_add(t[comp_item_index])]
    logging.debug('removed ' + str(len(some_list) - len(filt_list)) + ' duplicates')
    return filt_list


def flatten(list_):
    """ Return flat list with all nested items in 'list_' (recursive)."""
    def flat_rec(l):
        for e in l:
            if isinstance(e, list):
                for se in flat_rec(e):
                    yield se
            else:
                yield e

    return list(flat_rec(list_))


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
    mul = lambda x, y: x * y
    return int(reduce(mul, (fractions.Fraction(n - i, i + 1) for i in range(k)), 1))


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
