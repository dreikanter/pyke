# coding: utf-8

"""Pyke — Python build tool."""

import os
import sys
from pprint import pprint
from pyke import const
from pyke.file import PykeFile
from pyke.parser import PykeParser
from pyke.task import PykeTask


def main():
    pykefile = PykeFile(os.getcwd())
    parser = pykefile.parser()
    task, args = parser.parse_args(sys.argv[1:])

    if pykefile.loaded():
        pykefile.execute(task, args)
    else:
        names = ', '.join(const.PYKEFILE)
        print("No Pykefile found (looking for: %s). Use -h for help." % names)
