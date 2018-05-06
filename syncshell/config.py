#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# config.py: contain config class"""
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

import logging
import sys
import time
from configparser import ConfigParser
from . import constants

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
        
        # Read cofiguration
        self.read()

    def read(self):
        ''' Read and parse config file and config object '''
        try:
            self.parser.read(self.path)
        except:
            logger.error('Unable to read config file.')
            sys.exit(0)

    def write(self):
        ''' Set and write new config '''
        try:
            with open(constants.CONFIG_PATH, 'w') as file:
                file.write(self.parser)
                file.close()

                return True
        except:
            logger.error('Unable to set config file.')
            sys.exit(0)

