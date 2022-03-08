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

class add_brand(QtWidgets.QDialog):
    def __init__(self):
        super(add_brand, self).__init__()
        uic.loadUi('add_brand.ui', self)
        self.setWindowTitle("Hardware Service Manager - Add Brand")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.brd_reset_btn.clicked.connect(self.reset)
        self.brd_save_btn.clicked.connect(self.save)
        self.show()

    def reset(self):
        self.brd_entry.clear()
        self.active.setChecked(True)

    def save(self):
        u = global_variable.USER_ID
        if self.active.isChecked():
            a = '1'
        else:
            a = '0'
        b = self.brd_entry.text()
        d = str(datetime.datetime.now())
        try:
            if u == "" or b == "" or d == "":
                raise Exception()
            else:
                global_variable.mycursor.execute("SELECT BrandId FROM brand WHERE BrandName = '"+b+"'")
                x = global_variable.mycursor.fetchone()
                if x is None:
                    sql = "INSERT INTO brand (BrandName, IsActive, CreatedDateTime, CreatedUserId, UpdatedUserId, UpdatedDateTime) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (b, a, d, u, u, d)
                    global_variable.mycursor.execute(sql, val)
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset()

                else:
                    QMessageBox.critical(self, "Error", "Brand already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")
