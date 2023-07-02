#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from shutil import copy
from configparser import ConfigParser, Error as ConfigParserError
from github import Github, GithubException
from syncshell.utils import constants


class SyncShellConfig:
    """Config class consits of fundamental methods to read, write and validate
    config file for different scenarios of syncshell.
    """

    def __init__(self, path=constants.CONFIG_PATH):
        """Constructor

        Return configuration placed in config default path

        Keyword arguments:
        path -- the config file path
        """
        self.path = path
        self.parser = ConfigParser()
        self.gist = None

        # Copy template config file to home directory
        if os.path.exists(constants.CONFIG_PATH) is False:
            copy(constants.CONFIG_PATH_TEMPLATE, constants.CONFIG_PATH)

    def __deepcopy__(self, memo):
        return self

    def read(self):
        """Read and parse config file and config object"""
        try:
            self.parser.read(self.path)
            self.gist = Github(self.parser["Auth"]["token"])

            # Set Shell and write new config
            if not self.parser["Shell"]["name"] or not self.parser["Shell"]["path"]:
                self.parser["Shell"]["name"] = constants.SHELL
                self.parser["Shell"]["path"] = constants.SHELL_HISTORY_PATH

                self.write()

            return True
        except ConfigParserError:
            print("Unable to read config file.")
            sys.exit(1)
            return False

    def write(self, path=None):
        """Set and write new config"""
        self.path = path or constants.CONFIG_PATH

        try:
            with open(self.path, "w") as file:
                self.parser.write(file)
                file.close()

            return True
        except IOError:
            print("Unable to set config file.")
            sys.exit(1)
            return False

    def is_logged_in(self):
        """Check user exists in config file"""
        try:
            user = self.gist.get_user()

            if not user.login:
                return False

            return True
        except GithubException:
            return False

    def get_shell_history(self):
        """Return shell history file path and content"""
        with open(self.parser["Shell"]["path"], "r") as history_file:
            history_file_path = os.path.basename(history_file.name)
            try:
                content = history_file.read()

                return {"path": history_file_path, "content": content}
            except UnicodeDecodeError:
                with open(
                    self.parser["Shell"]["path"], "r", encoding="latin-1"
                ) as history_file_latin_1:
                    content = history_file_latin_1.read()

                return {"path": history_file_path, "content": content}

    def write_shell_history(self, content):
        """Write shell history content"""
        with open(self.parser["Shell"]["path"], "w") as history_file:
            history_file.write(content)

    def get_config(self):
        """Return config file path and content"""
        with open(self.path, mode="r") as config_file:
            config_file_path = os.path.basename(config_file.name)

            # Remove token key on uplaod
            lines = config_file.readlines()
            lines.pop(1)

            return {
                "path": config_file_path,
                "content": "".join(map(str, lines)),
            }