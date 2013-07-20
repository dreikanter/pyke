# coding: utf-8

import os
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
        exit('Pykefile not found')

    commands = tools.get_commands(file_name)

    # Function execution:

    f = partial(commands['md5']['func'])
    f(value='hello')
