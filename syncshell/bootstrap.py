#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# bootstrap.py: contain main() function of app"""
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

import logging
from . import constants

# Setup logger
logging.basicConfig(level=constants.log['level'],
                    format=constants.log['format'])
logger = logging.getLogger(__name__)


class Syncshell(object):
    def auth(self):
        logger.info('hi')
