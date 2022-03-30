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
from PyQt5.QtWidgets import QMessageBox, QApplication, QTableWidgetItem
import global_variable
import sys

class info(QtWidgets.QDialog):
    def __init__(self):
        super(info, self).__init__()
        uic.loadUi('info.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Information")
        self.generate()
        self.show()

    def generate(self):
        try:
            self.ticket.setText(global_variable.TICKET)
            self.hwt.setText(global_variable.HARDWARE)
            self.pbt.setText(global_variable.PROBLEM)
            self.usr.setText(global_variable.ASND)
            self.cmpid.setText(global_variable.COMP)
            self.name.setText(global_variable.NAME)
            self.remark.setPlainText(global_variable.REMARK)
        except:
            QMessageBox.critical(self, "Error", "An error occured while populating data")
