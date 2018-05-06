#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# syncshell.py: contain syncshell class of app"""
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

import logging

# Setup logger
logging.basicConfig(level=constants.LOG['level'],
                    format=constants.LOG['format'])
logger = logging.getLogger(__name__)

    
class Syncshell(object):
    def __init__(self, config):
        self.config = config

    def auth(self, token):
        self.token = token
