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

class full_log(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(full_log, self).__init__()
        uic.loadUi('full_log.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Hardware Service Manager - Full Log - "+global_variable.USER_ID+" ("+global_variable.USER_TYPE+")")
        self.search.textChanged.connect(self.get_search)
        self.generate()
        self.show()

    def open_db(self):
        full_log.mydb = mysql.connector.connect(host = global_variable.SERVER, user = "root", password = "root", database = "servicemgmt")
        full_log.mycursor = full_log.mydb.cursor()

    def close_db(self):
        full_log.mycursor.close()
        full_log.mydb.close()

    def get_problem_name(self, index):
        self.open_db()
        full_log.mycursor.execute("SELECT ProblemId, ProblemDescription FROM problemtype where IsActive = 1;")
        self.problems = full_log.mycursor.fetchall()
        self.close_db()
        for p in self.problems:
            if index == p[0]:
                return str(p[1])
    
    def get_hardware_name(self, index):
        self.open_db()
        full_log.mycursor.execute("SELECT HardwareId, HardwareName FROM hardwaretype where IsActive = 1;")
        self.hardwares = full_log.mycursor.fetchall()
        self.close_db()
        for h in self.hardwares:
            if index == h[0]:
                return str(h[1])
    
    def get_location_name(self, index):
        self.open_db()
        full_log.mycursor.execute("SELECT LocationId, LocationName FROM location where IsActive = 1;")
        self.locations = full_log.mycursor.fetchall()
        self.close_db()
        for loc in self.locations:
            if index == loc[0]:
                return str(loc[1])

    def get_search(self):
        if self.search.text() == "":
            self.generate()
        else:
            self.fetch(self.search.text())

    def fetch(self, text):
        self.open_db()
        full_log.mycursor.execute("SELECT TicketId, ProblemId, HardwareId, AdminId, CreatedUserId, CreatedDateTime, LocationId, Name, SystemName, Status, Remark, SolverId, Solution FROM transaction where TicketId like '%"+text+"%';")
        data = full_log.mycursor.fetchall()
        self.close_db()
        self.log_table.setRowCount(0)
        if len(data) == 0:
            return 
        try:
            row = len(data)
            col = len(data[0])
            self.log_table.setRowCount(0)
            self.log_table.setRowCount(row)
            self.log_table.setColumnCount(col)
            header = self.log_table.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
            for r in range(row):
                for c in range(col):
                    d = data[r][c]
                    if c == 5:
                        i = QTableWidgetItem(d.strftime("%Y/%m/%d, %H:%M:%S"))
                    elif c == 1:
                        i = QTableWidgetItem(self.get_problem_name(d))
                    elif c == 2:
                        i = QTableWidgetItem(self.get_hardware_name(d))
                    elif c == 6:
                        i = QTableWidgetItem(self.get_location_name(d))
                    else:
                        if d == "NULL":
                            i = QTableWidgetItem("")
                        else:
                            i = QTableWidgetItem(str(d))
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log_table.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "Failed to load data")


    def generate(self):
        self.open_db()
        full_log.mycursor.execute("SELECT TicketId, ProblemId, HardwareId, AdminId, CreatedUserId, CreatedDateTime, LocationId, Name, SystemName, Status, Remark, SolverId, Solution FROM transaction;")
        data = full_log.mycursor.fetchall()
        self.close_db()
        self.log_table.setRowCount(0)
        self.log_table.setRowCount(0)
        if len(data) == 0:
            return 
        try:
            row = len(data)
            col = len(data[0])
            self.log_table.setRowCount(0)
            self.log_table.setRowCount(row)
            self.log_table.setColumnCount(col)
            header = self.log_table.horizontalHeader()       
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(11, QtWidgets.QHeaderView.ResizeToContents)
            for r in range(row):
                for c in range(col):
                    d = data[r][c]
                    if c == 5:
                        i = QTableWidgetItem(d.strftime("%Y/%m/%d, %H:%M:%S"))
                    elif c == 1:
                        i = QTableWidgetItem(self.get_problem_name(d))
                    elif c == 2:
                        i = QTableWidgetItem(self.get_hardware_name(d))
                    elif c == 6:
                        i = QTableWidgetItem(self.get_location_name(d))
                    else:
                        if d == "NULL":
                            i = QTableWidgetItem("")
                        else:
                            i = QTableWidgetItem(str(d))
                    i.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.log_table.setItem(r, c, i)
        except:
            QMessageBox.critical(self, "Error", "Failed to load data")
