# coding: utf-8

import imp
import inspect
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


def _good_dog(func):
    """determines if specified pykefile function supposed to be a command"""
    return inspect.isfunction(func) and \
           func.__module__ == const.PYKEMOD and \
           not func.__name__.startswith(const.UNDERSCORE)


def get_commands(pykefile):
    """gets pyke commands collection from the specified pykefile"""
    pykemod = imp.load_source(const.PYKEMOD, pykefile)
    commands = {}

    for member in inspect.getmembers(pykemod):
        name, func = member
        if _good_dog(func):
            commands[name] = {
                    'func': func,
                    'doc': __doc__,
                    'defaults': func.__defaults__,
                    'annotations': func.__annotations__,
                }

    return commands
