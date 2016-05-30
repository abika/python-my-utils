#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: Alexander Bikadorov

Some functions not tested with Python 3
"""

import logging
import itertools


def group_it(l, n):
    """Yield successive 'n'-sized chunks from sequence 'l'.
       The last chunk contains len('l') modulo 'n' elements.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


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
