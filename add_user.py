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

class add_user(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(add_user, self).__init__()
        uic.loadUi('add_user.ui', self)
        self.setWindowTitle("Hardware Service Manager - Add User")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.user_save_btn.clicked.connect(self.save)
        self.user_reset_btn.clicked.connect(self.reset)
        self.user_combo.model().item(0).setEnabled(False)
        self.show()

    def open_db(self):
        add_user.mydb = mysql.connector.connect(host = global_variable.SERVER, user = "root", password = "root", database = "servicemgmt")
        add_user.mycursor = add_user.mydb.cursor()

    def close_db(self):
        add_user.mycursor.close()
        add_user.mydb.close()

    def save(self):
        i = self.user_id.text()
        u = self.user_name.text()
        p = self.user_pass.text()
        e = self.emp_code.text()
        t = self.user_combo.currentText()
        d = str(datetime.datetime.now())
        if self.user_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if u == "" or p == "" or e == "" or t == "" or i == "" or t == "-- Select --" or a == "":
                raise Exception()
            elif len(p) < 6:
                QMessageBox.critical(self, "Error", "Password must be 6 characters long")
            else:
                self.open_db()
                add_user.mycursor.execute("SELECT UserIndex FROM user WHERE UserId = '"+i+"'")
                x = add_user.mycursor.fetchone()
                self.close_db()
                self.open_db()
                add_user.mycursor.execute("SELECT UserIndex FROM user WHERE EmployeeCode = '"+e+"'")
                y = add_user.mycursor.fetchone()
                self.close_db()
                p = hashlib.md5(p.encode('utf-8')).hexdigest()
                if x is None and y is None:
                    sql = "INSERT INTO user (UserId, UserName, UserType, CreatedDateTime, EmployeeCode, UserPassword, CreatedUserId, UpdatedUserId, UpdatedDateTime, IsActive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"    
                    val = (i, u, t, d, e, p, global_variable.USER_ID, global_variable.USER_ID, d, a)
                    self.open_db()
                    add_user.mycursor.execute(sql, val)
                    add_user.mydb.commit()
                    self.close_db()
                    QMessageBox.information(self, "Message", "Data registered successfully")
                    self.reset()
                else:
                    QMessageBox.critical(self, "Error", "User ID and/or Employee Code already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")


    def reset(self):
        self.user_id.clear()
        self.user_name.clear()
        self.user_pass.clear()
        self.emp_code.clear()
        self.user_combo.setCurrentText("-- Select --")
        self.user_active.setChecked(True)
