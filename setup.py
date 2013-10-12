import os
from setuptools import setup, find_packages
import pyke.authoring
from pyke.version import get_version
import subprocess as sp


def get_data_files(path):
    files = []
    path = os.path.abspath(path)

    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in ['.py', '.pyc']:
                full_path = os.path.join(dirname, filename)
                files.append(os.path.relpath(full_path, path))

    return files


def get_desc(file_name):
    """Get long description by converting README file to reStructuredText."""
    cmd = "pandoc --from=markdown --to=rst %s" % file_name
    try:
        with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE) as process:
            return process.stdout.read().decode('utf-8')
    except FileNotFoundError:
        return open(file_name).read()


setup(
    name='pyke',
    description='A missing Python make tool.',
    version=get_version(),
    license=pyke.authoring.__license__,
    author=pyke.authoring.__author__,
    author_email=pyke.authoring.__email__,
    url=pyke.authoring.__url__,
    long_description=get_desc('README.md'),
    platforms=['any'],
    packages=find_packages(),
    package_data={'pyke': get_data_files('pyke')},
    install_requires=[],
    entry_points={'console_scripts': ['pyke = pyke.pyke:main']},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
    ],
    dependency_links=[],
)
