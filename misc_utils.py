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
import itertools
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


def split(iterable, delimiter):
    """Yield elements in 'iterable' grouped in lists divided by the elements equal to 'delimiter'
       (without the delimiter elements itself). Empty groups are ommited.
    """
    for k, g in itertools.groupby(iterable, lambda x: x == delimiter):
        if not k:
            yield list(g)


def filter_duplicates(some_list, comp_item_index=None, verbose=False):
    """Remove duplicate items in list, preserves order.
       If 'comp_item' is given, 'some_list' is treated as list of sequences, the duplicates
       will be found by comparing the items at 'comp_item_index' position in the sequences.
    """
    seen_set = set()
    seen_add = seen_set.add
    filter_list = []
    for element in some_list:
        compare_element = element if comp_item_index is None else element[comp_item_index]
        if compare_element not in seen_set:
            filter_list.append(element)
            seen_add(compare_element)
        elif verbose:
            logging.warning('duplicate item: '+str(element))
    diff_len = len(some_list) - len(filter_list)
    if diff_len:
        logging.debug('removed ' + str(diff_len) + ' duplicates')
    return filter_list


def flatten(list_):
    """Return flat list with all nested items in 'list_' (recursive)."""
    def flat_rec(l):
        for e in l:
            if isinstance(e, list):
                for se in flat_rec(e):
                    yield se
            else:
                yield e

    return list(flat_rec(list_))


def window(seq, n=2):
    """Returns a sliding window of width n over data from the iterable.
       Source: https://docs.python.org/release/2.3.5/lib/itertools-example.html
    """
    it = iter(seq)
    result = tuple(itertools.islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def join_if(seq, condition, delimiter=''):
    """Return an iterator with elements in 'seq'. Element that are 'condition' are
    joined with its predecessor using 'delimiter'.
    """
    if not seq:
        return seq

    rev = reversed(tuple(window(seq)))
    g = (delimiter.join((a, b)) if b == condition else a for a, b in rev if a != condition)
    return itertools.chain(reversed(tuple(g)), [seq[-1]])


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
