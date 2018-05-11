#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# syncshell.py: contain syncshell class of app
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"
__license__ = "MIT"
__version__ = "0.1.0"

import sys
import os
import logging
import textwrap
from . import constants
import time
from configparser import ConfigParser
from .config import Config
from github import Github, InputFileContent
from pathlib import Path
from halo import Halo

# Setup logger
logging.basicConfig(level=constants.LOG['level'],
                    format=constants.LOG['format'])
logger = logging.getLogger(__name__)


# Configuration
config = Config()
config.read()


def spinner_callback(spinner, message, status):
    if status == 'fail':
        spinner.fail(message)
    elif status == 'succeed':
        spinner.succeed(message)


class Syncshell(object):
    def __init__(self):
        pass

    def auth(self):
        ''' Retrive, set and validate user token '''
        try:
            # Help message
            print(textwrap.fill('If you don\'t have Github token key, Please, first go to {}{}https://github.com/settings/tokens{} address create a personal access token with gist scope.'.format(constants.WHITE, constants.BOLD, constants.NORMAL), width=80))  # noqa

            # Promte token key
            config.parser['Auth']['token'] = str(
                input('Enter your Github token key: '))

            spinner = Halo(text='Authentication ...', spinner='dots')
            spinner.start()

            # Set new token key
            config.gist = Github(config.parser['Auth']['token'])

            # Validate token key and if it's valid write config object
            if config.check_authorization(spinner, spinner_callback):
                config.write()
        except KeyboardInterrupt as e:
            sys.exit(0)

    def upload(self, history_path=None):
        ''' Upload current history '''
        spinner = Halo(text='Uploading ...', spinner='dots')
        spinner.start()

        # Validate token key
        config.check_authorization(spinner, spinner_callback)

        if not history_path:
            history_path = '{}/{}'.format(Path.home(),
                                          config.parser['Shell']['path'])

        # Read history file from default path of shell or history_path
        try:
            gist_meta = {
                'description': 'syncshell Gist',
                'files': {},
                'public': False
            }

            with open(history_path, errors='ignore', mode='r') as history_file:
                gist_meta['files'] = {
                    os.path.basename(history_file.name): InputFileContent(history_file.read()),
                }
                history_file.close()

            gist = config.gist.get_user().create_gist(False,
                                                      gist_meta['files'],
                                                      gist_meta['description'])

            # # Set upload date
            config.parser['Upload']['last_date'] = str(int(time.time()))

            # # Set Gist id
            if config.parser['Auth']['gist_id']:
                spinner_callback(
                    spinner, 'Gist ID ({}) updated.'.format(gist.id), 'succeed')
            else:
                spinner_callback(
                    spinner, 'New Gist ID ({}) created.'.format(gist.id), 'succeed')

            config.parser['Auth']['gist_id'] = gist.id
            config.write()

            with open(constants.CONFIG_PATH, mode='r') as config_file:
                # Remove token key on uplaod
                lines = config_file.readlines()
                lines.pop(1)

                gist_meta['files'] = {
                    os.path.basename(config_file.name): InputFileContent(''.join(map(str, lines)))
                }
                config_file.close()

            gist.edit(files=gist_meta['files'])

        except FileNotFoundError as e:
            spinner_callback(spinner, 'Couldn\'t find history file.', 'fail')
            sys.exit(0)
        except KeyError as e:
            spinner_callback(spinner, 'Request\'s data is not valid', 'fail')
            sys.exit(0)

    def download(self, token=config.parser['Auth']['token'], gist_id=config.parser['Auth']['gist_id'], out=None):
        ''' Retrive token and gist id to download gist '''
        try:
            token = token or str(input('Enter your Github token key: '))
            gist_id = gist_id or str(input('Enter your Gist ID: '))
        except KeyboardInterrupt as e:
            sys.exit(0)
