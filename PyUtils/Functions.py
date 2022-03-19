import os


def text(val: str):
    """Scape quetation marquer, to allow simple cotation marker."""
    return val.replace('"', '\"')

def is_non_zero_file(fpath: str):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

