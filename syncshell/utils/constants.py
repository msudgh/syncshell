#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Metainfo
APP_NAME = 'syncshell'

# Paths
APP_ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.pardir,
        os.pardir
    )
)
CONFIG_FILENAME = '.syncshell.ini'
CONFIG_PATH_TEMPLATE = os.path.join(APP_ROOT_DIR, CONFIG_FILENAME)
CONFIG_PATH = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)

# String Colors
DEFAULT = '\033[39m'
WHITE = '\033[97m'

# String Attr
NORMAL = '\033[0m'
BOLD = '\033[1m'

# History
SHELL = os.environ.get('SHELL')
HISTORY_PATH = {
    'bash': '.bash_history',
    'zsh': '.zsh_history',
}

HELP_MESSAGE = ("If you don't have Github token key, "
                "Please, first go to "
                f"{WHITE}{BOLD}https://github.com/settings/tokens{NORMAL} "
                "address create a personal access token with gist scope.")
