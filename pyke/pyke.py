# coding: utf-8

import os
import imp
import inspect
from functools import partial
import sys
from pprint import pprint
from . import tools
from . import const


# Argument reflection works this way:

# def annotated(a: int, b: str = 'hello', c = None):
#     pass

# pprint(annotated.__annotations__)

# args = inspect.getfullargspec(annotated)
# pprint(annotated.__defaults__)  # correspond to the last n elements listed in args



def main():
    file_name = tools.get_pykefile()
    if not file_name:
        exit("%s not found" % const.PYKEFILE)

    pykemod = imp.load_source('pykefile', file_name)
    commands = {}
    for member in inspect.getmembers(pykemod):
        name, func = member
        if inspect.isfunction(func) and not name.startswith(const.UNDERSCORE):
            commands[name] = func

    # Function execution:

    # f = partial(commands['start'], name=1)
    # f('a')
