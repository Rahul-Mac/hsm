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
from PyQt5.QtWidgets import QMessageBox, QApplication, QCompleter, QTableWidgetItem, QToolBar, QAction
from PyQt5.QtGui import QIcon
import mysql.connector
import datetime
import hashlib
import sys
from datetime import date
from datetime import timedelta
import global_variable
import add_user
import edit_user
import add_loc
import edit_loc
import add_hwt
import edit_hwt
import add_brand
import edit_brand
import add_pbt
import edit_pbt
import complaint
import ticket
import generate_report
import full_log
import com_log
import manual
import login
import reset_password

class window(QtWidgets.QMainWindow):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(window, self).__init__()
        uic.loadUi('window.ui', self)
        self.setWindowTitle("Hardware Service Manager - Master - "+global_variable.USER_ID+" ("+global_variable.USER_TYPE+")")
        self.measurement()
        self.connections()
        try:
            self.view_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        self.refresh.setText("Refresh\nTable")
        self.com_log.setText("Completed\nTable")
        self.rst_pass.setText("Reset\nPassword")
        self.report.setText("Export To\nXLSX")
        self.show()

    def open_db(self):
        window.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        window.mycursor = window.mydb.cursor()

    def close_db(self):
        window.mycursor.close()
        window.mydb.close()
        
    def table_click(self, item):
        global_variable.TICKET = self.log_table.item(self.log_table.currentRow(), 0).text()
        self.pop = ticket.ticket()
        self.pop.show()

    def show_manual(self):
        self.pop = manual.manual()
        self.pop.show()
        
    def connections(self):
        self.log_table.doubleClicked.connect(self.table_click)
        self.manual.clicked.connect(self.show_manual)
        self.report.clicked.connect(self.gen_rep)
        self.full_log.clicked.connect(self.show_full_log)
        self.com_log.clicked.connect(self.show_com_log)
        self.add_user.clicked.connect(self.open_add_user)
        self.edit_user.clicked.connect(self.open_edit_user)
        self.rst_pass.clicked.connect(self.open_reset)
        self.actionLog_Out.clicked.connect(self.log_out)
        self.add_location.clicked.connect(self.open_add_location)
        self.edit_location.clicked.connect(self.open_edit_location)
        self.add_hardware.clicked.connect(self.open_add_hardware)
        self.edit_hardware.clicked.connect(self.open_edit_hardware)
        self.add_brand.clicked.connect(self.open_add_brand)
        self.edit_brand.clicked.connect(self.open_edit_brand)
        self.add_pbt.clicked.connect(self.open_add_pbt)
        self.edit_pbt.clicked.connect(self.open_edit_pbt)
        self.refresh.clicked.connect(self.refresh_table)
        self.cmplnt.clicked.connect(self.show_complaint)
        self.about.clicked.connect(self.show_about)
        self.lic.clicked.connect(self.show_license)
        self.problems = []
        self.hardwares = []
        self.locations = []

    def open_reset(self):
        self.w = reset_password.reset_password()
        self.w.show()

    def show_com_log(self):
        self.w = com_log.com_log()
        self.w.show()

    def show_full_log(self):
        self.w = full_log.full_log()
        self.w.show()

    def gen_rep(self):
        self.w = generate_report.generate_report()
        self.w.show()

    def refresh_table(self):
        self.problems.clear()
        self.hardwares.clear()
        self.locations.clear()
        self.view_table()

    def show_complaint(self):
        self.w = complaint.complaint()
        self.w.show()
        
    def show_license(self):
        text = "\t\tHardware Service Manager\n\
        Copyright (C) 2022  Rahul Mac\n\n\
        This program is free software: you can redistribute it and/or modify\n\
        it under the terms of the GNU General Public License as published by\n\
        the Free Software Foundation, either version 3 of the License, or\n\
        (at your option) any later version.\n\n\
        This program is distributed in the hope that it will be useful,\n\
        but WITHOUT ANY WARRANTY; without even the implied warranty of\n\
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n\
        GNU General Public License for more details."
        QMessageBox().about(self, "License", text)

    def show_about(self):
        text = "Hardware Service Manager v0.3.2\nis a service management software\nfor hardware components.\n\nCopyright (C) 2022 Rahul Mac\n under GNU GPL v3 License"
        QMessageBox().about(self, "About HSM", text)

    def open_add_pbt(self):
        self.w = add_pbt.add_pbt()
        self.w.show()

    def open_edit_pbt(self):
        self.w = edit_pbt.edit_pbt()
        self.w.show()

    def open_add_brand(self):
        self.w = add_brand.add_brand()
        self.w.show()

    def open_edit_brand(self):
        self.w = edit_brand.edit_brand()
        self.w.show()

    def open_add_hardware(self):
        self.w = add_hwt.add_hwt()
        self.w.show()

    def open_edit_hardware(self):
        self.w = edit_hwt.edit_hwt()
        self.w.show()

    def open_add_location(self):
        self.w = add_loc.add_loc()
        self.w.show()

    def open_edit_location(self):
        self.w = edit_loc.edit_loc()
        self.w.show()
        
    def open_add_user(self):
        self.w = add_user.add_user()
        self.w.show()

    def open_edit_user(self):     
        self.w = edit_user.edit_user()
        self.w.show()
        
    def measurement(self):
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        height = screenRect.height()
        width = screenRect.width()
        self.ribbon.setGeometry(0, 0, width, 121)
        self.log_table.setGeometry(0, 130, width, height-200)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.showMaximized()

    def get_problem_name(self, index):
        self.open_db()
        window.mycursor.execute("SELECT ProblemId, ProblemDescription FROM problemtype where IsActive = 1;")
        self.problems = window.mycursor.fetchall()
        self.close_db()
        for p in self.problems:
            if index == p[0]:
                return str(p[1])
    
    def get_hardware_name(self, index):
        self.open_db()
        window.mycursor.execute("SELECT HardwareId, HardwareName FROM hardwaretype where IsActive = 1;")
        self.hardwares = window.mycursor.fetchall()
        self.close_db()
        for h in self.hardwares:
            if index == h[0]:
                return str(h[1])
    
    def get_location_name(self, index):
        self.open_db()
        window.mycursor.execute("SELECT LocationId, LocationName FROM location where IsActive = 1;")
        self.locations = window.mycursor.fetchall()
        self.close_db()
        for loc in self.locations:
            if index == loc[0]:
                return str(loc[1])

    def view_table(self):
        self.open_db()
        window.mycursor.execute("SELECT TicketId, ProblemId, HardwareId, AdminId, CreatedUserId, CreatedDateTime, LocationId, Name, SystemName, Remark, SolverId, Solution FROM transaction where IsActive = 1;")
        data = window.mycursor.fetchall()
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

    def log_out(self):
        self.w = login.login()
        self.w.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = window()
    app.exec_()
