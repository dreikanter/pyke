#!/usr/bin/env python

# coding: utf-8

import os
from setuptools import setup, find_packages
import awesometool.authoring
from awesometool.version import get_version


def get_data_files(path):
    files = []
    path = os.path.abspath(path)

    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in ['.py', '.pyc']:
                full_path = os.path.join(dirname, filename)
                files.append(os.path.relpath(full_path, path))

    return files


setup(
    name='awesometool',
    description='Yet another awesome tool.',
    version=get_version(),
    license=awesometool.authoring.__license__,
    author=awesometool.authoring.__author__,
    author_email=awesometool.authoring.__email__,
    url=awesometool.authoring.__url__,

    # This will use readme contents as a long description
    long_description=open('README.md').read(),

    platforms=['any'],
    packages=find_packages(),

    # This will put all data files from the package directory to the egg
    package_data={'awesometool': get_data_files('awesometool')},

    # TODO: Put here required package names
    install_requires=[
    ],

    # TODO: Use this to define the tool's command
    entry_points={'console_scripts': ['awesometool = awesometool.awesometool:main']},

    include_package_data=True,
    zip_safe=False,

    # TODO: Get the relevant classifiers from here:
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Development Status :: 1 - Planning
        # Development Status :: 2 - Pre-Alpha
        # Development Status :: 3 - Alpha
        # Development Status :: 4 - Beta
        # Development Status :: 5 - Production/Stable
        # Development Status :: 6 - Mature
        # Development Status :: 7 - Inactive
        # Environment :: Console
        # Environment :: MacOS X
        # Environment :: Win32 (MS Windows)
        # Intended Audience :: Customer Service
        # Intended Audience :: Developers
        # Intended Audience :: Education
        # Intended Audience :: End Users/Desktop
        # Intended Audience :: Financial and Insurance Industry
        # Intended Audience :: Healthcare Industry
        # Intended Audience :: Information Technology
        # Intended Audience :: Legal Industry
        # Intended Audience :: Manufacturing
        # Intended Audience :: Other Audience
        # Intended Audience :: Religion
        # Intended Audience :: Science/Research
        # Intended Audience :: System Administrators
        # Intended Audience :: Telecommunications Industry
        # License :: Free For Educational Use
        # License :: Free For Home Use
        # License :: Free for non-commercial use
        # License :: Freely Distributable
        # License :: OSI Approved :: Academic Free License (AFL)
        # License :: OSI Approved :: Apache Software License
        # License :: OSI Approved :: BSD License
        # License :: OSI Approved :: GNU General Public License v2 (GPLv2)
        # License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
        # License :: OSI Approved :: GNU General Public License v3 (GPLv3)
        # License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)
        # License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)
        # License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)
        # License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
        # License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)
        # License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
        # License :: OSI Approved :: MIT License
        # License :: Other/Proprietary License
        # License :: Public Domain
        # Natural Language :: English
        # Operating System :: MacOS
        # Operating System :: Microsoft :: Windows
        # Operating System :: OS Independent
        # Operating System :: POSIX :: Linux
        # Operating System :: Unix
        # Programming Language :: Python
        # Programming Language :: Python :: 2
        # Programming Language :: Python :: 2.3
        # Programming Language :: Python :: 2.4
        # Programming Language :: Python :: 2.5
        # Programming Language :: Python :: 2.6
        # Programming Language :: Python :: 2.7
        # Programming Language :: Python :: 2 :: Only
        # Programming Language :: Python :: 3
        # Programming Language :: Python :: 3.0
        # Programming Language :: Python :: 3.1
        # Programming Language :: Python :: 3.2
        # Programming Language :: Python :: 3.3
        # Topic :: Utilities
    ],

    # TODO: Define external dependencies
    dependency_links=[
        # Dependencies that's not on PyPI could be defined like this:
        # 'https://github.com/{user}/{project}/tarball/master#egg={package}'
    ],
)
