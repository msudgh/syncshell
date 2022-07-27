#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

# Metainfo
APP_NAME = "syncshell"

# Paths
APP_ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir)
)
CONFIG_FILENAME = ".syncshell.ini"
CONFIG_PATH_TEMPLATE = os.path.join(APP_ROOT_DIR, CONFIG_FILENAME)
CONFIG_PATH = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)

# String Colors
DEFAULT = "\033[39m"
WHITE = "\033[97m"

# String Attr
NORMAL = "\033[0m"
BOLD = "\033[1m"

# History
SUPPORTED_SHELLS = {
    "bash": ".bash_history",
    "zsh": ".zsh_history",
}
SHELL = os.path.basename(os.environ.get("SHELL", "bash"))
SHELL_HISTORY_PATH = str(Path.joinpath(Path.home(), SUPPORTED_SHELLS[SHELL]))
HELP_MESSAGE = (
    "If you don't have Github token key, "
    "Please, first go to "
    f"{WHITE}{BOLD}https://github.com/settings/tokens{NORMAL} "
    "address create a personal access token with gist scope."
)
