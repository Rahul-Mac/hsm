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
import edit_pbt

class edit_pbt_box(QtWidgets.QDialog):
    def __init__(self):
        super(edit_pbt_box, self).__init__()
        uic.loadUi('edit_pbt_box.ui', self)
        self.setWindowTitle("Hardware Service Manager - Problem Edit")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.hwt_combo.model().item(0).setEnabled(False)
        self.pbt_update_btn.clicked.connect(self.update)
        self.pbt_reset_btn.clicked.connect(self.reset)
        self.pbt_box.setTitle(global_variable.PBT)
        self.get_hardware_types()
        self.generate()
        self.show()

    def get_hardware(self, i):
        global_variable.mycursor.execute("SELECT HardwareName FROM hardwaretype where HardwareId = "+str(i)+" and IsActive = 1;")
        x = global_variable.mycursor.fetchone()
        return(str(x[0]))

    def get_hardware_types(self):
        global_variable.mycursor.execute("SELECT HardwareId, HardwareName FROM hardwaretype where IsActive = 1;")
        self.hardwares = global_variable.mycursor.fetchall()
        for hardware in self.hardwares:
            self.hwt_combo.addItem(hardware[1])
            
    def generate(self):
        global_variable.mycursor.execute("SELECT IsActive, HardwareId from problemtype where ProblemDescription = '"+global_variable.PBT+"'")
        data = global_variable.mycursor.fetchone()
        if data[0]:
            self.pbt_active.setChecked(True)
        else:
            self.pbt_active.setChecked(False)
        self.hwt_combo.setCurrentText(self.get_hardware(data[1]))
    
    def update(self):
        p = global_variable.PBT
        if self.pbt_active.isChecked():
            a = '1'
        else:
            a = '0'
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        h = self.hwt_combo.currentText()
        for hardware in self.hardwares:
            if h == hardware[1]:
                h = hardware[0]
        try:
            if p == "" or d == "" or u == "" or  a == "": 
                raise Exception()
            else:
                sql = "UPDATE problemtype set HardwareID = '"+str(h)+"', IsActive = '"+a+"', UpdatedDateTime = '"+d+"', UpdatedUserId = '"+u+"' Where  ProblemDescription = '"+p+"'"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Data updated successfully!")
                self.close()                      
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def reset(self):
        self.pbt_active.setChecked(True)

    def closeEvent(self, event):
        self.pop = edit_pbt.edit_pbt()
        self.pop.show()
        self.close()

