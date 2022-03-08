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

class add_pbt(QtWidgets.QDialog):
    def __init__(self):
        super(add_pbt, self).__init__()
        uic.loadUi('add_pbt.ui', self)
        self.setWindowTitle("Hardware Service Manager - Add Problem")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.pbt_reset_btn.clicked.connect(self.reset)
        self.pbt_save_btn.clicked.connect(self.save)
        self.show()

    def reset(self):
        self.pbt_entry.clear()
        self.pbt_active.setChecked(True)

    def save(self):
        p = self.pbt_entry.text()
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        if self.pbt_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if p == "" or d == "" or u == "" or a == "":
                raise Exception()
            else:
                global_variable.mycursor.execute("SELECT ProblemId FROM problemtype WHERE ProblemDescription = '"+p+"'")
                x = global_variable.mycursor.fetchone()
                if x is None:
                    sql = "INSERT INTO problemtype (ProblemDescription, CreatedDateTime, CreatedUserId, UpdatedDateTime, UpdatedUserId, IsActive) VALUES ('"+p+"', '"+d+"', '"+u+"', '"+d+"', '"+u+"', '"+a+"')"
                    global_variable.mycursor.execute(sql)
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset()
                else:
                    QMessageBox.critical(self, "Error", "Problem description already exists")
        except:
            QMessageBox.critical(self, "Error", "Data registration failed")