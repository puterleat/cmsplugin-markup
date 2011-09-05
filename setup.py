#!/usr/bin/env python
PACKAGE_NAME = 'cmsplugin_markup'
PACKAGE_DIR = PACKAGE_NAME

import os, sys

from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

def fullsplit(path, result=None):
    """
    Split a pathname into compontents (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell disutils to put the data_files in platofmr-specific installation
# locations.
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distuils doesn't have
# and easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk(PACKAGE_DIR):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append(
                [dirpath, [os.path.join(dirpath, f) for f in filenames]]
                )
# Small hack for working with bdist_wininst
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

# Dynamically calculate the version based on package.VERSION
version = __import__(PACKAGE_NAME).get_version()

setup(
        name='cmsplugin-markup',
        version=version.replace(' ', '-'),
        description='Adds a plugin based Markup System for django-cms',
        author='Xenofox, LLC',
        author_email='info@xenofox.com',
        url='http://bitbucket.org/xenofox/cmsplugin-markup',
        packages=packages,
        data_files=data_files,
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
            'License :: OSI Approved :: BSD License',
            ]
        )
