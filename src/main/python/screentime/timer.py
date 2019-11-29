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
        self.root_url = "http://localhost:5600/api/"
        assert requests.get(self.root_url).ok
        self.con = appctxt.db
        self.bucket = [item for item in requests.get(self.root_url + "0/buckets").json()
                  if 'aw-watcher-window' in item][0]

        self.today = datetime.today().date()
        self.update_config()
        print("Successfully Initialized")

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
        restricted = pd.DataFrame.merge(self.config, df_times, how="left")
        print(restricted)
        blocked = restricted[(
            (restricted.time_limit <= restricted.duration)
        )][["app", "time_limit"]]
        return blocked
        # TODO update config file and timer format to have groups with lists of apps

    def increase_limit(self, app_name):
        df = self.get_times()
        duration_dict = df.set_index('app').to_dict()
        duration = duration_dict['duration'][app_name]
        new_limit = duration + 15
        self.config.loc[self.config['app'] == app_name, 'time_limit'] = new_limit
        print(f"Adding 15 minutes to {app_name}."
              f"The new limit is {new_limit} min.")

    def update_config(self):
        query = """
SELECT
    LIMIT_GROUP.TITLE,
    LIMIT_GROUP.TIME_LIMIT as time_limit,
    APP.TITLE AS app
FROM
    LIMIT_GROUP
JOIN LIMIT_ITEM ON
    LIMIT_GROUP.ID = LIMIT_ITEM.LIMIT_GROUP_ID
JOIN APP ON
    APP.ID = LIMIT_ITEM.APP_ID"""
        self.config = pd.read_sql_query(query, self.con)
        self.config.app = self.config.app.str.lower()
