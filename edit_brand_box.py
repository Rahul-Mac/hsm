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
import edit_brand

class edit_brand_box(QtWidgets.QDialog):
    def __init__(self):
        super(edit_brand_box, self).__init__()
        uic.loadUi('edit_brand_box.ui', self)
        self.setWindowTitle("Hardware Service Manager - Brand Edit")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.brd_update_btn.clicked.connect(self.update)
        self.brd_reset_btn.clicked.connect(self.reset)
        self.generate()
        self.show()

    def generate(self):
        global_variable.mycursor.execute("SELECT IsActive, BrandId from brand where BrandName = '"+global_variable.BRD+"'")
        data = global_variable.mycursor.fetchone()
        if data[0]:
            self.active.setChecked(True)
        else:
            self.active.setChecked(False)
        self.brd_entry.setText(global_variable.BRD)
        self.ids = data[1]
    
    def update(self):
        b = self.brd_entry.text()
        if self.active.isChecked():
            a = '1'
        else:
            a = '0'
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        try:
            if b == "" or d == "" or u == "" or  a == "": 
                raise Exception()
            else:
                global_variable.mycursor.execute("SELECT BrandName FROM brand WHERE BrandId = "+str(self.ids))
                x = global_variable.mycursor.fetchone()
                global_variable.mycursor.execute("SELECT BrandId FROM brand WHERE BrandName = '"+b+"'")
                y = global_variable.mycursor.fetchone()
                if x[0] == b or y is None:
                    sql = "UPDATE brand set BrandName = '"+b+"', IsActive = '"+a+"', UpdatedDateTime = '"+d+"', UpdatedUserId = '"+u+"' Where  BrandId = "+str(self.ids)
                    global_variable.mycursor.execute(sql)
                    global_variable.mydb.commit()
                    QMessageBox.information(self, "Message", "Data updated successfully!")
                    self.close()
                else:
                    QMessageBox.critical(self, "Error", "Update Failed! Brand already exists")
        except:
            QMessageBox.critical(self, "Error", "An error has occured while updating data. \nTry again.")

    def reset(self):
        self.brd_entry.clear()
        self.active.setChecked(True)

    def closeEvent(self, event):
        self.ed = edit_brand.edit_brand()
        self.ed.show()
        self.close()
