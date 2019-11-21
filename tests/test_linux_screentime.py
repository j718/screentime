#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `screentime` package."""


# from click.testing import CliRunner

from screentime.app import Screentime
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


# test that environment variable is set
# test that config folder is created
# test that export line is in profile
# test that api endpoints still exist
# test that path variable is correct
# test that delete happens when app closes
# ensure that limit turns off on new day
# ensure that app is closed when killing it
# check that correct bin exist
