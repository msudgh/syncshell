#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bootstrap.py: contain main() function of app"""
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

import logging
from . import constants

# Setup logger
logging.basicConfig(level=constants.LOG['level'],
                    format=constants.LOG['format'])
logger = logging.getLogger(__name__)


class Syncshell(object):
    def auth(self):
        pass
