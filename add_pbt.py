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
        mydb = ""
        mycursor = ""
        super(add_pbt, self).__init__()
        uic.loadUi('add_pbt.ui', self)
        self.setWindowTitle("Hardware Service Manager - Add Problem")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.hwt_combo.model().item(0).setEnabled(False)
        self.pbt_reset_btn.clicked.connect(self.reset)
        self.pbt_save_btn.clicked.connect(self.save)
        self.get_hardware_types()
        self.show()

    def open_db(self):
        add_pbt.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        add_pbt.mycursor = add_pbt.mydb.cursor()

    def close_db(self):
        add_pbt.mycursor.close()
        add_pbt.mydb.close()

    def get_hardware_types(self):
        self.open_db()
        add_pbt.mycursor.execute("SELECT HardwareId, HardwareName FROM hardwaretype where IsActive = 1;")
        self.hardwares = add_pbt.mycursor.fetchall()
        self.close_db()
        for hardware in self.hardwares:
            self.hwt_combo.addItem(hardware[1])

    def reset(self):
        self.pbt_entry.clear()
        self.hwt_combo.setCurrentText("-- Select --")
        self.pbt_active.setChecked(True)

    def save(self):
        p = self.pbt_entry.text()
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        h = self.hwt_combo.currentText()
        for hardware in self.hardwares:
            if h == hardware[1]:
                h = hardware[0]
                
        if self.pbt_active.isChecked():
            a = '1'
        else:
            a = '0'
        try:
            if p == "" or d == "" or u == "" or a == "" or h == "-- Select --" or h == "":
                QMessageBox.critical(self, "Error", "Please fill the compulsory fields")
            else:
                self.open_db()
                add_pbt.mycursor.execute("SELECT ProblemId FROM problemtype WHERE ProblemDescription = '"+p+"'")
                x = add_pbt.mycursor.fetchone()
                self.close_db()
                if x is None:
                    sql = "INSERT INTO problemtype (ProblemDescription, CreatedDateTime, CreatedUserId, UpdatedDateTime, UpdatedUserId, IsActive, HardwareId) VALUES ('"+p+"', '"+d+"', '"+u+"', '"+d+"', '"+u+"', '"+a+"', '"+str(h)+"')"
                    self.open_db()
                    add_pbt.mycursor.execute(sql)
                    add_pbt.mydb.commit()
                    self.close_db()
                    QMessageBox.information(self, "Message", "Data registered successfully!")
                    self.reset()
                else:
                    QMessageBox.critical(self, "Error", "Problem description already exists")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
