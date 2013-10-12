# Pyke

Pyke is [rake](http://rake.rubyforge.org/)-inspired minimalistic [make](http://en.wikipedia.org/wiki/Make_(software) tool for Python.

The core benefit of Pyke over identical systems is the task files organization. There are no mandatory syntax constructions in addition to Python code to get an up-and-running command line interface. No decorators or specific docstrings required.

After `pyke` module is imported to a script, Pyke automagically translates function definitions to `argparse` parser configuration. Pyke is actively using [function annotations](http://www.python.org/dev/peps/pep-3107/) for additional capabilities like command line help and type validation. Also it plays well with default argument values and docstrings.

## Usage

Pyke is working identically to the majority of make tools. It allows to execute tasks defined within a specific file named `Pykefile`. Pykefiles are ordinary Python scripts. Each function from a pykefile is interpreted by Pyke as a separate task available to be executed from the command line.

Here is the basic syntax:

```
pyke <task> [options]
```

This command make Pyke to run a specified `<task>` with some optional arguments (`[otions]`) from a pykefile located in the current working directory. It is possible to execute pykefile tasks from arbitrary location using `-f` key, and there is always `--help` key available to get usage details for base `pyke` command arguments and pykefile-specific tasks.

Here is an example Pykefile with some basic tasks. Each function demonstrates one of Pyke features, from the most basic use case to advanced one.

``` python
"""example pykefile"""

from fnmatch import fnmatch
import math
import hashlib
import os
import re
import shutil
import sys


def ver():
    """show python version"""
    print(sys.version)


def md5(value: 'any text'):
    """calculate md5 hash for a string"""
    m = hashlib.md5()
    m.update(value.encode('utf-8'))
    print(m.hexdigest())


def sum(a: (int, 'first value'), b: (int, 'second value')):
    """sum two values and print the result"""
    print("%d + %d == %d" % (a, b, a + b))


def log(number: (float, 'number'),
        base: (float, 'b', 'logarithm base')=math.e):
    """prints logarithm of a [number] with respect to [base]"""
    print(math.log(number, base))


BLACKLIST = os.pathsep.join([
        '*.pyc',
        '__pycache__',
        '*.egg',
        '*.egg-info',
        'dist',
        'build',
        'sdist',
        'MANIFEST',
    ])

WHITELIST = os.pathsep.join([
        '.git',
    ])


def cleanup(path: (str, 'path'),
            blacklist: (str, 'b', 'files to delete')=BLACKLIST,
            whitelist: (str, 'w', 'files to NOT delete')=WHITELIST,
            dryrun: (bool, 'd', 'dry run')=False):
    """delete temporary files"""
    # check the destination directory path
    if not os.path.isdir(path):
        print('specified path not exists or not a directory')
        return

    # normalize file name pattern lists
    norm = lambda ps: list(filter(None, map(str.strip, ps.split(os.pathsep))))
    whitelist = norm(whitelist)
    blacklist = norm(blacklist)
    dirs2del = []

    if not blacklist:
        print('there is nothing to clean here')
        return

    for dir_path, dir_names, files in os.walk(path):
        if _correspond(dir_path, path, whitelist):
            continue

        for file_name in files:
            file_name = os.path.join(dir_path, file_name)
            if _correspond(file_name, path, blacklist):
                _drop_file(file_name, dryrun)

        if _correspond(dir_path, path, blacklist):
            dirs2del.append(dir_path)

        _drop_dirs(dirs2del, dryrun)


def _match(name, root, pattern):
    """gitignore-style file name pattern matching"""
    match = lambda n, p: fnmatch(n, p) or os.path.basename(n) == p
    return match(name, pattern) or any([match(p, pattern) for p in \
        os.path.relpath(os.path.normpath(name), root).split(os.sep)])


def _correspond(name, root, petterns):
    """check if file [name] matches to one [patterns]"""
    return any([_match(name, root, item) for item in petterns])


def _drop_file(file_name, dryrun):
    """safely delete a file"""
    print("rm %s" % file_name)
    if not dryrun:
        try:
            os.remove(file_name)
        except Exception as ex:
            print("ERROR: %s" % str(ex))


def _drop_dirs(dirs, dryrun):
    """safely delete empty directories in the right order"""
    for dir_path in reversed(sorted(dirs)):
        print("rm -rf %s" % dir_path)
        if not dryrun:
            try:
                shutil.rmtree(dir_path)
            except Exception as ex:
                print("ERROR: %s" % str(ex))
```

Put this file to current working directory and execute `pyke --help` command to see how function definitions translates to command line options:

```
$ pyke --help
usage: pyke [-h] [-n] [-q] [-f PATH] [-v] [--version]
            {cleanup,log,ver,md5,sum} ...

python make tool

positional arguments:
  {cleanup,log,ver,md5,sum}
    cleanup             delete temporary files
    log                 prints logarithm of a [number] with respect to [base]
    ver                 show python version
    md5                 calculate md5 hash for a string
    sum                 sum two values and print the result

optional arguments:
  -h, --help            show this help message and exit
  -n, --dry-run         do a dry run
  -q, --quiet           do not echo commands
  -f PATH, --file PATH  use explicitly specified pykefile
  -v, --verbose         use verbose logging
  --version             show program's version number and exit
```

It is also possible to get a detailed help for each command:

```
$ pyke md5 --help
usage: pyke md5 [-h] [-n] [-q] [-f PATH] [-v] [--version] value

python make tool

positional arguments:
  value                 any text
```

## License

- Project home page: [https://github.com/dreikanter/pyke](https://github.com/dreikanter/pyke)
- Author: Alex Musayev, [http://alex.musayev.com](http://alex.musayev.com)
- License: [MIT](http://opensource.org/licenses/MIT) (non-viral, totally free)
