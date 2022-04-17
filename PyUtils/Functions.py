import os
import math


def text(val: str):
    """Scape quetation marquer, to allow simple cotation marker."""
    return val.replace('"', '\"')


def is_non_zero_file(fpath: str):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def split_list(big_list, n):
    x = int(math.ceil(len(big_list) / n))
    list_of_lists = [big_list[i:i + x] for i in range(0, len(big_list), x)]
    return list_of_lists
