# coding: utf-8

import os.path
from pyke import const


class PykeFile():
    """Pykefile representation."""

    def __init__(self, dir_path):
        """Search for pyke file in the specified and load it."""

        for valid_name in const.PYKEFILE:
            self._fullname = os.path.join(dir_path, valid_name)
            if os.path.exists(self._fullname):
                self._load()
                break
        else:
            self._fullname = None


    def _load(self):
        """Loads pykefile tasks."""

        pykemod = imp.load_source(const.PYKEMOD, self._fullname)

        self.tasks = {}  # task functions
        self.metadata = []  # task information

        is_task = lambda func: inspect.isfunction(func) and \
                               func.__module__ == const.PYKEMOD and \
                               not func.__name__.startswith(const.UNDERSCORE)

        for member in inspect.getmembers(pykemod):
            name, func = member
            if is_task(func):
                self.tasks[name] = PykeTask(name, func)

        self.description = pykemod.__doc__


    def loaded(self):
        """Returns True if pykefile was found and loaded."""

        return self._fullname != None


    def parser(self):
        """Create PykeParser populated with pykefile commands."""

        parser = PykeParser()

        if self.loaded():
            for name, task in self.tasks.items():
                parser.add_task(name, args=task.args, help=task.help)

        return parser


    def execute(self, task, args):
        """Run a pyke task."""

        self.tasks[task].call(args)
