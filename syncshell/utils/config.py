#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from shutil import copy
from configparser import ConfigParser, Error as ConfigParserError
from github import Github, GithubException
from github import Auth
from syncshell.utils import constants


class SyncShellConfig:
    """Config class consits of fundamental methods to read, save and validate
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
        self.github = None

        # Copy template config file to home directory
        if os.path.exists(constants.CONFIG_PATH) is False:
            copy(constants.CONFIG_PATH_TEMPLATE, constants.CONFIG_PATH)

    def __deepcopy__(self, memo):
        return self

    def read_config(self):
        """Read and parse config file and config object"""
        try:
            with open(self.path) as fh:
                self.parser.read_file(fh)

            # if parser has auth token, then create github object
            has_auth_token = (
                self.parser.has_option("Auth", "token")
                and len(self.parser["Auth"]["token"]) > 0
            )

            if has_auth_token:
                auth_token = self.parser["Auth"]["token"]
                self.github = Github(auth=Auth.Token(auth_token))

            shell_name = self.parser["Shell"]["name"]
            shell_path = self.parser["Shell"]["path"]

            # Overwrite shell config if not exists
            if not shell_name or not shell_path:
                self.parser["Shell"]["name"] = constants.SHELL
                self.parser["Shell"]["path"] = constants.SHELL_HISTORY_PATH

                self.save_config()

            return True
        except ConfigParserError:
            print("Unable to read config file.")
            sys.exit(1)

    def save_config(self, path=None):
        """Save new config"""
        self.path = path or constants.CONFIG_PATH

        try:
            with open(self.path, "w") as file:
                self.parser.write(file)
                file.close()

            return True
        except IOError:
            print("Unable to save config file.")
            sys.exit(1)

    def is_logged_in(self):
        """Check user exists in config file"""
        try:
            user = self.github.get_user()

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
        try:
            with open(self.parser["Shell"]["path"], "w") as history_file:
                history_file.write(content)
                return True
        except IOError:
            return False

    def get_config(self):
        """Return config file path and content"""
        with open(self.path, "r") as config_file:
            config_file_path = os.path.basename(config_file.name)

            # Remove token key on uplaod
            lines = config_file.readlines()
            lines.pop(1)

            return {
                "path": config_file_path,
                "content": "".join(map(str, lines)),
            }
