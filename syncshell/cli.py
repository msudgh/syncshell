#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import textwrap
import time
from configparser import ConfigParser
from subprocess import run, PIPE
from github import Github, InputFileContent, UnknownObjectException
from syncshell.utils import constants, spinner as Spinner
from syncshell.config import SyncShellConfig

# Configuration
config = SyncShellConfig()
config.read()


class Application:
    """SyncShell CLI Application"""

    def __prepare_payload(self):
        """Prepare history and config file for upload"""

        files = {}
        config_path = constants.CONFIG_PATH

        with open(constants.SHELL_HISTORY_PATH, "r") as history_file:
            history_file_path = os.path.basename(history_file.name)
            try:
                content = history_file.read()
                files[history_file_path] = InputFileContent(content)
            except UnicodeDecodeError:
                with open(
                    constants.SHELL_HISTORY_PATH, "r", encoding="latin-1"
                ) as history_file_latin_1:
                    content = history_file_latin_1.read()
                    files[history_file_path] = InputFileContent(content)

        with open(config_path, mode="r") as config_file:
            # Remove token key on uplaod
            lines = config_file.readlines()
            lines.pop(1)

            files[os.path.basename(config_file.name)] = InputFileContent(
                "".join(map(str, lines))
            )

        return files

    def auth(self):
        """Retrieve & authenticate user token"""
        try:
            # Help message
            getting_started = textwrap.fill(constants.HELP_MESSAGE, width=80)
            print(getting_started)

            # Promte token key
            prompt_token = input("Enter your Github token key: ")
            config.parser["Auth"]["token"] = str(prompt_token)

            # Set new token key
            config.gist = Github(config.parser["Auth"]["token"])

            spinner = Spinner.NewTask("Check authentication...")

            # Write config file if Github user alreaded authorized
            if config.is_logged_in():
                spinner.succeed("Your Github token key is authenticated.")
                config.write()
            else:
                spinner.fail("Your Github token key is not valid.")
                sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(0)

    def upload(self):
        """Upload current history"""
        spinner = Spinner.NewTask("Uploading ...")

        # Exit process if not logged in
        if not config.is_logged_in():
            spinner.fail("Your Github token key is not valid. Authenticate first.")
            sys.exit(1)

        try:
            if config.parser["Auth"]["gist_id"]:
                gist = config.gist.get_gist(config.parser["Auth"]["gist_id"])

                # Set upload date
                config.parser["Upload"]["last_date"] = str(int(time.time()))
                config.write()

                files = self.__prepare_payload()

                gist.edit(files=files)

                spinner.succeed(f"Gist ID ({gist.id}) updated.")
            else:
                description = "SyncShell Gist"

                user = config.gist.get_user()
                files = self.__prepare_payload()
                gist = user.create_gist(False, files, description)

                # Set upload date
                config.parser["Upload"]["last_date"] = str(int(time.time()))
                config.parser["Auth"]["gist_id"] = gist.id

                config.write()

                files = self.__prepare_payload()
                gist.edit(files=files)
                spinner.succeed(f"New Gist ID ({gist.id}) created.")
        except FileNotFoundError:
            spinner.fail("Couldn't find history file.")
            sys.exit(1)
        except KeyError:
            spinner.fail("Request's data is not valid")
            sys.exit(1)
        except UnknownObjectException as error:
            if error.status == 404:
                spinner.fail(
                    "Gist ID not found. If you manually deleted Gist "
                    "in past then try to execute upload command "
                    "again for new upload and sync."
                )

                config.parser["Auth"]["gist_id"] = ""
                config.write()
            sys.exit(1)

    def download(self):
        """Download Gist and save it to history file"""

        try:
            token = str(input("Enter your Github token key: "))
            gist_id = str(input("Enter your Gist ID: "))

            spinner = Spinner.NewTask("Downloading ...")

            # Redefine Github instance with new token
            config.gist = Github(token)

            # Exit process if not logged in
            if not config.is_logged_in():
                sys.exit(1)

            # Download Gist object
            gist = config.gist.get_gist(gist_id)

            if len(gist.files) != 2:
                spinner.fail("Gist content corrupted, Please use another Gist.")
                sys.exit(1)

            # Read new configuration
            temp_config = ConfigParser()
            temp_config.read_string(gist.files[constants.CONFIG_FILENAME].content)

            # Check shell names
            if temp_config["Shell"]["name"] != config.parser["Shell"]["name"]:
                spinner.fail("Unable to convert different shells")
                sys.exit(1)

            # Write configuration
            config.parser["Auth"]["token"] = token
            config.parser["Auth"]["gist_id"] = gist_id
            config.write()

            with open(constants.SHELL_HISTORY_PATH, "r+") as history_file:
                history = history_file.read()

                new_changes = gist.files[
                    constants.SUPPORTED_SHELLS[config.parser["Shell"]["name"]]
                ]

                synced_changes = new_changes.content + history

                awk_proc = run(
                    [
                        "awk",
                        '"/:[0-9]/ { if(s) { print s } s=$0 } !/:[0-9]/ { s=s"\n"$0 } END { print s }"',
                    ],
                    stdout=PIPE,
                    input=bytes(synced_changes, encoding="utf8"),
                    check=True,
                )

                # Remove duplicate lines
                awk_duplicates_proc = run(
                    [
                        "awk",
                        '"!visited[$0]++ { print $0 }"',
                    ],
                    stdout=PIPE,
                    input=bytes(awk_proc.stdout.decode("utf-8"), encoding="utf8"),
                    check=True,
                )

                sort_proc = run(
                    ["sort", "-u"],
                    stdout=PIPE,
                    input=bytes(
                        awk_duplicates_proc.stdout.decode("utf-8"), encoding="utf8"
                    ),
                    check=True,
                )

                history_file.write(sort_proc.stdout.decode("utf-8"))
                spinner.succeed("Gist downloaded and stored.")
        except KeyboardInterrupt:
            sys.exit(0)
        except FileNotFoundError:
            spinner.fail("Couldn't find history file.")
            sys.exit(1)
        except OSError:
            sys.exit(1)
