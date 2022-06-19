#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from pathlib import Path
from shutil import copy
import re
from configparser import ConfigParser, Error as ConfigParserError
from github import Github, GithubException
from syncshell.utils import constants, spinner as Spinner


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
                # Extract shell name
                regex = r"([^/]*$)"
                matches = re.search(regex, constants.SHELL)
                shell = matches.group() or "zsh"

                self.parser["Shell"]["name"] = shell
                self.parser["Shell"]["path"] = constants.HISTORY_PATH[shell]

                self.write()

            return True
        except ConfigParserError:
            print("Unable to read config file.")
            sys.exit(1)

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
        spinner = Spinner.NewTask("Check authenticated ...")

        try:
            if self.gist.get_user().login:
                success_text = "Your Github token key authenticated and confirmed."
                spinner.succeed(success_text)
                return True

            return False
        except GithubException:
            fail_text = "Your Github token key is not valid. Authenticate first."
            spinner.fail(fail_text)
            return False

    def get_history_path(self):
        """Return path of shell history file"""
        return Path.joinpath(Path.home(), self.parser["Shell"]["path"])
