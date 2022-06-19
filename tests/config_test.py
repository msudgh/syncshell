#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# config_test.py: unit tests of config class

import pytest
import syncshell.constants as constants
from syncshell.config import Config


@pytest.mark.config
def test_initialization():
    """Check the configuration path"""
    config = Config()

    assert config.path == constants.CONFIG_PATH


@pytest.mark.config
def test_reading_configuration():
    """Check reading configuration from path is successful"""
    config = Config()

    assert config.read()


@pytest.mark.config
def test_writing_configuration():
    """Check writing configuration from modified config to
    file is successful.

    """
    config = Config(constants.CONFIG_PATH_TEMPLATE)
    config.read()
    temp_file_path = "/tmp/{}".format(constants.CONFIG_FILENAME)

    # Write config file as temporary
    config.write(temp_file_path)

    # Mody config
    config.parser["Auth"]["token"] = "TEST"

    # assert writing
    assert config.write()

    # assert values
    assert config.parser["Auth"]["Token"] == "TEST"
