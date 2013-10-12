import imp
import inspect
import os.path
from pyke import const
from pyke.task import PykeTask


class PykeFile():
    """Pykefile representation."""

    def __init__(self, dir_path):
        """Search for pyke file in the specified directory and load it."""
        file_name = dir_path
        if not os.path.isfile(dir_path):
            for valid_name in const.PYKEFILE:
                file_name = os.path.join(dir_path, valid_name)
                if os.path.exists(file_name):
                    break
            else:
                file_name = None

        self._load(file_name)

    def __str__(self):
        pattern = "{%s filename: %s; tasks: [%s]}"
        name = self.__class__.__name__
        return pattern % (name, self._fullname, self.tasks().keys())

    def _load(self, file_name):
        """Load pykefile tasks."""
        self._fullname = os.path.abspath(file_name) if file_name else None
        self._tasks = {}  # task functions
        self.metadata = []  # task information
        if not self._fullname:
            return

        pykemod = imp.load_source(const.PYKEMOD, self._fullname)
        is_task = lambda func: inspect.isfunction(func) and \
            func.__module__ == const.PYKEMOD and \
            not func.__name__.startswith(const.UNDERSCORE)

        for member in inspect.getmembers(pykemod):
            name, func = member
            if is_task(func):
                self._tasks[name] = PykeTask(name, func)

        self.description = pykemod.__doc__

    def loaded(self):
        """Return True if pykefile was found and loaded."""
        return bool(self._fullname)

    def file_name(self):
        """Return absolute path to the pykefile or None if not loaded."""
        return self._fullname

    def tasks(self):
        """Return tasks dict or {} if pykefile was not loaded."""
        return self._tasks if self.loaded() else {}

    def execute(self, task, args):
        """Run a pyke task."""
        excludes = ['task', 'quiet', 'verbose', 'dryrun', 'help', 'file']
        task_args = {k: args[k] for k in args if k not in excludes}
        self._tasks[task].call(task_args)
