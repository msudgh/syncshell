#!/usr/bin/env python3

import pytest
from unittest.mock import patch
from syncshell.utils.config import SyncShellConfig
from syncshell.utils import constants
import os
from configparser import ConfigParser

temp_history_file_path = "/tmp/.zsh_history"
sample_config = "[Auth]\ntoken=my_token\n\n[Shell]\nname=zsh\npath={}\n\n".format(
    temp_history_file_path
)


@pytest.fixture
def config_path():
    # Create a temporary config file
    config_file_path = "/tmp/{}".format(constants.CONFIG_FILENAME)
    with open(config_file_path, "w") as file:
        file.write(sample_config)

    # Create a temporary zsh history file
    with open(temp_history_file_path, "w") as file:
        file.write("")

    yield config_file_path

    # Clean up the temporary config file after the test
    os.remove(config_file_path)
    os.remove(temp_history_file_path)


def test_read_config(config_path, monkeypatch):
    config = SyncShellConfig(path=config_path)

    assert config.read_config() is True
    assert config.github is not None


def test_save_config(config_path):
    config = SyncShellConfig(path=config_path)

    assert config.save_config() is True


def test_is_logged_in(config_path):
    config = SyncShellConfig(path=config_path)
    config.read_config()

    # Mock the Github get_user method
    with patch.object(config.github, "get_user") as mock_get_user:
        # User exists in config file
        mock_get_user.return_value.login = "my_username"
        assert config.is_logged_in() is True

        # User does not exist in config file
        mock_get_user.return_value.login = ""
        assert config.is_logged_in() is False


def test_get_shell_history(config_path):
    config = SyncShellConfig(path=config_path)
    config.read_config()

    result = config.get_shell_history()

    assert result["path"] == ".zsh_history"


def test_write_shell_history(config_path):
    config = SyncShellConfig(path=config_path)
    config.read_config()

    assert config.write_shell_history("New shell history content")


def test_get_config(config_path):
    config = SyncShellConfig(path=config_path)
    config.read_config()

    result = config.get_config()

    assert result["path"] == ".syncshell.ini"


def test_get_config_without_token(config_path):
    config = SyncShellConfig(path=config_path)
    config.read_config()

    result = config.get_config()

    new_config = ConfigParser()
    new_config.read_string(result["content"])
    assert "token" not in new_config["Auth"]
