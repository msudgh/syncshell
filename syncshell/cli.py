#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# syncshell.py: contain syncshell class of app
__author__ = "Masoud Ghorbani <msud.ghorbani@gmail.com>"

import sys
import os
import logging
import textwrap
import constants
import time
import utils
from configparser import ConfigParser
from subprocess import run, PIPE
from config import Config
from github import Github, InputFileContent, UnknownObjectException
from pathlib import Path

# Setup logger
logging.basicConfig(level=constants.LOG['level'],
                    format=constants.LOG['format'])
logger = logging.getLogger(__name__)

# Configuration
config = Config()
config.read()


def prepare_payload():
    ''' Prepare history and config file for upload '''

    files = {}
    history_path = '{}/{}'.format(Path.home(), config.parser['Shell']['path'])
    config_path = constants.CONFIG_PATH

    with open(history_path, errors='ignore', mode='r') as history_file:
        files[os.path.basename(history_file.name)] = InputFileContent(
            history_file.read())

    with open(config_path, mode='r') as config_file:
        # Remove token key on uplaod
        lines = config_file.readlines()
        lines.pop(1)

        files[os.path.basename(config_file.name)] = InputFileContent(
            ''.join(map(str, lines)))

    return files


class Application(object):
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

            # Set new token key
            config.gist = Github(config.parser['Auth']['token'])

            # Write config file if Github user alreaded authorized
            if config.is_logged_in():
                config.write()
        except KeyboardInterrupt as e:
            sys.exit(0)

    def upload(self, history_path=None):
        ''' Upload current history '''
        spinner = utils.Spinner('Uploading ...')

        # Exit process if not logged in
        if not config.is_logged_in():
            sys.exit(1)

        try:
            files = prepare_payload()
            if config.parser['Auth']['gist_id']:
                gist = config.gist.get_gist(config.parser['Auth']['gist_id'])

                # Set upload date
                config.parser['Upload']['last_date'] = str(int(time.time()))
                config.write()

                gist.edit(files=files)

                spinner.succeed('Gist ID ({}) updated.'.format(gist.id))
            else:
                description = 'SyncShell Gist'
                user = config.gist.get_user()
                gist = user.create_gist(False, files, description)

                # Set upload date
                config.parser['Upload']['last_date'] = str(int(time.time()))
                config.parser['Auth']['gist_id'] = gist.id
                config.write()

                gist.edit(files=files)
                spinner.succeed('New Gist ID ({}) created.'.format(gist.id))
        except FileNotFoundError as e:
            spinner.fail('Couldn\'t find history file.')
            sys.exit(1)
        except KeyError as e:
            spinner.fail('Request\'s data is not valid')
            sys.exit(1)
        except UnknownObjectException as e:
            if e.status == 404:
                config.parser['Auth']['gist_id'] = ''
                config.write()

                logger.warn('To create new gist run command again.')
                spinner.fail('{} - {}'.format(e.status, e.data['message']))
            sys.exit(1)

    def download(self, token=config.parser['Auth']['token'], gist_id=config.parser['Auth']['gist_id'], out=None):
        ''' Retrive token and gist id to download gist 

        Here after authorization and downloading gist by `awk` command we'll
        try to order commands to unix timestamps and sort(uniq) them by `sort`
        command.
        '''
        try:
            token = token or str(input('Enter your Github token key: '))
            gist_id = gist_id or str(input('Enter your Gist ID: '))

            spinner = utils.Spinner('Downloading ...')

            # Redefine Github instance with new token
            config.gist = Github(token)

            # Exit process if not logged in
            if not config.is_logged_in():
                sys.exit(1)

            # Download Gist object
            gist = config.gist.get_gist(gist_id)

            # TODO: use checksum instead checking length of files
            if len(gist.files) != 2:
                spinner.fail(
                    'Gist contents are corrupted, Please be sure about the uploaded content.')
                sys.exit(1)

            config_file = gist.files[constants.CONFIG_FILENAME]

            # Read configuration
            temp_config = ConfigParser()
            temp_config.read_string(config_file.content)

            # Check shell names
            if (temp_config['Shell']['name'] != config.parser['Shell']['name']):
                spinner.fail(
                    'Shells arn\'t match, At this momment syncshell is unable to convert history of different shells')
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

            awk_proc = run(['awk', '"/:[0-9]/ { if(s) { print s } s=$0 } !/:[0-9]/ { s=s"\n"$0 } END { print s }"'],
                           stdout=PIPE,  input=bytes(history, encoding='utf8'))

            sort_proc = run(['sort', '-u'], stdout=PIPE, input=awk_proc.stdout)

            with open(out, 'w') as file:
                file.write(sort_proc.stdout.decode())

            spinner.succeed('Gist downloaded and stored.')

            return True

        except KeyboardInterrupt as e:
            sys.exit(0)
        except FileNotFoundError as e:
            spinner.fail('Couldn\'t find history file.')
            sys.exit(1)
