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
from PyQt5.QtWidgets import QMessageBox, QApplication, QCompleter, QTableWidgetItem
import mysql.connector
import datetime
import global_variable
import hashlib
import sys
import edit_pbt_box

class edit_pbt(QtWidgets.QDialog):
    def __init__(self):
        super(edit_pbt, self).__init__()
        uic.loadUi('edit_pbt.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Hardware Service Manager - Edit Problem - "+global_variable.USER_ID+" ("+global_variable.USER_TYPE+")")
        self.log.doubleClicked.connect(self.table_click)
        self.generate()
        self.search.textChanged.connect(self.get_search)
        self.show()

    def table_click(self, item):
        global_variable.PBT = self.log.item(self.log.currentRow(), 1).text()
        self.pop = edit_pbt_box.edit_pbt_box()
        self.pop.show()
        self.close()

    def fetch(self, text):
        global_variable.mycursor.execute("SELECT IsActive, ProblemDescription from problemtype where ProblemDescription like '%"+text+"%';")
        data = global_variable.mycursor.fetchall()
        self.log.setRowCount(0)
        if len(data) == 0:
            return 
        try:
            row = len(data)
            col = len(data[0])
            self.log.setRowCount(0)
            self.log.setRowCount(row)
            self.log.setColumnCount(col)
            header = self.log.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 0:
                        if d == "1":
                            d = "Yes"
                        else:
                            d = "No"
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "An error occured while populating data")

    def get_search(self):
        if self.search.text() == "":
            self.generate()
        else:
            self.fetch(self.search.text())

    def generate(self):
        global_variable.mycursor.execute("SELECT IsActive, ProblemDescription from problemtype;")
        data = global_variable.mycursor.fetchall()
        self.log.setRowCount(0)
        try:
            row = len(data)
            col = len(data[0])
            self.log.setRowCount(0)
            self.log.setRowCount(row)
            self.log.setColumnCount(col)
            header = self.log.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 0:
                        if d == "1":
                            d = "Yes"
                        else:
                            d = "No"
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "An error occured while populating data")
