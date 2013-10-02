# coding: utf-8

"""Pyke — Python build tool."""

from argparse import ArgumentParser
import os
import sys
from pyke import const
from pyke.env import setenv
from pyke.file import PykeFile
from pyke.parsers import CoarseParser, PykeParser


def main():
    argv = sys.argv[1:]

    basic_args = CoarseParser().parse_args(argv)
    pykefile = PykeFile(basic_args.file)
    parser = PykeParser(tasks=pykefile.tasks())
    args = vars(parser.parse_args(argv))

    if pykefile.loaded():
        print(args)
        if not basic_args.task:
            print('Pykefile task not specified.\n')
            parser.print_help()
            exit()

        setenv(args)
        pykefile.execute(basic_args.task, args)
    else:
        names = ', '.join(const.PYKEFILE)
        exit("No Pykefile found (looking for: %s).\nUse -h for help." % names)
