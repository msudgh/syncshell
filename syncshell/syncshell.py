#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# syncshell.py: contain syncshell class of app"""
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

import sys
import logging
import textwrap
from . import constants
from .config import Config
from gist import GistAPI

# Setup logger
logging.basicConfig(level=constants.LOG['level'],
                    format=constants.LOG['format'])
logger = logging.getLogger(__name__)


# Configuration
config = Config()

class Syncshell(object):
    def __init__(self):
        pass

    def auth(self):
        ''' Retrive, set and validate user token '''
        
        try:
            # Help message
            print(textwrap.fill('If you don\'t have Github token key, Please, first go to {}{}https://github.com/settings/tokens{} address create a personal access token with gist scope.'.format(constants.WHITE, constants.BOLD, constants.NORMAL), width=80))  # noqa

            # Promte token key
            config.parser['Auth']['token'] = str(input('Github Token Key: '))

            # Set new token key
            config.gist = GistAPI(config.parser['Auth']['token'])

            # Validate token key
            config.check_authorization()
        except KeyboardInterrupt as e:
            sys.exit(0)

    def upload(self, history_path):
        ''' Upload current history '''
        
        # Validate token key
        config.check_authorization()

        # config.gist.create('test')
