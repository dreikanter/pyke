# coding: utf-8

import argparse
import sys
from pyke import const
from pyke import version


class PykeParser(argparse.ArgumentParser):
    """Customized ArgumentParser for pykefile-configurable command lines."""

    # Repeating base constructor signature is important to make subparsers work
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True):

        super(PykeParser, self).__init__(prog=const.CMD,
                                         description=const.DESCRIPTION,
                                         epilog=const.EPILOG)

        self.add_argument('-v', '--version',
                          action='version',
                          version=version.get_version())

        self._subs = None


    def add_task(self, name, args, help):
        """Add new subparser for a pyke task."""
        if self._subs == None:
            self._subs = super(PykeParser, self).add_subparsers(dest='task')
        sp = self._subs.add_parser(name, help=help)
        for arg in args:
            sp.add_argument(*_arg_names(arg), **_arg_opts(arg))


    def parse_args(self, args=None, namespace=None):
        """Same as base method but returns a tuple of two elements instean
        of Namespace: a parsed task name, and a dict of task arguments."""
        result = super(PykeParser, self).parse_args(args, namespace)
        if hasattr(result, 'task'):
            task = result.task
            del(result.task)
            return task, vars(result)
        else:
            return None, {}


    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        sys.exit(2)


def _arg_names(arg):
    """get argument name(s) from metadata for add_argument()"""
    result = []

    if arg['default'] != None:
        if arg['shortname']:
            result.append("-%s" % arg['shortname'])
        result.append("--%s" % arg['name'])
    else:
        result.append("%s" % arg['name'])

    return result


def _arg_opts(arg):
    """generate add_argument() parameters from arg metadata"""
    opts = { 'help': arg['help'] }

    if arg['type'] == bool:
        opts.update({ 'action': 'store_true' })
    else:
        opts.update({ 'default': arg['default'], 'type': arg['type'] })

    return opts
