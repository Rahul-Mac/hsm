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
import edit_loc

class edit_loc_box(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(edit_loc_box, self).__init__()
        uic.loadUi('edit_loc_box.ui', self)
        self.setWindowTitle("Hardware Service Manager - Location Edit")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.loc_update_btn.clicked.connect(self.update)
        self.loc_reset_btn.clicked.connect(self.reset)
        self.details_box.setTitle(global_variable.LOC)
        self.flr_combo.model().item(0).setEnabled(False)
        self.wing_combo.model().item(0).setEnabled(False)
        self.generate()
        self.show()

    def open_db(self):
        edit_loc_box.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        edit_loc_box.mycursor = edit_loc_box.mydb.cursor()

    def close_db(self):
        edit_loc_box.mycursor.close()
        edit_loc_box.mydb.close()

    def generate(self):
        self.open_db()
        edit_loc_box.mycursor.execute("SELECT IsActive, Floor, Wing from location where LocationName = '"+global_variable.LOC+"'")
        data = edit_loc_box.mycursor.fetchone()
        self.close_db()
        if data[0]:
            self.loc_active.setChecked(True)
        else:
            self.loc_active.setChecked(False)
        self.flr_combo.setCurrentText(data[1])
        self.wing_combo.setCurrentText(data[2])
    
    def update(self):
        l = global_variable.LOC
        f = self.flr_combo.currentText()
        w = self.wing_combo.currentText()
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        if self.loc_active.isChecked():
            a = '1'
        else:
            a = '0'
        if w == "-- Select --":
            w = ""
        try:
            if l == "" or f == "" or d == "" or u == "" or  f == "-- Select --" or a == "":
                raise Exception()
            else:
                sql = "UPDATE location set IsActive = '"+a+"', Floor = '"+f+"', Wing = '"+w+"', UpdatedDateTime = '"+d+"', UpdatedUserId = '"+u+"' Where LocationName = '"+l+"'"
                self.open_db()
                edit_loc_box.mycursor.execute(sql)
                edit_loc_box.mydb.commit()
                self.close_db()
                QMessageBox.information(self, "Message", "Data updated successfully!")
                self.close()
                
        except:
            QMessageBox.warning(self, "Warning", "Enter the details correctly")

    def reset(self):
        self.flr_combo.setCurrentText("-- Select --")
        self.wing_combo.setCurrentText("-- Select --")
        self.loc_active.setChecked(True)

    def closeEvent(self, event):
        self.ed = edit_loc.edit_loc()
        self.ed.show()
        self.close()
