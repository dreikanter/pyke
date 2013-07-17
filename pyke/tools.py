# coding: utf-8

import os
from . import const


def get_pykefile():
    """Search for pyke file in the current directory and return its
    name with absolute path or None if not found."""
    for valid_name in const.PYKEFILE:
        file_name = os.path.join(os.getcwd(), valid_name)
        if os.path.exists(file_name):
            return file_name
    else:
        return None
