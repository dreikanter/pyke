import inspect
from pyke import const


class PykeTask():
    """Pykefile task."""

    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.args = self._args(func)
        self.help = func.__doc__

    def __str__(self):
        pattern = "{%s name: %s; help: %s}"
        name = self.__class__.__name__
        return pattern % (name, self.name, self.help)

    def call(self, args):
        """Call the task function."""
        self.func(**args)

    def _args(self, func):
        """Get annotated task parameters."""
        args = []
        error_format = "%s (function: %s; argument: %s)"
        argerror = lambda msg: error_format % (msg, func.__name__, name)

        for name in inspect.signature(func).parameters:
            shortname = None
            argtype = str
            help = None

            if name in func.__annotations__:
                annotation = func.__annotations__[name]
                if type(annotation) == type:  # got argument type constraint
                    argtype = annotation
                elif type(annotation) == str:  # got argument description
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
