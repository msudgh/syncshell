#!/usr/bin/env python3

import os

# Metainfo
APP_NAME = "syncshell"

# Paths
APP_ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, os.pardir)
)
CONFIG_FILENAME = ".syncshell.ini"
CONFIG_PATH_TEMPLATE = os.path.join(APP_ROOT_DIR, CONFIG_FILENAME)
CONFIG_PATH = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)
USER_HOME = os.path.expanduser("~")

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
SHELL_HISTORY_PATH = os.path.join(USER_HOME, SUPPORTED_SHELLS[SHELL])
AUTH_MESSAGE = (
    "Enter GitHub token (Visit https://github.com/settings/tokens to generate one)."
)
TOKEN_INPUT = "Token: "
GIST_ID_INPUT = "Gist Id: "
