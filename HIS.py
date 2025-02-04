from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QLineEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1246, 721)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Banner = QtWidgets.QFrame(self.centralwidget)
        self.Banner.setGeometry(QtCore.QRect(0, 0, 1251, 80))
        self.Banner.setStyleSheet("background-color: rgb(227, 236, 250);")
        self.Banner.setObjectName("Banner")
        self.ContactUS = QtWidgets.QLabel(self.Banner)
        self.ContactUS.setGeometry(QtCore.QRect(1000, 20, 151, 41))
        self.ContactUS.setStyleSheet("color: rgb(0, 0, 255);\n"
                                      "font: 18pt \"MS Shell Dlg 2\";")
        self.ContactUS.setObjectName("ContactUS")
        self.Logo = QtWidgets.QLabel(self.Banner)
        self.Logo.setGeometry(QtCore.QRect(0, 10, 91, 61))
        self.Logo.setStyleSheet("image: url(:/newPrefix/intelligentHealthInc/intelligentHealthInc/static/logo-removebg-preview.png);")
        self.Logo.setText("")
        self.Logo.setObjectName("Logo")
        self.IntelligentHealthInc = QtWidgets.QLabel(self.Banner)
        self.IntelligentHealthInc.setGeometry(QtCore.QRect(130, 0, 161, 71))
        self.IntelligentHealthInc.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";\n"
                                                "color: #0000FF")
        self.IntelligentHealthInc.setObjectName("IntelligentHealthInc")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-20, 80, 1261, 491))
        self.label.setStyleSheet("background-image: url(:/newPrefix/static/background.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.ToHIS = QtWidgets.QPushButton(self.centralwidget)
        self.ToHIS.setGeometry(QtCore.QRect(1000, 110, 93, 28))
        self.ToHIS.setObjectName("ToHIS")

        self.searchBar = QLineEdit(self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(20, 100, 200, 25))
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.filter_table)

        # Add a QTableWidget to the central widget
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 140, 1050, 411))
        self.tableWidget.setObjectName("tableWidget")

        # Connect to the database and fetch data when the application starts
        self.connect_to_database()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def connect_to_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Watchdogs1",
                database="fyp"
            )
            if self.db.is_connected():
                print("Connected to the MySQL database")
                # Fetch data from the database and populate the table
                self.fetch_data_from_database()
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            return

    def fetch_data_from_database(self):
        try:
            with self.db.cursor() as cursor:
                # Execute the SQL query
                cursor.execute("SELECT * FROM fyp.his")

                # Fetch all rows from the result set
                data = cursor.fetchall()

                if not data:
                    print("No data found in the table.")
                    return

                # Set the number of rows and columns in the table
                self.tableWidget.setRowCount(len(data))
                self.tableWidget.setColumnCount(len(cursor.description) + 1)  # +1 for the checkbox column

                # Set column headers, including an empty header for the checkbox column
                self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem(""))
                for i, column_info in enumerate(cursor.description):
                    self.tableWidget.setHorizontalHeaderItem(i + 1, QtWidgets.QTableWidgetItem(column_info[0]))

                # Populate the table with data and add checkboxes to the first column
                for row_num, row_data in enumerate(data):
                    # Add a checkbox in the first column
                    checkbox_item = QtWidgets.QTableWidgetItem()
                    checkbox_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    checkbox_item.setCheckState(QtCore.Qt.Unchecked)
                    self.tableWidget.setItem(row_num, 0, checkbox_item)

                    for col_num, cell_value in enumerate(row_data):
                        # Shift the columns by +1 to accommodate the checkbox column
                        col_index = col_num + 1
                        item = QtWidgets.QTableWidgetItem(str(cell_value))
                        self.tableWidget.setItem(row_num, col_index, item)

        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")
        finally:
            self.db.close()
            
    def filter_table(self):
        # Get the search query from the search bar
        search_query = self.searchBar.text()

        # Iterate through the rows and hide/show them based on the search query
        for row_num in range(self.tableWidget.rowCount()):
            row_hidden = True
            for col_num in range(1, self.tableWidget.columnCount()):
                item = self.tableWidget.item(row_num, col_num)
                if item and search_query.lower() in item.text().lower():
                    row_hidden = False
                    break

            # Set the row visibility based on whether it matches the search query
            self.tableWidget.setRowHidden(row_num, row_hidden)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ContactUS.setText(_translate("MainWindow", "Back"))
        self.IntelligentHealthInc.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>Health Inc.</p></body></html>"))
        self.IntelligentHealthInc.setText(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>HealthInc</p></body></html>"))
        self.ToHIS.setText(_translate("MainWindow", "Add Info"))
    
    def showAddInfoButton(self):
        # Show the "Add Info" button when any checkbox is checked
        for row_num in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_num, 0)  # Checkbox is in the first column
            if item and item.checkState() == QtCore.Qt.Checked:
                self.add_info_button.show()
                return
        # Hide the button if no checkbox is checked
        self.add_info_button.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())