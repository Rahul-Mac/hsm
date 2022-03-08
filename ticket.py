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

class ticket(QtWidgets.QDialog):
    def __init__(self):
        super(ticket, self).__init__()
        uic.loadUi('ticket.ui', self)
        self.setWindowTitle("Ticket")
        self.ticket_box.setTitle(global_variable.TICKET)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.save_btn.clicked.connect(self.save)
        self.show()

    def save(self):
        i = global_variable.USER_ID
        t = global_variable.TICKET
        if self.pending.isChecked():
            a = '1'
        else:
            a = '0'
        s = self.solution.toPlainText()
        try:
            if i == "" or a == "" or s == "" or t == "":
                raise Exception()
            else:
                sql = "UPDATE transaction set IsActive = '"+str(a)+"', SolverId = '"+i+"', Solution = '"+s+"' where TicketId = '"+t+"'"
                global_variable.mycursor.execute(sql)
                global_variable.mydb.commit()
                QMessageBox.information(self, "Message", "Transaction successful!")
                self.close()
        except:
            QMessageBox.critical(self, "Error", "Transaction failed")

        
