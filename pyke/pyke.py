# coding: utf-8

"""main module"""

import argparse
import os
import sys
from pprint import pprint
from . import const
from . import helpers
from . import version


def parse(metadata, args, description=None):
    """maps task line arguments to pyke task parameters"""
    parser = argparse.ArgumentParser(prog='pyke',
                                     description=description,
                                     epilog=const.EPILOG)

    subparsers = parser.add_subparsers(dest='task')

    ver = version.get_version()
    parser.add_argument('-v', '--version', action='version', version=ver)

    for task in metadata:
        sp = subparsers.add_parser(task['name'], help=task['help'])
        for arg in task['args']:
            sp.add_argument(*helpers.arg_names(arg), **helpers.arg_opts(arg))

    args = parser.parse_args(args)
    task = args.task
    del(args.task)

    return task, vars(args)


def main():
    pykefile = helpers.get_pykefile(os.getcwd())
    if not pykefile:
        exit('pykefile not found')
    tasks, metadata, description = helpers.load_pykefile(pykefile)
    # print(sys.argv[1:])
    # exit()
    name, args = parse(metadata, sys.argv[1:], description)
    tasks[name](**args)
