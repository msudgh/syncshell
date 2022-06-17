#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# config.py: contain config class
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"

import logging
import sys
import os
from shutil import copy
import time
import re
from configparser import ConfigParser
from github import Github
import constants, utils

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

        # Copy template config file to home directory
        if os.path.exists(constants.CONFIG_PATH) is False:
            copy(constants.CONFIG_PATH_TEMPLATE, constants.CONFIG_PATH)

    def __deepcopy__(self, memo):
        return self

    def read(self):
        ''' Read and parse config file and config object '''
        try:
            self.parser.read(self.path)
            self.gist = Github(self.parser['Auth']['token'])

            # Set Shell and write new config
            if (not self.parser['Shell']['name'] or
                    not self.parser['Shell']['path']):
                # Extract shell name
                regex = r"([^/]*$)"
                matches = re.search(regex, constants.SHELL)
                shell = matches.group() or 'zsh'

                self.parser['Shell']['name'] = shell
                self.parser['Shell']['path'] = constants.HISTORY_PATH[shell]

                self.write()

            return True
        except:
            logger.error('Unable to read config file.')

            return False
            sys.exit(0)

    def write(self, path=None):
        ''' Set and write new config '''
        self.path = path or constants.CONFIG_PATH

        try:
            with open(self.path, 'w') as file:
                self.parser.write(file)
                file.close()

            return True
        except:
            logger.error('Unable to set config file.')

            return False
            sys.exit(1)

    # Check user exists
    def is_logged_in(self):
        spinner = utils.Spinner('Check authenticated ...')

        try:
            self.gist.get_user().login
            success_text = 'Your Github token key authenticated and confirmed.'
            spinner.succeed(success_text)
            return True
        except:
            fail_text = 'Your Github token key is not valid. Authenticate first.'
            spinner.fail(fail_text)
            return False
