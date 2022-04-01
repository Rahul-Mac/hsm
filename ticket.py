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
from PyQt5.QtWidgets import QMessageBox, QApplication
import mysql.connector
import datetime
import global_variable
import sys

class ticket(QtWidgets.QDialog):
    def __init__(self):
        mydb = ""
        mycursor = ""
        super(ticket, self).__init__()
        uic.loadUi('ticket.ui', self)
        self.setWindowTitle("Ticket")
        self.ticket_box.setTitle(global_variable.TICKET)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.save_btn.clicked.connect(self.save)
        self.status.model().item(0).setEnabled(False)
        self.generate()
        self.show()

    def open_db(self):
        ticket.mydb = mysql.connector.connect(host = "GMIT.LHDOMAIN.LOCAL", user = "root", password = "root", database = "servicemgmt")
        ticket.mycursor = ticket.mydb.cursor()

    def close_db(self):
        ticket.mycursor.close()
        ticket.mydb.close()

    def generate(self):
        self.open_db()
        ticket.mycursor.execute("SELECT Status, Solution from transaction where TicketId = '"+global_variable.TICKET+"'")
        data = ticket.mycursor.fetchone()
        self.close_db()
        self.status.setCurrentText(data[0])
        self.solution.insertPlainText(data[1])

    def save(self):
        i = global_variable.USER_ID
        t = global_variable.TICKET
        a = self.status.currentText()
        s = self.solution.toPlainText()
        try:
            if i == "" or a == "" or a == "-- Select --" or s == "" or t == "":
                QMessageBox.critical(self, "Error", "Empty fields are not allowed")
            else:
                sql = "UPDATE transaction set Status = '"+str(a)+"', SolverId = '"+i+"', Solution = '"+s+"' where TicketId = '"+t+"'"
                self.open_db()
                ticket.mycursor.execute(sql)
                ticket.mydb.commit()
                self.close_db()
                QMessageBox.information(self, "Message", "Transaction successful!")
                self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

        
