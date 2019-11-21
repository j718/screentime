# -*- coding: utf-8 -*-

"""Main module."""
import os
import signal
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
log_path = (home_dir / 'log.txt')


class Screentime():
    def __init__(self):
        self.MODULE_NAME = MODULE_NAME
        # create config folder

        self.logger = self.setup_custom_logger(MODULE_NAME)

        # manage config file
        config_path = home_dir / "config.yml"
        if not config_path.exists():
            config_path.touch()
        config_file = yaml.safe_load(config_path.open())
        if config_file:
            df = json_normalize(config_file)
        else:
            self.logger.warning("Config file is empty")
            df = pd.DataFrame(columns=['id', 'limit'])
        df.columns = ['id', 'limit']
        df = df.astype({"id": str, "limit": int})
        df.id = df.id.str.lower()
        df["blocked"] = False
        self.config = df

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
        """ closes blocked apps """
        if app_name in str(subprocess.check_output(['ps', 'aux'])):
            self.logger.info(f"Killed {app_name}")
            subprocess.call(['notify-send', f'Closing {app_name}. Limit already reached'])
            subprocess.Popen(["pkill", "-HUP", app_name], bufsize=0)

        # kill app

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
            (restricted.limit < restricted.duration)
        )]["id"]

        for x in blocked:
            self.block_app(x.lower())


def main():
    app = Screentime()
    while True:
        app.apply_limits()
        time.sleep(10)


if __name__ == "__main__":
    main()
