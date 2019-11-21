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


def test_config():
    """ ensure that all config folders exist """
    base = Path(os.environ['HOME']) / ".config/screentime"
    assert base.exists()
    assert (base / "bin").exists()
    assert (base / "share/applications").exists()
    assert (base / "config.yml").exists()


def test_api():
    """ test that api still works """
    root_url = "http://localhost:5600/api/"
    try:
        r = requests.get(root_url + "0/buckets")
    except requests.exceptions.RequestException as e:
        print(e)
        assert False
    assert r.ok


# test that delete happens when app closes
# ensure that limit turns off on new day
# ensure that app is closed when killing it
