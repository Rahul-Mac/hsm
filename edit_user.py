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
import edit_user_box

class edit_user(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(edit_user, self).__init__()
        uic.loadUi('edit_user.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Hardware Service Manager - Edit User - "+global_variable.USER_ID+" ("+global_variable.USER_TYPE+")")
        self.log.doubleClicked.connect(self.table_click)
        self.generate()
        self.search.textChanged.connect(self.get_search)
        self.show()

    def open_db(self):
        edit_user.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        edit_user.mycursor = edit_user.mydb.cursor()

    def close_db(self):
        edit_user.mycursor.close()
        edit_user.mydb.close()

    def table_click(self, item):
        global_variable.UID = self.log.item(self.log.currentRow(), 0).text()
        self.pop = edit_user_box.edit_user_box()
        self.pop.show()
        self.close()

    def fetch(self, text):
        self.open_db()
        edit_user.mycursor.execute("SELECT UserId, IsActive, UserType, EmployeeCode, UserName from user where UserId like '%"+text+"%';")
        data = edit_user.mycursor.fetchall()
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
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 1:
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
        self.open_db()
        edit_user.mycursor.execute("SELECT UserId, IsActive, UserType, EmployeeCode, UserName from user;")
        data = edit_user.mycursor.fetchall()
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
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
            for r in range(row):
                for c in range(col):
                    d = str(data[r][c])
                    if c == 1:
                        if d == "1":
                            d = "Yes"
                        else:
                            d = "No"
                    i = QTableWidgetItem(d)
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "An error occured while populating data")
