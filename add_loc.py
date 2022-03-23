'''
This file is part of Hardware Service Manager.

Hardware Service Manager is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.
Hardware Service Manager is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Hardware Service Manager.
If not, see <https://www.gnu.org/licenses/>.
'''

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QApplication, QCompleter
import mysql.connector
import datetime
import global_variable
import hashlib
import sys

class add_loc(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(add_loc, self).__init__()
        uic.loadUi('add_loc.ui', self)
        self.setWindowTitle("Hardware Service Manager - Add Location")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.flr_combo.model().item(0).setEnabled(False)
        self.wing_combo.model().item(0).setEnabled(False)
        self.loc_reset_btn.clicked.connect(self.reset_loc)
        self.loc_save_btn.clicked.connect(self.save_loc)
        self.show()

    def open_db(self):
        add_loc.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        add_loc.mycursor = add_loc.mydb.cursor()

    def close_db(self):
        add_loc.mycursor.close()
        add_loc.mydb.close()

    def save_loc(self):
        l = self.loc_entry.text()
        f = self.flr_combo.currentText()
        w = self.wing_combo.currentText()
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        if self.loc_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if l == "" or f == "" or d == "" or u == "" or  f == "-- Select --" or a == "":
                raise Exception()
            else:
                if w == "-- Select --":
                    w = ''
                self.open_db()
                add_loc.mycursor.execute("SELECT LocationId FROM location WHERE LocationName = '"+l+"'")
                x = add_loc.mycursor.fetchone()
                self.close_db()
                if x is None:
                    sql = "INSERT INTO location (LocationName, Floor, Wing, CreatedDateTime, CreatedUserId, UpdatedDateTime, UpdatedUserId, IsActive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    val = (l, f, w, d, u, d, u, a)
                    self.open_db()
                    add_loc.mycursor.execute(sql, val)
                    add_loc.mydb.commit()
                    self.close_db()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset_loc()
                else:
                    QMessageBox.critical(self, "Error", "Location Name already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")

    def reset_loc(self):
        self.loc_entry.clear()
        self.flr_combo.setCurrentText("-- Select --")
        self.wing_combo.setCurrentText("-- Select --")
        self.loc_active.setChecked(True)
