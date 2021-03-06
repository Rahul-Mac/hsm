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
        mydb = ""
        mycursor = ""
        super(add_brand, self).__init__()
        uic.loadUi('add_brand.ui', self)
        self.setWindowTitle("Hardware Service Manager - Add Brand")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.brd_reset_btn.clicked.connect(self.reset)
        self.brd_save_btn.clicked.connect(self.save)
        self.show()

    def open_db(self):
        add_brand.mydb = mysql.connector.connect(host = global_variable.SERVER, user = "root", password = "root", database = "servicemgmt")
        add_brand.mycursor = add_brand.mydb.cursor()

    def close_db(self):
        add_brand.mycursor.close()
        add_brand.mydb.close()

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
                self.open_db()
                add_brand.mycursor.execute("SELECT BrandId FROM brand WHERE BrandName = '"+b+"'")
                x = add_brand.mycursor.fetchone()
                self.close_db()
                if x is None:
                    sql = "INSERT INTO brand (BrandName, IsActive, CreatedDateTime, CreatedUserId, UpdatedUserId, UpdatedDateTime) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (b, a, d, u, u, d)
                    self.open_db()
                    add_brand.mycursor.execute(sql, val)
                    add_brand.mydb.commit()
                    self.close_db()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset()

                else:
                    QMessageBox.critical(self, "Error", "Brand already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")
