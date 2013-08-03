# coding: utf-8

import argparse
import os
import sys
from pyke import const
from pyke import version


class CoarseParser(argparse.ArgumentParser):
    """Arguments parser fot initial extraction of the basic parameters."""

    # Repeating base constructor signature is important to make subparsers work
    def __init__(self,
                 prog=const.CMD,
                 usage=None,
                 description=const.DESCRIPTION,
                 epilog=const.EPILOG,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=False,
                 tasks=None):

        superme = super(CoarseParser, self)
        superme.__init__(prog=prog,
                         usage=None,
                         description=description,
                         epilog=epilog,
                         parents=parents,
                         formatter_class=formatter_class,
                         prefix_chars=prefix_chars,
                         fromfile_prefix_chars=fromfile_prefix_chars,
                         argument_default=argument_default,
                         conflict_handler=conflict_handler,
                         add_help=False)

        self.add_args()

    def add_args(self):
        """Adds basic pyke arguments to the parent parser."""

        self.add_argument('task',
                          nargs='?',
                          default=None)

        self.add_argument('-f', '--file',
                          dest='file',
                          default=os.getcwd(),
                          metavar='PATH',
                          help='use explicirly specified pykefile')

        self.add_argument('-h', '--help',
                          dest='help',
                          action='store_true',
                          help='show help')


    def parse_args(self, args):
        return self.parse_known_args(args)[0]


class PykeParser(argparse.ArgumentParser):
    """Arguments parser for pykefile-configurable command line."""

    # Repeating base constructor signature is important to make subparsers work
    def __init__(self,
                 prog=const.CMD,
                 usage=None,
                 description=const.DESCRIPTION,
                 epilog=const.EPILOG,
                 parents=[],
                 formatter_class=argparse.HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=False,
                 tasks=None):

        superme = super(PykeParser, self)
        superme.__init__(prog=prog,
                         usage=None,
                         description=description,
                         epilog=epilog,
                         parents=parents,
                         formatter_class=formatter_class,
                         prefix_chars=prefix_chars,
                         fromfile_prefix_chars=fromfile_prefix_chars,
                         argument_default=argument_default,
                         conflict_handler=conflict_handler,
                         add_help=False)

        self.add_args()
        self._sps = None

        if tasks:
            for name, task in tasks.items():
                self.add_task(task)

    def add_args(self):
        """Adds common arguments to the parent parser."""

        self.add_argument('-n', '--dry-run',
                          dest='dryrun',
                          action='store_true',
                          help='do a dry run')

        self.add_argument('-q', '--quiet',
                          dest='quiet',
                          action='store_true',
                          help='do not echo commands')

        self.add_argument('-f', '--file',
                          dest='file',
                          default=None,
                          metavar='PATH',
                          help='use explicirly specified pykefile')

        self.add_argument('-v', '--verbose',
                          dest='verbose',
                          action='store_true',
                          help='use verbose logging')

        self.add_argument('--version',
                          action='version',
                          version=version.get_version())

        self.add_argument('-h', '--help',
                          dest='help',
                          action='store_true',
                          help='show help')

    def add_task(self, task):
        """Add new subparser for a pyke task."""

        if self._sps == None:
            self._sps = self.add_subparsers(dest='task')

        sp = self._sps.add_parser(task.name, help=task.help)

        for arg in task.args:
            sp.add_argument(*_arg_names(arg), **_arg_opts(arg))

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
