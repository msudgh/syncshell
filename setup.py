#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup

try:
    from version import __version__
except RuntimeError:
    raise RuntimeError("Unable to find version string.")
    sys.exit(1)


with open("README.md") as file:
    long_description = file.read()


setup(
    name="syncshell",
    packages=["syncshell"],
    entry_points={"console_scripts": ["syncshell = syncshell.__main__:main"]},
    version=__version__,
    description="Keep your machine's shell history synchronize",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Masoud Ghorbani",
    author_email="masoudghorbani@pm.me",
    maintainer="Masoud Ghorbani",
    maintainer_email="masoudghorbani@pm.me",
    url="https://github.com/msudgh/syncshell",
    project_urls={
        "Bug Reports": "https://github.com/msudgh/syncshell/issues",
        "Source": "https://github.com/msudgh/syncshell",
    },
    install_requires=["pygithub", "halo", "fire"],
    keywords="sync shell history bash zsh",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: System :: Shells",
        "Topic :: Software Development",
    ],
    python_requires=">=3.8.16",
)
