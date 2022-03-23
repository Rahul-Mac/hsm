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
import global_variable
import hashlib
import datetime
import sys

class reset_password(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(reset_password, self).__init__()
        uic.loadUi('reset_password.ui', self)
        self.setWindowTitle("Reset Password")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.save_btn.clicked.connect(self.save)
        self.user_id.model().item(0).setEnabled(False)
        self.get_users()
        self.show()

    def open_db(self):
        reset_password.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        reset_password.mycursor = reset_password.mydb.cursor()

    def close_db(self):
        reset_password.mycursor.close()
        reset_password.mydb.close()

    def get_users(self):
        self.open_db()
        reset_password.mycursor.execute("SELECT UserId FROM user;")
        data = reset_password.mycursor.fetchall()
        self.close_db()
        for d in data:
            self.user_id.addItem(d[0])

    def save(self):
        u = self.user_id.currentText()
        p = self.pswd.text()
        c = self.confirm.text()
        d = str(datetime.datetime.now())
        try:
            if p != c:
                QMessageBox.critical(self, "Error", "Passwords do not match")
            elif u == "" or p == "" or c == "" or d == "" or u == "-- Select --":
                QMessageBox.critical(self, "Error", "Empty field detected")
            elif len(p) < 6:
                QMessageBox.critical(self, "Error", "Password must be 6 characters long")
            else:
                p = hashlib.md5(p.encode('utf-8')).hexdigest()
                sql = "UPDATE user set UserPassword = '"+p+"', UpdatedDateTime = '"+d+"', UpdatedUserId = '"+global_variable.USER_ID+"' Where UserId = '"+u+"'"
                self.open_db()
                reset_password.mycursor.execute(sql)
                reset_password.mydb.commit()
                self.close_db()
                QMessageBox.information(self, "Message", "Password changed successfully!")
                self.close()
        except:
            QMessageBox.critical(self, "Error", "Failed to reset password")
