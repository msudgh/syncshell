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
from subprocess import run, PIPE
from .config import Config
from github import Github, InputFileContent, UnknownObjectException
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
        spinner.stop()
    elif status == 'succeed':
        spinner.succeed(message)


def read_files():
    ''' Read history and setting file '''

    history_path = '{}/{}'.format(Path.home(), config.parser['Shell']['path'])
    files = {}
    with open(history_path, errors='ignore', mode='r') as history_file:
        files[os.path.basename(history_file.name)] = InputFileContent(
            history_file.read())

    with open(constants.CONFIG_PATH, mode='r') as config_file:
        # Remove token key on uplaod
        lines = config_file.readlines()
        lines.pop(1)

        files[os.path.basename(config_file.name)] = InputFileContent(
            ''.join(map(str, lines)))

    return files


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

        try:
            if config.parser['Auth']['gist_id']:
                gist = config.gist.get_gist(config.parser['Auth']['gist_id'])

                # Set upload date
                config.parser['Upload']['last_date'] = str(int(time.time()))
                config.write()

                gist.edit(files=read_files())

                spinner_callback(
                    spinner, 'Gist ID ({}) updated.'.format(gist.id), 'succeed')
            else:
                description = 'syncshell Gist'
                gist = config.gist.get_user().create_gist(False,
                                                          read_files(),
                                                          description)

                # Set upload date
                config.parser['Upload']['last_date'] = str(int(time.time()))
                config.parser['Auth']['gist_id'] = gist.id
                config.write()

                gist.edit(files=read_files())
                spinner_callback(
                    spinner, 'New Gist ID ({}) created.'.format(gist.id), 'succeed')
        except FileNotFoundError as e:
            spinner_callback(spinner, 'Couldn\'t find history file.', 'fail')
            sys.exit(1)
        except KeyError as e:
            spinner_callback(spinner, 'Request\'s data is not valid', 'fail')
            sys.exit(1)
        except UnknownObjectException as e:
            if e.status == 404:
                config.parser['Auth']['gist_id'] = ''
                config.write()

                logger.warn('To create new gist run command again.')

            spinner_callback(
                spinner, '{} - {}'.format(e.status, e.data['message']), 'fail')
            sys.exit(1)

    def download(self, token=config.parser['Auth']['token'], gist_id=config.parser['Auth']['gist_id'], out=None):
        ''' Retrive token and gist id to download gist '''
        try:
            token = token or str(input('Enter your Github token key: '))
            gist_id = gist_id or str(input('Enter your Gist ID: '))

            spinner = Halo(text='Downloading ...', spinner='dots')
            spinner.start()

            # Redefine Github instance with new token
            config.gist = Github(token)

            # Validate token key
            config.check_authorization(spinner, spinner_callback)

            # Download Gist object
            gist = config.gist.get_gist(gist_id)

            # TODO: use checksum instead checking length of files
            if len(gist.files) != 2:
                spinner_callback(
                    spinner, 'Gist contents are corrupted, Please be sure about the uploaded content.', 'fail')
                sys.exit(1)

            config_file = gist.files[constants.CONFIG_FILENAME]

            # Read configuration
            temp_config = ConfigParser()
            temp_config.read_string(config_file.content)

            # Check shell names
            if (temp_config['Shell']['name'] != config.parser['Shell']['name']):
                spinner_callback(
                    spinner, 'Shells arn\'t match, At this momment syncshell is unable to convert history of different shells', 'fail')
                sys.exit(1)

            # Write configuration
            config.parser['Auth']['token'] = token
            config.parser['Auth']['gist_id'] = gist_id
            config.write()

            # Save history file
            out = out or '{}/{}'.format(Path.home(),
                                        config.parser['Shell']['path'])
            history_file = gist.files[constants.HISTORY_PATH[config.parser['Shell']['name']]]

            with open(out, 'r', encoding="utf-8", errors='ignore') as system_history:
                content = system_history.read()

            history = history_file.content + content

            awk_proc = run(['awk', '"/:[0-9]/ { if(s) { print s } s=$0 } !/:[0-9]/ { s=s"\n"$0 } END { print s }"'], stdout=PIPE,  input=bytes(history, encoding='utf8'))

            sort_proc = run(['sort', '-u'], stdout=PIPE, input=awk_proc.stdout)

            with open(out, 'w') as file:
                file.write(sort_proc.stdout.decode())

            spinner_callback(spinner, 'Gist downloaded and stored.', 'succeed')

        except KeyboardInterrupt as e:
            sys.exit(0)
        except FileNotFoundError as e:
            spinner_callback(spinner, 'Couldn\'t find history file.', 'fail')
            sys.exit(1)
