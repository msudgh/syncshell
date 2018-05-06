#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# syncshell.py.__main__: execute main function directly"""
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

from fire import Fire
from .config import Config
from .syncshell import Syncshell


if __name__ == "__main__":
    config = Config()

    f = Fire(Syncshell(config.parser))
