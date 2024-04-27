# SyncShell
<!-- License -->
<a href="https://mit-license.org/msudgh">
  <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg"
    alt="MIT License" />
</a>
<!-- Releases -->
<a href="https://github.com/msudgh/syncshell/releases">
  <img src="https://img.shields.io/github/release/msudgh/syncshell.svg"
    alt="PyPi" />
</a>
<!-- PyPi -->
<a href="https://pypi.org/project/syncshell/">
  <img src="https://img.shields.io/pypi/v/syncshell.svg"
    alt="PyPi" />
</a>

SyncShell as a simple and secure tool allows to synchronize machine's shell history across devices. It's built on top of Github Gist and written in Python (CLI). With SyncShell, you no longer have to worry about manually syncing your office and home machine's shell history and let continue where the terminal session left.

## Features

- Sync your shell history across all your devices
- Securely store your shell history on Github Gist
- Support for `zsh` and `bash` shells
- Easy to install and use

## Installation
To install SyncShell, simply run the following command:

```bash
$ pip install syncshell
```

## Usage
To use SyncShell, It first needs to set up a Github token key by following these steps:

1. Open [**Github personal access tokens**](https://github.com/settings/tokens) page, [**Generate a new token**](https://github.com/settings/tokens/new) with `gist` scope feature.
2. Execute the **`syncshell auth`** command, Enter the token key to validate and confirm it.

Once finished, try to upload shell history by the following command:

```bash
$ syncshell upload
```

After uploading, the download command lets to sync and pull changes on the other machines:

```bash
$ syncshell download
```


### Synopsis

```bash
$ syncshell
Type:        Application
String form: <syncshell.cli.Application object at 0x101b1ff10>
Docstring:   SyncShell CLI Application

Usage:       syncshell
             syncshell auth
             syncshell download
             syncshell upload
```

## How it Works

SyncShell is a tool that synchronizes shell history across all devices by securely storing the history file on Github Gist. Github Gist provides two types of Gists, `public` and `secret`. When the `syncshell upload` command is executed, the shell history file is uploaded and stored securely on Github Gist as a secret Gist. To download the uploaded shell history on other devices, the `syncshell download` command is used. This command retrieves the previously uploaded Gist, allowing the user to access their shell history on any device.

**Security:** A Gist will be secret until it's not shared and will be secret and safe until you only have the Github Token and Gist ID.

**Privacy:** In case of having password or secret in a history file, Its suggested to first have a alignment with privacy policies for any usecase.

## Contributing

I would love to have your help in making SyncShell idea better and expand it capabilities.

### Branching

- `main` is being used for the latest development version.
- `release` is being used for the latest stable version.


### Pull Requests
To contribute follow the below steps:

1. Install [poetry](https://python-poetry.org/docs/#installation) as a dependency manager
2. Install dependencies by running ```poetry shell && poetry install```
3. Make your changes
4. Run and debug your changes by running ```poetry run python syncshell```
5. Run tests by running ```poetry run pytest -c pytest.ini -s```
6. Submit a pull request

## License
The code is licensed under the MIT License. See the data's [LICENSE](https://github.com/msudgh/syncshell/blob/main/LICENSE) file for more information.
