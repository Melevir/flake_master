# flake_master

[![Build Status](https://travis-ci.org/Melevir/flake_master.svg?branch=master)](https://travis-ci.org/Melevir/flake_master)
[![Maintainability](https://api.codeclimate.com/v1/badges/f69de0bcd500a0548840/maintainability)](https://codeclimate.com/github/Melevir/flake_master/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f69de0bcd500a0548840/test_coverage)](https://codeclimate.com/github/Melevir/flake_master/test_coverage)
[![PyPI version](https://badge.fury.io/py/flake-master.svg)](https://badge.fury.io/py/flake-master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake-master)

flake_master is a manager for flake8 plugins and configuration.

If you have multiple projects with rich flake8 setup, you
know how painful it could be to keep flake8 setup in
all projects up to date and synced.
This is what flake master does.

This library is inspired by eslint and does pretty much the same
as nitpick or flakehell. I need simple tool that helps with
flake8 configuration management. Also I'm bored.

## Installation

```terminal
pip install flake_master
```

## Usage

Flake master can help with flake8 set setup and upgrade.

### Setup

```terminal
flake_master setup <preset name or path> <dir to do the setup>
```

This will do the following:

- download preset with all plugins versions and project setup (from Github);
- add required packages to `requirements.txt`;
- add plugins configuration to `setup.cfg`;
- create `.flake_master` file with current preset version
  (add the file to vsc).

### Upgrade

```terminal
flake_master upgrade <dir with .flake_master>
```

This command will fetch last version of preset from `.flake_master` and apply
it to `requirements.txt` and `setup.py`.

Beware, it can overwrite some data, that was updated by `flake_master` and
then manually updated.

## Contributing

We would love you to contribute to our project. It's simple:

- Create an issue with bug you found or proposal you have.
  Wait for approve from maintainer.
- Create a pull request. Make sure all checks are green.
- Fix review comments if any.
- Be awesome.

Here are useful tips:

- You can run all checks and tests with `make check`. Please do it
  before TravisCI does.
- We use
  [BestDoctor python styleguide](https://github.com/best-doctor/guides/blob/master/guides/en/python_styleguide.md).
- We respect [Django CoC](https://www.djangoproject.com/conduct/).
  Make soft, not bullshit.
