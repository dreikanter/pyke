_vars = {}


def env(key, value=None, default=None):
    if value is None:
        return _vars.get(key, default)
    else:
        _vars[key] = value


def setenv(args):
    for key, value in args.items():
        env(key, value)
