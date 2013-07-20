# coding: utf-8

import argparse
import os
import inspect
from functools import partial
import sys
from pprint import pprint
from . import const
from . import helpers


def parse(metadata, args, description=None):
    """maps command line arguments to pyke command parameters"""
    parser = argparse.ArgumentParser(prog='pyke',
                                     description=description,
                                     epilog=const.EPILOG)

    subparsers = parser.add_subparsers()
    for command in metadata:
        subparser = subparsers.add_parser(command['name'], help=command['help'])
        for arg in command['args']:
            subparser.add_argument(*helpers.arg_names(arg),
                                   default=arg['default'],
                                   help=arg['help'])

    # let's try this
    parser.parse_args('cleanup --help'.split())

    args = {}
    name = 'dummy_command'

    return name, args


def main():
    pykefile = helpers.get_pykefile(os.getcwd())
    if not pykefile:
        exit('pykefile not found')
    commands, metadata, description = helpers.load_commands(pykefile)
    name, args = parse(metadata, sys.argv[1:], description)
    commands[name](**args)
