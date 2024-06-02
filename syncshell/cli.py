#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
from configparser import ConfigParser
from subprocess import run, PIPE
from github import Github, InputFileContent, UnknownObjectException
from syncshell.utils import constants, spinner as Spinner
from syncshell.utils.config import SyncShellConfig
from fire import Fire

# Configuration
config = SyncShellConfig()
config.read_config()


def bundle_files_for_upload():
    """Bundle history and config files for upload"""

    files = {}
    history_file = config.get_shell_history()
    config_file = config.get_config()

    files[history_file["path"]] = InputFileContent(history_file["content"])
    files[config_file["path"]] = InputFileContent(config_file["content"])

    return files


class Application:
    """SyncShell CLI Application"""

    def auth(self):
        """Retrieve & authenticate user's token"""
        print(constants.AUTH_MESSAGE)

        try:
            config.parser["Auth"]["token"] = str(input(constants.TOKEN_INPUT))
            config.github = Github(config.parser["Auth"]["token"])

            spinner = Spinner.NewTask("Check authentication...")

            # Write config file if Github user already authorized
            if config.is_logged_in():
                spinner.succeed("Github token is authenticated.")
                config.save_config()
            else:
                spinner.fail("Github token is not valid.")
                sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(0)

    def upload(self):
        """Upload history and config file to Gist"""
        spinner = Spinner.NewTask("Uploading ...")

        # Exit process if not logged in
        if not config.is_logged_in():
            spinner.fail(
                "Github token key is not valid. Use 'auth' command to authenticate."
            )
            sys.exit(1)

        try:
            gist_id = config.parser["Auth"]["gist_id"]
            if gist_id:
                gist = config.github.get_gist(gist_id)

                # Set upload date
                config.parser["Upload"]["last_date"] = str(int(time.time()))
                config.save_config()

                gist.edit(files=bundle_files_for_upload())

                spinner.succeed(f"Gist ID ({gist.id}) updated.")
            else:
                description = "SyncShell Gist"

                user = config.github.get_user()
                gist = user.create_gist(False, bundle_files_for_upload(), description)

                # Set upload date
                config.parser["Upload"]["last_date"] = str(int(time.time()))
                config.parser["Auth"]["gist_id"] = gist.id

                config.save_config()

                gist.edit(files=bundle_files_for_upload())
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
                config.save_config()
            sys.exit(1)

    def download(self):
        """Download history and config file from Gist"""

        try:
            print(constants.AUTH_MESSAGE)
            token = str(input(constants.TOKEN_INPUT))
            gist_id = str(input(constants.GIST_ID_INPUT))
            config.github = Github(token)

            # Exit process if not logged in
            if not config.is_logged_in():
                sys.exit(1)

            spinner = Spinner.NewTask("Downloading ...")

            # Download Gist object
            gist = config.github.get_gist(gist_id)

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

            config.parser["Auth"]["token"] = token
            config.parser["Auth"]["gist_id"] = gist_id
            config.save_config()

            history_file = config.get_shell_history()
            history_content = history_file["content"]

            new_changes = gist.files[
                constants.SUPPORTED_SHELLS[config.parser["Shell"]["name"]]
            ]

            synced_changes = new_changes.content + history_content

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

            config.write_shell_history(sort_proc.stdout.decode("utf-8"))
            spinner.succeed("Gist downloaded and stored.")
        except KeyboardInterrupt:
            sys.exit(0)
        except FileNotFoundError:
            spinner.fail("Couldn't find history file.")
            sys.exit(1)
        except OSError:
            sys.exit(1)


def main():
    Fire(Application)
