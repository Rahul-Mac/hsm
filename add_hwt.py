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

class add_hwt(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(add_hwt, self).__init__()
        uic.loadUi('add_hwt.ui', self)
        self.setWindowTitle("Hardware Service Manager - Add Hardware")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.hwt_reset_btn.clicked.connect(self.reset)
        self.hwt_save_btn.clicked.connect(self.save)
        self.show()

    def open_db(self):
        add_hwt.mydb = mysql.connector.connect(host = global_variable.SERVER, user = "root", password = "root", database = "servicemgmt")
        add_hwt.mycursor = add_hwt.mydb.cursor()

    def close_db(self):
        add_hwt.mycursor.close()
        add_hwt.mydb.close()

    def reset(self):
        self.hwt_entry.clear()
        self.hwt_active.setChecked(True)

    def save(self):
        h = self.hwt_entry.text()
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        if self.hwt_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if h == "" or d == "" or u == "" or a == "":
                raise Exception()
            else:
                self.open_db()
                add_hwt.mycursor.execute("SELECT HardwareId FROM hardwaretype WHERE HardwareName = '"+h+"'")
                x = add_hwt.mycursor.fetchone()
                self.close_db()
                if x is None:
                    sql = "INSERT INTO hardwaretype (HardwareName, CreatedDateTime, CreatedUserId, UpdatedDateTime, UpdatedUserId, IsActive) VALUES ('"+h+"', '"+d+"', '"+u+"', '"+d+"', '"+u+"', '"+a+"')"
                    self.open_db()
                    add_hwt.mycursor.execute(sql)
                    add_hwt.mydb.commit()
                    self.close_db()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset()
                else:
                    QMessageBox.critical(self, "Error", "Hardware already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")

