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


xdg_path = [Path(x) for x in os.environ['XDG_DATA_DIRS'].split(':')]
MODULE_NAME = 'linux_screentime'
HOME = Path(os.environ['HOME'])
home_dir = Path(HOME / '.config' / MODULE_NAME)
share_dir = home_dir / 'share'
app_dir = share_dir / 'applications'



class Screentime():
    def __init__(self):
        # create config folder
        shutil.rmtree(app_dir, ignore_errors=True)
        app_dir.mkdir(parents=True, exist_ok=True)

        # manage config file
        config_path = home_dir / "config.yml"
        if not config_path.exists():
            config_path.touch()
        df = json_normalize(yaml.safe_load(config_path.open()))
        df.columns = ['id', 'limit']
        df = df.astype({"id": str, "limit": int})
        df["blocked"] = False
        self.config = df

        # find the profile folder
        profile_paths = [Path("/etc/.profile"), HOME / ".bash_profile", HOME / ".profile"]
        user_profile = ""
        for profile in profile_paths:
            if os.path.isfile(profile):
                user_profile = profile
        assert user_profile

        # ensure that config is in XDG DATA DIRS
        export_str = "export XDG_DATA_DIRS=~/.config/activitytime/share:$XDG_DATA_DIRS"
        if not share_dir in xdg_path:
            os.environ["XDG_DATA_DIRS"] = f'{share_dir}:{os.environ["XDG_DATA_DIRS"]}'
            with open(user_profile, "a") as f:
                f.write("\n"+export_str)


    def create_app(self, app_name:str):
        """ creates a fake desktop app"""
        sample_desktop = f"""#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Terminal=false
Type=Application
Name={app_name}
Exec=notify-send "limit for the day has been reached"
Icon=error"""
        file_path = app_dir / (app_name + ".desktop")
        print(f"blocked {app_name}")
        file_path.touch()
        file_path.write_text(sample_desktop)


    def get_times(self):
        root_url = "http://localhost:5600/api/"

        # check if api is up
        assert requests.get(root_url).ok

        # retrieve pertinent bucket
        bucket = [item for item in requests.get(root_url + "0/buckets").json() if 'aw-watcher-window' in item][0]

        # get today's history
        history = [item
                    for item in requests.get(root_url + f"0/buckets/{bucket}/events").json()
                    if parse(item["timestamp"]).date() == datetime.today().date()]

        # get todays apps and sum duration
        df = json_normalize(history).groupby("data.app").sum()[['duration']].reset_index()
        df.columns = ['id', 'duration']
        df = df.astype({"id": str, "duration": int})
        return df

    def apply_limits(self):
        df = self.get_times()
        restricted = pd.DataFrame.merge(self.config, df, how="left")
        blocked = restricted[(restricted.limit < restricted.duration) & (self.config.blocked == 0)]["id"]
        self.config.loc[restricted.limit < restricted.duration, "blocked"] = True

        for x in blocked:
            self.create_app(x.lower())



def main():
    app = Screentime()
    while True:
        app.apply_limits()
        time.sleep(10)

if __name__ == "__main__":
    main()
