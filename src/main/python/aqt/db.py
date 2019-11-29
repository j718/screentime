import sqlite3
from pathlib import Path
# TODO add testing mode to cli.py
# TODO change timer to make requests to database
# TODO change preferences to make requests to database


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
        print("Closed connection")
        # TODO add logger to appctxt

    def init_db(self):
        self.init_connection()
        with open(self.appctxt.get_resource('schema.sql')) as f:
            self.connection.executescript(f.read())
