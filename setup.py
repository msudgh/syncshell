#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# setup.py: setuptools control

import sys
from setuptools import setup

try:
    from __version__ import __version__
except RuntimeError as e:
    raise RuntimeError('Unable to find version string.')
    sys.exit(1)


with open('README.md') as file:
    long_description = file.read()


setup(
    name='syncshell',
    packages=['syncshell'],
    entry_points={
        'console_scripts': ['syncshell = syncshell.__main__:main']
    },
    version=__version__,
    description='Keep your machine\'s shell history synchronize.',
    long_description=long_description,
    author='Masoud Ghorbani',
    author_email='msud.ghorbani@gmail.com',
    maintainer='Masoud Ghorbani',
    maintainer_email='msud.ghorbani@gmail.com',
    url='https://github.com/msudgh/syncshell',
    install_requires=['pygithub', 'halo']
)
