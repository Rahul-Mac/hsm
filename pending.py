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
import mysql.connector
import sys

class pending(QtWidgets.QDialog):
    def __init__(self):
        super(pending, self).__init__()
        uic.loadUi('pending.ui', self)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Pending Complaints")
        self.generate()
        self.show()

    def open_db(self):
        pending.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        pending.mycursor = pending.mydb.cursor()

    def close_db(self):
        pending.mycursor.close()
        pending.mydb.close()

    def get_problem_name(self, index):
        self.open_db()
        pending.mycursor.execute("SELECT ProblemId, ProblemDescription FROM problemtype where IsActive = 1;")
        self.problems = pending.mycursor.fetchall()
        self.close_db()
        for p in self.problems:
            if index == p[0]:
                return str(p[1])
    
    def get_hardware_name(self, index):
        self.open_db()
        pending.mycursor.execute("SELECT HardwareId, HardwareName FROM hardwaretype where IsActive = 1;")
        self.hardwares = pending.mycursor.fetchall()
        self.close_db()
        for h in self.hardwares:
            if index == h[0]:
                return str(h[1])
    
    def get_location_name(self, index):
        self.open_db()
        pending.mycursor.execute("SELECT LocationId, LocationName FROM location where IsActive = 1;")
        self.locations = pending.mycursor.fetchall()
        self.close_db()
        for loc in self.locations:
            if index == loc[0]:
                return str(loc[1])

    def generate(self):
        try:
            self.open_db()
            sql = "SELECT TicketId, ProblemId, HardwareId, AdminId, CreatedUserId, CreatedDateTime, LocationId, Name, SystemName, Remark, SolverId, Solution FROM transaction where CreatedUserId = '"+global_variable.USER_ID+"' and not Status = 'Completed';"
            pending.mycursor.execute(sql)
            data = pending.mycursor.fetchall()
            self.close_db()
            self.log_table.setRowCount(0)
            self.log_table.setRowCount(0)
            if len(data) == 0:
                return 
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
                    self.log_table.setItem(r, c, i)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
