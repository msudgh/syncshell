#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# config.py: contain config class"""
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

import logging
import sys
import os
from shutil import copy
import time
from configparser import ConfigParser
from . import constants
from gist import GistAPI

# Setup logger
logging.basicConfig(level=constants.LOG['level'],
                    format=constants.LOG['format'])
logger = logging.getLogger(__name__)


class Config(object):
    def __init__(self, path=constants.CONFIG_PATH):
        '''Constructor

        Return configuration placed in config default path

        Keyword arguments:
        path -- the config file path
        '''
        self.path = path
        self.parser = ConfigParser()
        self.gist = None

        # Read cofiguration
        self.read()

    def read(self):
        ''' Read and parse config file and config object '''
        # Copy template config file to home directory
        if os.path.exists(constants.CONFIG_PATH) is False:
            copy(constants.CONFIG_PATH_TEMPLATE, constants.CONFIG_PATH)

        try:
            self.parser.read(self.path)
            self.gist = GistAPI(self.parser['Auth']['token'])
        except:
            logger.error('Unable to read config file.')
            sys.exit(0)

    def write(self):
        ''' Set and write new config '''
        try:
            with open(constants.CONFIG_PATH, 'w') as file:
                self.parser.write(file)
                file.close()
        except:
            logger.error('Unable to set config file.')
            sys.exit(0)

    def check_authorization(self):
        try:
            self.gist.list()
        except:
            logger.error('You\'re token key isn\'t authorized')
            sys.exit(0)
