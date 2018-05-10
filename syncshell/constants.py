#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# constants.py: contain syncshell's consts
import os
from pathlib import Path

# Metainfo
APP_NAME = 'syncshell'

# Log
LOG = {
    'level': 'INFO',
    'format': '↳ %(levelname)s - %(message)s'
}

# Paths
APP_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))  # noqa
CONFIG_FILENAME = '.syncshell.ini'
CONFIG_PATH_TEMPLATE = '{}/{}'.format(APP_ROOT_DIR, CONFIG_FILENAME)
CONFIG_PATH = '{}/{}'.format(Path.home(), CONFIG_FILENAME)

# String Colors
DEFAULT = '\033[39m'
WHITE = '\033[97m'

# String Attr
NORMAL = '\033[0m'
BOLD = '\033[1m'

# History
# TODO: find safe way to find out the shell name
SHELL = os.environ.get('SHELL')
HISTORY_PATH = {
    'bash': '.bash_history',
    'zsh': '.zsh_history',
}
