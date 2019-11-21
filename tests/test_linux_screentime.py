#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `linux_screentime` package."""


import unittest
from click.testing import CliRunner

from linux_screentime import linux_screentime
from linux_screentime import cli


class TestLinux_screentime(unittest.TestCase):
    """Tests for `linux_screentime` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'linux_screentime.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

# test that environment variable is set
# test that config folder is created
# test that export line is in profile
# test that api endpoints still exist
