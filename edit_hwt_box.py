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
import edit_hwt

class edit_hwt_box(QtWidgets.QDialog):
    def __init__(self):
        super(edit_hwt_box, self).__init__()
        uic.loadUi('edit_hwt_box.ui', self)
        self.setWindowTitle("Hardware Service Manager - Hardware Edit")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.hwt_update_btn.clicked.connect(self.update)
        self.hwt_reset_btn.clicked.connect(self.reset)
        self.details_box.setTitle(global_variable.HWT)
        self.generate()
        self.show()

    def generate(self):
        global_variable.mycursor.execute("SELECT IsActive from hardwaretype where HardwareName = '"+global_variable.HWT+"'")
        data = global_variable.mycursor.fetchone()
        if data[0]:
            self.hwt_active.setChecked(True)
        else:
            self.hwt_active.setChecked(False)
    
    def update(self):
        h = global_variable.HWT
        if self.hwt_active.isChecked():
            a = '1'
        else:
            a = '0'
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        try:
            if d == "" or u == "" or  a == "": 
                raise Exception()
            else:
                sql = "UPDATE hardwaretype set IsActive = '"+a+"', UpdatedDateTime = '"+d+"', UpdatedUserId = '"+u+"' Where HardwareName = '"+h+"'"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Data updated successfully!")
                self.close()
        except:
            QMessageBox.critical(self, "Error", "An error has occured while updating data. \nTry again.")

    def reset(self):
        self.hwt_active.setChecked(True)

    def closeEvent(self, event):
        self.ed = edit_hwt.edit_hwt()
        self.ed.show()
        self.close()

