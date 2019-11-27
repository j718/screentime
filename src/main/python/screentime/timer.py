# -*- coding: utf-8 -*-

"""Main module."""
import os
import yaml
import requests
from pathlib import Path
from datetime import datetime
from dateutil.parser import parse
from pandas.io.json import json_normalize
import pandas as pd

MAX_RESULTS = 1000

xdg_path = [Path(x) for x in os.environ['XDG_DATA_DIRS'].split(':')]
MODULE_NAME = 'screentime'
HOME = Path(os.environ['HOME'])
home_dir = Path(HOME / '.config' / MODULE_NAME)


class Screentime():
    def __init__(self):
        self.MODULE_NAME = MODULE_NAME
        self.root_url = "http://localhost:5600/api/"
        assert requests.get(self.root_url).ok
        self.bucket = [item for item in requests.get(self.root_url + "0/buckets").json()
                  if 'aw-watcher-window' in item][0]

        self.today = datetime.today().date()

        print("Successfully Initialized")

        config_path = home_dir / "config.yml"
        if not config_path.exists():
            config_path.touch()
        config_file = yaml.safe_load(config_path.open())
        if config_file:
            df_config = json_normalize(config_file)
        else:
            print("Config file is empty")
            df_config = pd.DataFrame(columns=['id', 'limit'])
        df_config.columns = ['id', 'limit']
        df_config = df_config.astype({"id": str, "limit": int})
        df_config.id = df_config.id.str.lower()
        self.config = df_config

    def get_times(self):
        # get today's history
        history_url = self.root_url + f"0/buckets/{self.bucket}/events"
        history = [item
                   for item
                   in requests.get(history_url).json()
                   if parse(item["timestamp"]).date() >= self.today]

        # get todays apps and sum duration
        df = (json_normalize(history)
              .groupby("data.app")
              .sum()[['duration']]
              .reset_index())
        df.columns = ['id', 'duration']
        df.duration /= 60
        df = df.astype({"id": str, "duration": int})
        df.id = df.id.str.lower()
        return df

    def apply_limits(self):
        # manage config file
        df = self.get_times()
        restricted = pd.DataFrame.merge(self.config, df, how="left")
        blocked = restricted[(
            (restricted.limit < restricted.duration)
        )][["id", "limit"]]
        return blocked

    def increase_limit(self, app_name):
        df = self.get_times()
        duration_dict = df.set_index('id').to_dict()
        duration = duration_dict['duration'][app_name]
        new_limit = duration + 15
        self.config.loc[self.config['id'] == app_name, 'limit'] = new_limit
        print(f"Adding 15 minutes to {app_name}."
              f"The new limit is {new_limit} min.")
