# -*- coding: utf-8 -*-

"""Main module."""
import os
import yaml
import requests
from pathlib import Path
import subprocess
from datetime import datetime
from dateutil.parser import parse
import shutil
from pandas.io.json import json_normalize
import pandas as pd
import time
import logging
import sys

MAX_RESULTS = 1000

xdg_path = [Path(x) for x in os.environ['XDG_DATA_DIRS'].split(':')]
MODULE_NAME = 'screentime'
HOME = Path(os.environ['HOME'])
home_dir = Path(HOME / '.config' / MODULE_NAME)
share_dir = home_dir / 'share'
bin_dir = home_dir / 'bin'
app_dir = share_dir / 'applications'
log_path = (home_dir / 'log.txt')


class Screentime():
    def __init__(self):
        self.MODULE_NAME = MODULE_NAME
        # create config folder
        shutil.rmtree(app_dir, ignore_errors=True)
        app_dir.mkdir(parents=True, exist_ok=True)

        shutil.rmtree(bin_dir, ignore_errors=True)
        bin_dir.mkdir(parents=True, exist_ok=True)

        self.logger = self.setup_custom_logger(MODULE_NAME)

        # manage config file
        config_path = home_dir / "config.yml"
        if not config_path.exists():
            config_path.touch()
        config_file = yaml.safe_load(config_path.open())
        if config_file:
            df = json_normalize(config_file)
        else:
            df = pd.DataFrame(columns=['id', 'limit'])
        df.columns = ['id', 'limit']
        df = df.astype({"id": str, "limit": int})
        df.id = df.id.str.lower()
        df["blocked"] = False
        self.config = df

        # find the profile folder
        profile_paths = [
            Path("/etc/.profile"),
            HOME / ".bash_profile",
            HOME / ".profile"]
        user_profile = ""
        for profile in profile_paths:
            if os.path.isfile(profile):
                user_profile = profile
        assert user_profile

        # ensure that config is in XDG DATA DIRS
        export_str = "export XDG_DATA_DIRS="\
            f"~/.config/{self.MODULE_NAME}/share:$XDG_DATA_DIRS"
        if share_dir not in xdg_path:
            os.environ["XDG_DATA_DIRS"] = \
                 f'{share_dir}:{os.environ["XDG_DATA_DIRS"]}'
            with open(user_profile, "a") as f:
                f.write("\n"+export_str)

        export_str = f"export PATH=~/.config/{self.MODULE_NAME}/bin:$PATH"
        if not str(bin_dir) in os.environ['PATH']:
            os.environ["PATH"] = f'{bin_dir}:{os.environ["PATH"]}'
            with open(user_profile, "a") as f:
                f.write("\n"+export_str)

        self.logger.info("Successfully Initialized")
        self.logger.info(f"PATH: {os.environ['PATH']}")
        self.logger.info(f"XDG_DATA_DIRS: {os.environ['XDG_DATA_DIRS']}")

    def setup_custom_logger(self, name):
        if not log_path.exists():
            log_path.touch()
        formatter = logging.Formatter(
                        fmt='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        handler = logging.FileHandler(home_dir / 'log.txt', mode='a')
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(screen_handler)
        return logger

    def block_app(self, app_name: str):
        """ creates a fake desktop app"""
        # overwrite desktop entry
        sample_desktop = f"""#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Terminal=false
Type=Application
Name={app_name}
Exec=notify-send "limit for the day has been reached"
Icon=error"""
        desktop_path = app_dir / (app_name + ".desktop")
        print(f"blocked {app_name}")
        desktop_path.touch()
        desktop_path.write_text(sample_desktop)

        # overwrite terminal command
        sample_bin = f"""#!/usr/bin/sh
echo "limit for the day has been reached"""
        bin_path = bin_dir / app_name
        bin_path.touch()
        bin_path.write_text(sample_bin)

        # kill app
        subprocess.Popen(["pkill", app_name], bufsize=0)

    def get_times(self):
        root_url = "http://localhost:5600/api/"

        # check if api is up
        assert requests.get(root_url).ok

        # retrieve pertinent bucket
        bucket = [item for item in requests.get(root_url + "0/buckets").json()
                  if 'aw-watcher-window' in item][0]

        # get today's history
        history_url = root_url + f"0/buckets/{bucket}/events"
        today = datetime.today().date()
        history = [item
                   for item
                   in requests.get(history_url).json()
                   if parse(item["timestamp"]).date() >= today]

        # get todays apps and sum duration
        df = (json_normalize(history)
              .groupby("data.app")
              .sum()[['duration']]
              .reset_index())
        df.columns = ['id', 'duration']
        df = df.astype({"id": str, "duration": int})
        df.id = df.id.str.lower()
        return df

    def apply_limits(self):
        df = self.get_times()
        restricted = pd.DataFrame.merge(self.config, df, how="left")
        blocked = restricted[(
            (restricted.limit < restricted.duration) &
            (self.config.blocked == 0)
        )]["id"]

        self.config.loc[(
            restricted.limit < restricted.duration, "blocked"
        )] = True

        for x in blocked:
            self.block_app(x.lower())


def main():
    app = Screentime()
    while True:
        app.apply_limits()
        time.sleep(10)


if __name__ == "__main__":
    main()
