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
import edit_user

class edit_user_box(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(edit_user_box, self).__init__()
        uic.loadUi('edit_user_box.ui', self)
        self.setWindowTitle("Hardware Service Manager - User Edit")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.user_update_btn.clicked.connect(self.update)
        self.user_reset_btn.clicked.connect(self.reset)
        self.details_box.setTitle(global_variable.UID)
        self.user_combo.model().item(0).setEnabled(False)
        self.generate()
        self.show()

    def open_db(self):
        edit_user_box.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        edit_user_box.mycursor = edit_user_box.mydb.cursor()

    def close_db(self):
        edit_user_box.mycursor.close()
        edit_user_box.mydb.close()

    def closeEvent(self, event):
        self.ed = edit_user.edit_user()
        self.ed.show()
        self.close()

    def generate(self):
        self.open_db()
        edit_user_box.mycursor.execute("SELECT IsActive, UserType, EmployeeCode, UserName from user where UserId = '"+global_variable.UID+"'")
        data = edit_user_box.mycursor.fetchone()
        self.close_db()
        if data[0]:
            self.user_active.setChecked(True)
        else:
            self.user_active.setChecked(False)
        self.user_combo.setCurrentText(data[1])
        self.emp_code.setText(data[2])
        self.user_name.setText(data[3])
        
    def update(self):
        i = global_variable.UID
        u = self.user_name.text()
        e = self.emp_code.text()
        t = self.user_combo.currentText()
        d = str(datetime.datetime.now())
        if self.user_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if  i == "" or u == "" or e == "" or t == "" or t == "-- Select --" or a == "":
                raise Exception()
            else:
                self.open_db()
                edit_user_box.mycursor.execute("SELECT UserIndex FROM user WHERE EmployeeCode = '"+e+"'")
                x = edit_user_box.mycursor.fetchone()
                self.close_db()
                self.open_db()
                edit_user_box.mycursor.execute("SELECT EmployeeCode FROM user WHERE UserId = '"+i+"'")
                y = edit_user_box.mycursor.fetchone()
                self.close_db()
                if e == y[0]:
                    x = None
                if x is None:
                    sql = "UPDATE user set IsActive = '"+a+"', UserName = '"+u+"', UserType = '"+t+"', EmployeeCode = '"+e+"', UpdatedDateTime = '"+d+"', UpdatedUserId = '"+global_variable.USER_ID+"' Where UserId = '"+i+"'"
                    self.open_db()
                    edit_user_box.mycursor.execute(sql)
                    edit_user_box.mydb.commit()
                    self.close_db()
                    QMessageBox.information(self, "Message", "Data updated successfully!")
                    self.close()
                else:
                    QMessageBox.critical(self, "Error", "Update Failed! Employee Code already exists")
        except:
            QMessageBox.critical(self, "Error", "An error has occured while updating data. \nTry again.")


    def reset(self):
        self.user_name.clear()
        self.emp_code.clear()
        self.user_combo.setCurrentText("-- Select --")
        self.user_active.setChecked(True)

