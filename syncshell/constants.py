from pathlib import Path

# Metainfo
APP_NAME = 'syncshell'

# Log
LOG = {
    'level': 'INFO',
    'format': '({}) ↳ %(levelname)s - %(message)s'.format(APP_NAME)
}

# Paths
CONFIG_PATH = '{}/.syncshell.ini'.format(Path.home())
