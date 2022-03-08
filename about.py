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
import sys

class about(QtWidgets.QDialog):
    def __init__(self):
        super(about, self).__init__()
        uic.loadUi('about.ui', self)
        self.setWindowTitle("About")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.desc.setText("Hardware Service Manager is a \nservice management software\nfor hardware components.\n\nCopyright (C) 2022 Rahul Mac\n under GNU GPL v3 License")
        self.show()
