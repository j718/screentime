# -*- coding: utf-8 -*-

"""Main module."""
import yaml
import requests
from datetime import datetime
from dateutil.parser import parse
from pandas.io.json import json_normalize
import pandas as pd


class Screentime():
    def __init__(self, appctxt):
        self.appctxt = appctxt
        self.root_url = "http://localhost:5600/api/"
        self.con = appctxt.db.connection
        self.bucket = [item for item in requests.get(self.root_url + "0/buckets").json()
                  if 'aw-watcher-window' in item][0]

        self.today = datetime.today().date()
        self.appctxt.logger.info("Successfully Initialized")

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
        df.columns = ['app', 'duration']
        df.duration /= 60
        df = df.astype({"app": str, "duration": int})
        df.app = df.app.str.lower()
        return df

    def apply_limits(self):
        # manage config file
        df_times = self.get_times()
        df_master = pd.DataFrame.merge(self.appctxt.config, df_times, how="left")
        df_groups = (df_master
                    .groupby(["title"]).agg(
                        duration=('duration', 'sum'),
                        time_limit=('time_limit', 'max')
                    )
                    .reset_index()
                    .merge(self.appctxt.config[['title', 'app']], how='left')
                    )

        df_groups = df_groups[df_groups.time_limit <= df_groups.duration]
        return df_groups

# TODO add ability to increase time limit

