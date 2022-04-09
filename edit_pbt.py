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
        mydb = ""
        mycursor = ""
        super(edit_pbt, self).__init__()
        uic.loadUi('edit_pbt.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Hardware Service Manager - Edit Problem - "+global_variable.USER_ID+" ("+global_variable.USER_TYPE+")")
        self.log.doubleClicked.connect(self.table_click)
        self.generate()
        self.search.textChanged.connect(self.get_search)
        self.show()

    def open_db(self):
        edit_pbt.mydb = mysql.connector.connect(host = global_variable.SERVER, user = "root", password = "root", database = "servicemgmt")
        edit_pbt.mycursor = edit_pbt.mydb.cursor()

    def close_db(self):
        edit_pbt.mycursor.close()
        edit_pbt.mydb.close()

    def table_click(self, item):
        global_variable.PBT = self.log.item(self.log.currentRow(), 2).text()
        self.pop = edit_pbt_box.edit_pbt_box()
        self.pop.show()
        self.close()

    def get_hardware(self, i):
        self.open_db()
        edit_pbt.mycursor.execute("SELECT HardwareName FROM hardwaretype where HardwareId = "+str(i)+";")
        x = edit_pbt.mycursor.fetchone()
        self.close_db()
        return(str(x[0]))

    def fetch(self, text):
        self.open_db()
        edit_pbt.mycursor.execute("SELECT IsActive, HardwareId, ProblemDescription from problemtype where ProblemDescription like '%"+text+"%';")
        data = edit_pbt.mycursor.fetchall()
        self.close_db()
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
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 0:
                        if d == "1":
                            d = "Yes"
                        else:
                            d = "No"
                    elif c == 1:
                        d = self.get_hardware(d)
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def get_search(self):
        if self.search.text() == "":
            self.generate()
        else:
            self.fetch(self.search.text())

    def generate(self):
        self.open_db()
        edit_pbt.mycursor.execute("SELECT IsActive, HardwareId, ProblemDescription from problemtype;")
        data = edit_pbt.mycursor.fetchall()
        self.close_db()
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
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 0:
                        if d == "1":
                            d = "Yes"
                        else:
                            d = "No"
                    elif c == 1:
                        d = self.get_hardware(d)
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

