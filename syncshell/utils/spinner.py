#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from halo import Halo


class NewTask:
    """Spinner New Task class wrapper around Halo"""

    __spinner = None

    def __init__(self, text, spinner="dots"):
        self.__spinner = Halo(text=text, spinner=spinner)
        self.__spinner.start()

    def succeed(self, text):
        """Override Halo succeed method"""
        self.__spinner.succeed(text)
        self.__spinner.stop()

    def fail(self, text):
        """Override Halo fail method"""
        self.__spinner.fail(text)
        self.__spinner.stop()
