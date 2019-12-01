import sqlite3
from pathlib import Path
import pandas as pd


class Database():
    def __init__(self, appctxt):
        self.appctxt = appctxt
        self.flagConnOpen = False
        self.db_path = Path(appctxt.db_path)
        if not self.db_path.exists():
            self.init_db()
        self.init_connection()

    def init_connection(self):
        if not self.flagConnOpen:
            self.flagConnOpen = True
            connection = sqlite3.connect(
                str(self.db_path)
            )
            self.connection = connection

    def close_db(self):
        if self.flagConnOpen:
            self.connection.close()
            self.flagConnOpen = False
        self.appcxt.logger.info("Closed connection")

    def init_db(self):
        self.init_connection()
        with open(self.appctxt.get_resource('schema.sql')) as f:
            self.connection.executescript(f.read())

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
        config = pd.read_sql_query(query, self.connection)
        config.app = config.app.str.lower()
        self.appctxt.config = config
