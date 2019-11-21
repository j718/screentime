#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `screentime` package."""


# from click.testing import CliRunner

from screentime.app import Screentime, HOME, MODULE_NAME
import requests
# from screentime import cli
import os
from pathlib import Path


def test_setUp():
    """Set up test fixtures, if any."""
    Screentime()


def tearDown():
    """Tear down test fixtures, if any."""


def test_environment():
    """Check that files are first in path"""
    desktop_path = os.environ["HOME"] + "/.config/screentime/share"
    bin_path = os.environ["HOME"] + "/.config/screentime/bin"
    assert desktop_path in os.environ['XDG_DATA_DIRS'].split(':')[0]
    assert bin_path in os.environ['PATH'].split(':')[0]

# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output


def test_config():
    """ ensure that all config folders exist """
    base = Path(os.environ['HOME']) / ".config/screentime"
    assert base.exists()
    assert (base / "bin").exists()
    assert (base / "share/applications").exists()
    assert (base / "config.yml").exists()


def test_profile():
    """ test that export statements are in profile """
    profile_paths = [
        Path("/etc/.profile"),
        HOME / ".bash_profile",
        HOME / ".profile"]
    user_profile = ""
    for profile in profile_paths:
        if os.path.isfile(profile):
            user_profile = profile
    assert user_profile
    profile = user_profile.read_text()
    export_str = "export XDG_DATA_DIRS="\
                 f"~/.config/{MODULE_NAME}/share:$XDG_DATA_DIRS"
    assert export_str in profile
    export_str = f"export PATH=~/.config/{MODULE_NAME}/bin:$PATH"
    assert export_str in profile


def test_api():
    root_url = "http://localhost:5600/api/"
    try:
        r = requests.get(root_url + "0/buckets")
    except requests.exceptions.RequestException as e:
        print(e)
        assert False
    assert r.ok

    bucket = [item for item in requests.get(root_url + "0/buckets").json()
              if 'aw-watcher-window' in item][0]

    # get today's history
    history_url = root_url + f"0/buckets/{bucket}/events"
    try:
        r = requests.get(history_url)
    except requests.exceptions.RequestException as e:
        print(e)
        assert False
    assert r.ok

# test that delete happens when app closes
# ensure that limit turns off on new day
# ensure that app is closed when killing it
