import yaml
import pandas as pd
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout, QGroupBox, QLabel, QPushButton, QFormLayout
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QCheckBox, QWidget
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import os
from pathlib import Path
from aqt import deleter, app

# get all data dris removing duplicates and checking if they exist

class Preferences(QtWidgets.QDialog):
    def __init__(self, appctxt, group=None):
        super().__init__()
        self.appctxt = appctxt
        self.con = self.appctxt.db.connection
        uic.loadUi(appctxt.get_resource("preferences.ui"), self)
        self.setWindowTitle("Preferences - Screentime")

        self.config = self.appctxt.get_config()
        self.group = group
        if self.group:
            # add time limit to limit group line edit
            query = f"""
    SELECT time_limit FROM limit_group WHERE title = '{self.group}';
    """
            limit = [x for x, in self.appctxt.db.connection.execute(query)][0]
            self.time_limit.setText(str(limit))

            # get a list of apps for group
            self.apps = self.config[self.config['title'] == group].app.str.lower().tolist()

        self.draw_list()
        self.accept_button.clicked.connect(self.accept)
        self.delete_button.clicked.connect(self.delete)
        self.search_bar.textChanged.connect(self.filter_search_bar)
        self.newapp_button.clicked.connect(self.create_app)

    # TODO make added time persist between updates
    # TODO make sure that time is only increased in group that ran out for app
    def draw_list(self):
        # remove all buttons
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)
        # redraw
        for app in self.get_apps():
            cb = QCheckBox(app, self)
            if self.group:
                if app.lower() in self.apps:
                    cb.setChecked(True)
            self.formLayout.addWidget(cb)

    def create_app(self):
        dialog = app.App(self.appctxt)
        if dialog.exec_():
            if dialog.add_current_check.isChecked():
                self.apps.append(dialog.app_lineEdit.text())
            self.draw_list()
                # (cb.setChecked(True)
                #     for cb in
                #     [self.formLayout.itemAt(i).widget() for i in range(self.formLayout.count())]
                #     if cb.text() == dialog.app_lineEdit.text())

    def filter_search_bar(self):
        filter = self.search_bar.text().lower()

        for i in range(self.formLayout.count()):
            box = self.formLayout.itemAt(i).widget()
            if filter.lower() in box.text().lower():
                box.show()
            else:
                box.hide()

# TODO update schema to delete apps limit_items when a group is deleted
# TODO make a way to manage apps
# TODO give multiple properties to apps
# TODO update connection approach
    def get_apps(self):
        query = """
select title from app
"""
        apps = [app for app, in self.con.execute(query)]
        return apps

            # TODO add time limit to dashboard widget ubttons

    def remove_group(self):
        if self.group:
            query = f"""
    DELETE FROM limit_group
    WHERE title = '{self.group}';
    """
            self.con.execute(query)
            self.con.commit()
        self.done(1)

    def delete(self):
        dialog = deleter.Delete(self.appctxt)
        if dialog.exec_():
            self.remove_group()

    def accept(self):
        """
        invoked by clicking the add time button on the dialog.

        """
        # returns app name of all checked boxes
        boxes = ([self.formLayout.itemAt(i).widget().text()
                  for i in range(self.formLayout.count())
                  if self.formLayout.itemAt(i).widget().isChecked()]
        )

        # get limit
        limit = self.time_limit.text()

        # create new group title
        name_limit = 3 if len(boxes) >= 3 else len(boxes)
        if name_limit < len(boxes):
            title = ", ".join(boxes[:2]) + f" and {len(boxes) - name_limit} others."
        else:
            title = ", ".join(boxes)

        # get and update or create limit group
        if not self.group:
            # add new group to database
            query = f"""
INSERT INTO limit_group (title, time_limit)
VALUES ('{title}', {limit});
"""
            self.con.execute(query)
            self.con.commit()

            # get id of the new group
            query = """
SELECT last_insert_rowid() FROM limit_group;
"""
            group_id = self.con.execute(query).lastrowid
        else:
            # get group id
            query = f"""
SELECT id FROM limit_group WHERE title = '{self.group}';
"""
            group_id = [x for x, in self.appctxt.db.connection.execute(query)][0]

            # update group time
            query = f"""
UPDATE limit_group
SET time_limit = {limit}, title = '{title}'
WHERE id = {group_id};
"""
            self.con.execute(query)
            self.con.commit()

        # add new apps to db
        for app in boxes:
            query = f"""
INSERT OR IGNORE INTO app (title) VALUES('{app}');
"""
            self.con.execute(query)
            self.con.commit()

        # get ids of apps for group
        boxes_sql = ', '.join([f"'{x.lower()}'" for x in boxes])
        query = f"""
SELECT
    ID
FROM
    APP
WHERE
    lower(title) in ({boxes_sql})

    """
        response = self.con.execute(query).fetchall()
        app_ids = [x for x, in response]

        # remove then add ids to lookup table
        query = f"""
DELETE FROM limit_item
WHERE limit_group_id = {group_id};
"""
        self.con.execute(query)
        self.con.commit()

        for app_id in app_ids:
            query = f"""
INSERT OR IGNORE INTO limit_item (app_id, limit_group_id)
VALUES ('{app_id}','{group_id}')
"""
            self.con.execute(query)
            self.con.commit()
        self.done(1)
