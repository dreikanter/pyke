# coding: utf-8

import os
import imp
import inspect
from pprint import pprint
import sys

PYKEFILES = ['pykefile', 'Pykefile', 'pykefile.py', 'Pykefile.py']
UNDERSCORE = '_'


def get_pykefile():
    for file_name in PYKEFILES:
        file_name = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_name):
            return file_name
    return None


file_name = get_pykefile()
if not file_name:
    exit('pykefile not found')

pykemod = imp.load_source('pykefile', file_name)
usage = []
names = []
commands = {}

start = getattr(pykemod, 'start')
start()
exit()

for member in inspect.getmembers(pykemod):
    name, func = member
    if not hasattr(func, '__call__') or name.startswith(UNDERSCORE):
        continue
    usage.append("  {name} - {desc}".format(name=name, desc=func.__doc__))
    names.append(name)
    commands[name] = func

if len(sys.argv) < 2:
    print('usage')
    print("\n".join(usage))
elif sys.argv[1] in names:
    name = sys.argv[1]
    print("command: " + name)
    x = commands[name]
    x()
else:
    print('unknown command')
    exit(404)
