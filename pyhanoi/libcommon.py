""" LibCommon - Library of common generic functions """

from __future__ import annotations

from typing import Sequence, Any, List, Tuple

def pop_list(index_list: List[int], item_list: List[Any]):
    """ Pops multiple items from the given list """
    
    index_list.sort()
    index_list.reverse()

    for i in index_list:
        item_list.pop(i)


def get_matching_index(list_1: Sequence[Any], list_2: Sequence[Any]):
    """Gets index of item in list matching the args
    i: matching index of list_1
    j: matching index from list_2
    """

    result: List[Tuple[int, int]] = []

    for i, term_1 in enumerate(list_1):
        for j, term_2 in enumerate(list_2):
            if term_1 == term_2:
                result.append((i, j))

    return result
