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
import window
import complaint

class login(QtWidgets.QDialog):
    def __init__(self):
        super(login, self).__init__()
        uic.loadUi('login.ui', self)
        self.setWindowTitle("Hardware Service Manager - Login")
        self.login_btn.clicked.connect(self.login_check)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.show()
        
    def login_check(self):
        u = self.user.text()
        p = self.pswd.text()
        p = hashlib.md5(p.encode('utf-8')).hexdigest()
        try:
            if u == "" or p == "":
                QMessageBox().critical(self, "Error", "Empty fields are not allowed")
            else:
                mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
                mycursor = mydb.cursor()
                mycursor.execute("SELECT UserType FROM user WHERE UserId = '"+u+"' AND UserPassword = '"+p+"' AND IsActive = 1;")
                global_variable.USER_TYPE = mycursor.fetchone()[0]
                mycursor.close()
                mydb.close()
                global_variable.USER_ID = u
                if(global_variable.USER_TYPE):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Login Successful!")
                    msg.setWindowTitle("Message")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.buttonClicked.connect(self.msgbtn)
                    msg.setWindowIcon(QtGui.QIcon('icon.ico'))
                    retval = msg.exec_()
                else:
                    QMessageBox().critical(self, "Error", "UserID and/or Password is incorrect")
        except Exception as e:
            QMessageBox().critical(self, "Error", str(e))

    def msgbtn(self, x):
        if x.text:
            if global_variable.USER_TYPE == "Client":
                self.t = complaint.complaint()
                self.t.show()
                self.close()
            else:
                try:
                    self.w = window.window()
                    self.w.show()
                    self.close()
                except Exception as e:
                    QMessageBox().critical(self, "Error", str(e))
