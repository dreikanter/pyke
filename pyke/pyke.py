# coding: utf-8

"""Pyke — Python build tool."""

from argparse import ArgumentParser
import os
import sys
from pyke import const
from pyke.env import setenv
from pyke.file import PykeFile
from pyke.help import help
from pyke.parsers import CoarseParser, PykeParser


def main():
    argv = sys.argv[1:]

    basic_args = CoarseParser().parse_args(argv)
    pykefile = PykeFile(basic_args.file)

    if basic_args.help:
        help(pykefile, basic_args.task)
        exit()

    args = vars(PykeParser(tasks=pykefile.tasks()).parse_args(argv))

    if pykefile.loaded():
        setenv(args)
        pykefile.execute(basic_args.task, args)
    else:
        names = ', '.join(const.PYKEFILE)
        exit("No Pykefile found (looking for: %s).\nUse -h for help." % names)
