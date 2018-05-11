<h1 align="center">SyncShell</h1>

<div align="center">
  <strong>Yet another tool for laziness</strong>
</div>
<div align="center">
  Keep your machine's shell history synchronize
</div>
<br/>
<div align="center">
  <!-- Build Status -->
  <a href="https://travis-ci.org/msudgh/syncshell">
    <img src="https://img.shields.io/travis/msudgh/syncshell/master.svg?style=flat"
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
Type:        Syncshell
String form: <syncshell.syncshell.Syncshell object at 0x7fa35d7d87f0>

Usage:       syncshell 
             syncshell auth
             syncshell download
             syncshell upload
```

## How it Works
The actual idea of SyncShell is synchronization of your devices shell history, Almost, this ability will be useful when you want to sync your office and home machines. SyncShell is just built on Github `Gist` feature such that this CLI tool represents three methods to communicate with the tool.

According to Github API, you can create a token key by set `gist` scope to accessing to your gists. gists have two **`public`**, **`secret`** type that on executing `syncshell upload` command will use secret type to store your history file and keep them secret on Github Gist.

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
- [ ] Support `bash` and other shells

## Contributing
So nice you wanna contribute to this repository. Thank you. You may contribute in several ways like:

  * Creating new features
  * Fixing bugs
  * Write test cases

#### Installing dependencies
By the following command install syncshell dependencies
```bash
$ python install -r requirements.txt
```

#### Tests
Before submiting your PR by running the below command to be sure about passing test cases.
```bash
$ pytest -c pytest.ini -s
```

Done :wink:

## License
The code is licensed under the MIT License. See the data's [LICENSE](https://github.com/msudgh/syncshell/blob/master/LICENSE) file for more information.
