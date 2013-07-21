# coding: utf-8

import argparse
import os
import sys
from pprint import pprint
from . import const
from . import helpers
from . import version


def parse(metadata, args, description=None):
    """maps command line arguments to pyke command parameters"""
    parser = argparse.ArgumentParser(prog='pyke',
                                     description=description,
                                     epilog=const.EPILOG)

    subparsers = parser.add_subparsers(dest='command')

    ver = version.get_version()
    parser.add_argument('-v', '--version', action='version', version=ver)

    for command in metadata:
        sp = subparsers.add_parser(command['name'], help=command['help'])
        for arg in command['args']:
            sp.add_argument(*helpers.arg_names(arg), **helpers.arg_opts(arg))

    args = parser.parse_args(args)
    command = args.command
    del(args.command)

    return command, vars(args)


def main():
    pykefile = helpers.get_pykefile(os.getcwd())
    if not pykefile:
        exit('pykefile not found')
    commands, metadata, description = helpers.load_pykefile(pykefile)
    name, args = parse(metadata, sys.argv[1:], description)
    commands[name](**args)
