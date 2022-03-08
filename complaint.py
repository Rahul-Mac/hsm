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
from datetime import date
from datetime import timedelta

class complaint(QtWidgets.QDialog):
    def __init__(self):
        super(complaint, self).__init__()
        uic.loadUi('complaint.ui', self)
        self.setWindowTitle("Hardware Service Manager - Complaint - "+global_variable.USER_ID+" ("+global_variable.USER_TYPE+")")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.ticket.setEnabled(False)
        self.ad_combo.model().item(0).setEnabled(False)
        self.hwt_combo.model().item(0).setEnabled(False)
        self.pbt_combo.model().item(0).setEnabled(False)
        self.loc_combo.model().item(0).setEnabled(False)
        self.generate_ticket()
        self.get_admins()
        self.get_hardware_types()
        self.get_problem_types()
        self.get_location_types()
        self.reset_details.clicked.connect(self.reset)
        self.save_details.clicked.connect(self.save)
        self.show()

    def save(self):
        t = self.ticket.text()
        h = self.hwt_combo.currentText()
        p = self.pbt_combo.currentText()
        l = self.loc_combo.currentText()
        d = str(datetime.datetime.now())
        u = global_variable.USER_ID
        r = self.remark.toPlainText()
        for hardware in self.hardwares:
            if h == hardware[1]:
                h = hardware[0]

        for problem in self.problems:
            if p == problem[1]:
                p = problem[0]

        for loc in self.locations:
            if l == loc[1]:
                l = loc[0]
        b = self.sys_name.text()
        n = self.opt_name.text()
        a = self.ad_combo.currentText()
        try:
            if a == "" or u == "" or a == "-- Select --" or l == "" or l == "-- Select --" or t == "" or h == "" or h == "-- Select --" or p == "" or p == "-- Select --":
                raise Exception()
            else:
                if b == "":
                    b = "NULL"
                if r == "": 
                    r = "NULL"
                if  n == "":
                    n = "NULL"
                sql = "INSERT INTO transaction (TicketId, ProblemId, HardwareId, CreatedUserId, CreatedDateTime, Remark, SystemName, LocationId, Name, AdminId) VALUES \
                ('"+t+"', "+str(p)+", "+str(h)+", '"+u+"', '"+d+"','"+r+"', '"+str(b)+"', '"+str(l)+"', '"+n+"', '"+str(a)+"')"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Data registered successfully!")
                self.reset()
                self.generate_ticket()
        except:
           QMessageBox.critical(self, "Error", "Data registration failed")

    def reset(self):
        self.pbt_combo.setCurrentText("-- Select --")
        self.hwt_combo.setCurrentText("-- Select --")
        self.loc_combo.setCurrentText("-- Select --")
        self.ad_combo.setCurrentText("-- Select --")
        self.sys_name.clear()
        self.opt_name.clear()
        self.remark.setPlainText("")

    def get_location_types(self):
        global_variable.mycursor.execute("SELECT LocationId, LocationName FROM location where IsActive = 1;")
        self.locations = global_variable.mycursor.fetchall()
        for loc in self.locations:
            self.loc_combo.addItem(loc[1])

    def get_problem_types(self):
        global_variable.mycursor.execute("SELECT ProblemId, ProblemDescription FROM problemtype where IsActive = 1;")
        self.problems = global_variable.mycursor.fetchall()
        for problem in self.problems:
            self.pbt_combo.addItem(problem[1])

    def get_hardware_types(self):
        global_variable.mycursor.execute("SELECT HardwareId, HardwareName FROM hardwaretype where IsActive = 1;")
        self.hardwares = global_variable.mycursor.fetchall()
        for hardware in self.hardwares:
            self.hwt_combo.addItem(hardware[1])

    def get_admins(self):
        global_variable.mycursor.execute("SELECT UserId FROM user where IsActive = 1 and UserType = 'Admin';")
        self.admin = global_variable.mycursor.fetchall()
        for admin in self.admin:
            self.ad_combo.addItem(admin[0])

    def generate_ticket(self):
        yesterday = (date.today() - timedelta(days = 1)).year
        today = date.today().year            
        try:
            global_variable.mycursor.execute("SELECT count(ComplaintId) FROM transaction;")
            x = global_variable.mycursor.fetchall()
            cnt = x[0][0]
            if cnt == 0 or yesterday == today:
                self.ticket.setText("IT-"+str(today)+"-"+str(cnt))
            else:
                self.ticket.setText("IT-"+str(today)+"-"+str(0))
        except Exception as e:
            print(e)


