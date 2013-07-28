# coding: utf-8

"""helper functions"""

import imp
import inspect
import os
from pprint import pprint
from . import const


def get_pykefile(dir_path):
    """search for pyke file in the current directory and return its
    name with absolute path or None if not found"""
    for valid_name in const.PYKEFILE:
        file_name = os.path.join(dir_path, valid_name)
        if os.path.exists(file_name):
            return file_name
    else:
        return None


def load_pykefile(pykefile):
    """gets pykefile tasks as callable object and tasks metadata"""
    pykemod = imp.load_source(const.PYKEMOD, pykefile)

    tasks = {}
    metadata = []

    # determine if specified pykefile function supposed to be a task
    good_dog = lambda func: inspect.isfunction(func) and \
                            func.__module__ == const.PYKEMOD and \
                            not func.__name__.startswith(const.UNDERSCORE)

    for member in inspect.getmembers(pykemod):
        name, func = member
        if good_dog(func):
            tasks[name] = func
            metadata.append(_metadata(name, func))

    description = pykemod.__doc__

    return tasks, metadata, description


def _metadata(name, func):
    """gets pyke task metadata from callable object"""
    return {
            'name': name,
            'args': _args(func),
            'help': func.__doc__,
        }


def _args(func):
    """get annotated task parameters"""
    args = []
    error_format = "%s (function: %s; argument: %s)"
    argerror = lambda msg: error_format % (msg, func.__name__, name)

    for name in inspect.signature(func).parameters:
        shortname = None
        argtype = str
        help = None

        if name in func.__annotations__:
            annotation = func.__annotations__[name]
            if type(annotation) == type:  # we have argument type constraint
                argtype = annotation
            elif type(annotation) == str:  # we have argument description
                help = annotation
            elif type(annotation) in [tuple, list]:
                if len(annotation) > 2:  # got full definition
                    argtype, shortname, help = annotation[0:3]
                elif len(annotation) > 1:  # got type and help
                    argtype, help = annotation[0:2]
                elif len(annotation) > 0:
                    if type(annotation[0]) in type:  # got type constraint
                        argtype = annotation[0]
                    elif type(annotation[0]) == str:  # got help
                        help = annotation[0]
                else:
                    raise Exception(argerror('empty annotation'))
            else:
                raise Exception(argerror('illegal annotation object type'))
        if argtype not in const.LEGAL_TYPES:
            raise Exception(argerror('illegal argument type constraint'))

        args.append({
                'name': name,
                'shortname': shortname,
                'type': argtype,
                'default': None,
                'help': help,
            })

    if func.__defaults__:
        start = len(args) - len(func.__defaults__)
        for num, value in enumerate(func.__defaults__, start=start):
            args[num]['default'] = value or ''

    return args


def arg_names(arg):
    """get argument name(s) from metadata for ArgumentParser.add_argument()"""
    result = []

    if arg['default'] != None:
        if arg['shortname']:
            result.append("-%s" % arg['shortname'])
        result.append("--%s" % arg['name'])
    else:
        result.append("%s" % arg['name'])

    return result


def arg_opts(arg):
    """generate add_argument() parameters from arg metadata"""
    opts = { 'help': arg['help'] }

    if arg['type'] == bool:
        opts.update({ 'action': 'store_true' })
    else:
        opts.update({ 'default': arg['default'], 'type': arg['type'] })

    return opts
