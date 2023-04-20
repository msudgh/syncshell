<h1 align="center">SyncShell</h1>

<div align="center">
  <strong>Yet another tool for laziness</strong>
</div>
<div align="center">
  Keep your machine's shell history synchronized
</div>
<br/>
<div align="center">
  <!-- Build Status -->
  <a href="https://github.com/msudgh/syncshell/actions/workflows/test.yaml">
    <img src="https://github.com/msudgh/syncshell/actions/workflows/test.yaml/badge.svg?branch=main"
      alt="Build Status" />
  </a>
  <!-- License -->
  <a href="https://mit-license.org/msudgh">
    <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg"
      alt="MIT License" />
  </a>
  <!-- Release -->
  <a href="https://github.com/msudgh/syncshell/releases">
    <img src="https://img.shields.io/github/release/msudgh/syncshell.svg"
      alt="PyPi" />
  </a>
  <!-- PyPi -->
  <a href="https://pypi.org/project/syncshell/">
    <img src="https://img.shields.io/pypi/v/syncshell.svg"
      alt="PyPi" />
  </a>
</div>
<br/>

## Get SyncShell
Currently, `SyncShell` is just available on `PyPi` and by the following command install the latest version:
```bash
$ pip install syncshell # Maybe sudo need
```
```bash
$ syncshell -- --help
Type:        Application
String form: <syncshell.cli.Application object at 0x1035f51c0>
Docstring:   SyncShell CLI Application

Usage:       syncshell 
             syncshell auth
             syncshell download
             syncshell upload
```

## How it Works
The actual idea of SyncShell is synchronization of your all device's shell history, it means you don't need to have concerns when you want to sync your office and home machine's shell history. Application integrated and built on top of Github Gist, and written in Python (CLI).

According to Github API, you can generate a token key with `gist` scope to access to Gist. 
Gists have two **`public`**, **`secret`** type which syncshell while executing `syncshell upload` command will upload your history file and store them on Github Gist securely (**private**).

On the others machine, by executing `syncshell download` after entering your token key and created Gist ID you can download the gist and sync your shell's history.

  > Gists will be secret until you don't share it with someone else, In other words, It'll be secret and safe until you only have the Github Token and Gist ID.

## Usage
  > Currently, `SyncShell` just support `zsh` and supporting other shells is in WIP.

Before SyncShell can be useful you need to setup your Github token key:

  1. Open [**Github personal access tokens**](https://github.com/settings/tokens) page, [**Generate a new token**](https://github.com/settings/tokens/new) with `gist` scope feature.
  2. Execute the **`syncshell auth`** command, Enter your token key to validate and confirm it.
  3. Done :wink:

Now you can try to upload your shell history by the following command:

```bash
$ syncshell upload
```

After the uploading process, you'll take a Gist ID that by this ID and your Github token, you can download history on the others machine by executing the following command:
```bash
$ syncshell download
```

## Todo
- [ ] Write more test cases
- [x] Support `zsh`, `bash`

## Contributing
Appreciate the contribution to this repository.

To contribute, you need to follow the below steps for suggesting a change or a new feature:

### Installing dependencies

1. Install [poetry](https://python-poetry.org/docs/#installation) as a dependency manager
2. Install dependencies

```bash
$ poetry install
```

### Running

```bash
$ poetry run python syncshell
# or
$ python syncshell
```

### Tests
Before submit a PR, execute the below command to ensure test cases are passed.
```bash
$ poetry run pytest -c pytest.ini -s
```

Done :wink:

## License
The code is licensed under the MIT License. See the data's [LICENSE](https://github.com/msudgh/syncshell/blob/main/LICENSE) file for more information.
