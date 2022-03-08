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
from PyQt5.QtWidgets import QMessageBox, QApplication, QCompleter, QFileDialog
from PyQt5.QtCore import QDateTime
import mysql.connector
import datetime
import global_variable
import sys
from datetime import date, datetime 
from datetime import timedelta
import pandas as pd

class generate_report(QtWidgets.QDialog):
    def __init__(self):
        super(generate_report, self).__init__()
        self.date = date.today()
        self.time = datetime.now()
        uic.loadUi('generate_report.ui', self)
        self.setWindowTitle("Generate Report")
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.folder.clicked.connect(self.select_directory)
        self.exp_btn.clicked.connect(self.export)
        self.rst_btn.clicked.connect(self.reset)
        self.start.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 0, 0, 0))
        self.end.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 23, 59, 59))
        self.show()

    def list_to_excel(self, n):
        fields = ['Ticket ID', 'Complainer', 'Assigned To', 'Location', 'Is It Pending?', 'Date & Time', 'System Name']
        df = pd.DataFrame(list(self.data), columns = fields)
        writer = pd.ExcelWriter(n)
        df.to_excel(writer)
        writer.save()
        QMessageBox.information(self, "Message", "File exported")
    
    def select_directory(self):
        self.folder.setText(str(QFileDialog.getExistingDirectory(self, "Select Folder")))

    def get_location_name(self, index, i):
        try:
            global_variable.mycursor.execute("SELECT LocationId, LocationName FROM location where IsActive = 1;")
            locations = global_variable.mycursor.fetchall()
            for loc in locations:
                if index == loc[0]:
                    self.data[i][3] = loc[1]
        except Exception as e:
            print(e)
                
    def convert(self):
        for i in range(len(self.data)):
            self.data.insert(i, list(self.data.pop(i)))
            self.get_location_name(self.data[i][3], i)
            self.data[i][4] = "Yes" if self.data[i][4] else "No"
            self.data[i][5] = str(self.data[i][5])

    def export(self):
        n = self.file_name.text()
        f = self.folder.text()
        s = self.start.dateTime().toPyDateTime()
        e = self.end.dateTime().toPyDateTime()
        try:
            if n == "" or f == "" or s == "" or e == "" or f == "Select Folder":
                raise Exception()
            else:
                sql = "SELECT TicketId, CreatedUserId, AdminId, LocationId, IsActive, CreatedDateTime, SystemName FROM transaction WHERE CreatedDateTime BETWEEN '"+str(s)+"' AND '"+str(e)+"'"
                global_variable.mycursor.execute(sql)
                self.data = global_variable.mycursor.fetchall()
                self.convert()
                self.list_to_excel(f+"/"+n+".xlsx")
                self.close()
        except:
            QMessageBox.critical(self, "Error", "An error has occured while exporting")

    def reset(self):
        self.file_name.clear()
        self.folder.setText("Select Folder")
        self.start.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 0, 0, 0))
        self.end.setDateTime(QDateTime(self.date.year, self.date.month, self.date.day, 23, 59, 59))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = generate_report()
    app.exec_()
