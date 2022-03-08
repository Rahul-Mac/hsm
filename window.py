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
import about
import ticket
import lic
import generate_report
import full_log
import com_log
import manual
import login
import reset_password

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        uic.loadUi('window.ui', self)
        self.setWindowTitle("Hardware Service Manager - Master - "+global_variable.USER_ID+" ("+global_variable.USER_TYPE+")")
        self.measurement()
        self.connections()
        self.view_table()
        self.tool_bar()
        self.show()

    def tool_bar(self):
        tb = self.addToolBar("Tools")
        tb.addAction(QAction(QIcon("refresh.ico"), "Refresh Pending Log", self))
        tb.addAction(QAction(QIcon("user.ico"), "Add User", self))
        tb.addAction(QAction(QIcon("location.ico"), "Add Location", self))
        tb.addAction(QAction(QIcon("hardware.ico"), "Add Hardware", self))
        tb.addAction(QAction(QIcon("brand.ico"), "Add Brand", self))
        tb.addAction(QAction(QIcon("problem.ico"), "Add Problem", self))
        tb.addAction(QAction(QIcon("report.ico"), "Generate Report", self))
        tb.addAction(QAction(QIcon("complaint.png"), "Complaint", self))
        tb.addAction(QAction(QIcon("exit.png"), "Log Out", self))
        tb.actionTriggered[QAction].connect(self.tool_btn)

    def tool_btn(self, x):
        if x.text() == "Refresh Pending Log":
            self.refresh_table()
        elif x.text() == "Add User":
            self.open_add_user()
        elif x.text() == "Add Location":
            self.open_add_location()
        elif x.text() == "Add Hardware":
            self.open_add_hardware()
        elif x.text() == "Add Brand":
            self.open_add_brand()
        elif x.text() == "Add Problem":
            self.open_add_pbt()
        elif x.text() == "Generate Report":
            self.gen_rep()
        elif x.text() == "Complaint":
            self.show_complaint()
        elif x.text() == "Log Out":
            self.log_out()
        else:
            return
        
    def table_click(self, item):
        global_variable.TICKET = self.log_table.item(self.log_table.currentRow(), 0).text()
        self.pop = ticket.ticket()
        self.pop.show()

    def show_manual(self):
        self.pop = manual.manual()
        self.pop.show()
        
    def connections(self):
        self.log_table.doubleClicked.connect(self.table_click)
        self.manual.triggered.connect(self.show_manual)
        self.report.triggered.connect(self.gen_rep)
        self.full_log.triggered.connect(self.show_full_log)
        self.com_log.triggered.connect(self.show_com_log)
        self.add_user.triggered.connect(self.open_add_user)
        self.edit_user.triggered.connect(self.open_edit_user)
        self.rst_pass.triggered.connect(self.open_reset)
        self.actionLog_Out.triggered.connect(self.log_out)
        self.close_window.triggered.connect(self.close)
        self.add_location.triggered.connect(self.open_add_location)
        self.edit_location.triggered.connect(self.open_edit_location)
        self.add_hardware.triggered.connect(self.open_add_hardware)
        self.edit_hardware.triggered.connect(self.open_edit_hardware)
        self.add_brand.triggered.connect(self.open_add_brand)
        self.edit_brand.triggered.connect(self.open_edit_brand)
        self.add_pbt.triggered.connect(self.open_add_pbt)
        self.edit_pbt.triggered.connect(self.open_edit_pbt)
        self.refresh.triggered.connect(self.refresh_table)
        self.cmplnt.triggered.connect(self.show_complaint)
        self.about.triggered.connect(self.show_about)
        self.lic.triggered.connect(self.show_license)
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
        self.w = lic.lic()
        self.w.show()

    def show_about(self):
        self.w = about.about()
        self.w.show()

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
        self.log_table.setGeometry(0, 0, width, height)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.showMaximized()

    def get_problem_name(self, index):
        global_variable.mycursor.execute("SELECT ProblemId, ProblemDescription FROM problemtype where IsActive = 1;")
        self.problems = global_variable.mycursor.fetchall()
        for p in self.problems:
            if index == p[0]:
                return str(p[1])
    
    def get_hardware_name(self, index):
        global_variable.mycursor.execute("SELECT HardwareId, HardwareName FROM hardwaretype where IsActive = 1;")
        self.hardwares = global_variable.mycursor.fetchall()
        for h in self.hardwares:
            if index == h[0]:
                return str(h[1])
    
    def get_location_name(self, index):
        global_variable.mycursor.execute("SELECT LocationId, LocationName FROM location where IsActive = 1;")
        self.locations = global_variable.mycursor.fetchall()
        for loc in self.locations:
            if index == loc[0]:
                return str(loc[1])

    def view_table(self):
        global_variable.mycursor.execute("SELECT TicketId, ProblemId, HardwareId, AdminId, CreatedUserId, CreatedDateTime, LocationId, Name, SystemName, Remark FROM transaction where IsActive = 1;")
        data = global_variable.mycursor.fetchall()
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
            #header.setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)
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
