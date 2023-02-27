from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from tablewidget import Ui_MainWindow
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QTextDocument
import sys


class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Customers and goods")
        self.setWindowIcon(QIcon("Logo.png"))

        self.loadProducts()
        self.loadProductss()


        self.ui.pushButton.clicked.connect(self.data_save)
        self.ui.pushButton_1.clicked.connect(self.save_data)
        self.ui.pushButton_delete.clicked.connect(self.data_delete)
        self.ui.pushButton_delete_2.clicked.connect(self.delete_data)
        self.ui.pushButton_print.clicked.connect(self.print_receipt)

    def data_save(self):
        name = self.ui.name.text()
        surname = self.ui.surname.text()
        adres = self.ui.adres.text()
        kg = self.ui.kg.text()
        money = self.ui.money.text()
        number = self.ui.number.text()

        if name and surname and adres and kg and money and number is not None:
            rowCount = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(rowCount)
            self.ui.tableWidget.setItem(rowCount,0,QTableWidgetItem(name))
            self.ui.tableWidget.setItem(rowCount,1,QTableWidgetItem(surname))
            self.ui.tableWidget.setItem(rowCount,2,QTableWidgetItem(adres))
            self.ui.tableWidget.setItem(rowCount,3,QTableWidgetItem(kg))
            self.ui.tableWidget.setItem(rowCount,4,QTableWidgetItem(money))
            self.ui.tableWidget.setItem(rowCount,5,QTableWidgetItem(number))

            # зберегти дані в файлі
            with open('data\\data.txt', 'a') as f:
                row_data = f"{name},{surname},{adres},{kg},{money},{number}\n"
                f.write(row_data)

    def save_data(self):
        name_tow = self.ui.name_tow.text()
        purchase = self.ui.purchase_price.text()
        sale = self.ui.sale_price.text()


        if name_tow and purchase and sale is not None:
            rowCount = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(rowCount)
            self.ui.tableWidget_2.setItem(rowCount,0,QTableWidgetItem(name_tow))
            self.ui.tableWidget_2.setItem(rowCount,1,QTableWidgetItem(purchase))
            self.ui.tableWidget_2.setItem(rowCount,2,QTableWidgetItem(sale))
        
            # зберегти дані в файлі
            with open('data\\tow.txt', 'a') as f:
                row_data = f"{name_tow},{purchase},{sale}\n"
                f.write(row_data)
 

    def loadProducts(self):
        products = []

        # прочитати дані з файлу
        with open('data\\data.txt', 'r') as f:
            for line in f:
                row_data = line.strip().split(',')
                product = {
                    'name': row_data[0],
                    'surname': row_data[1],
                    'adres': row_data[2],
                    'kg': row_data[3],
                    'money': row_data[4],
                    'number': row_data[5]
                }
                products.append(product)

        # встановити кількість рядків у таблиці
        self.ui.tableWidget.setRowCount(len(products))

        # додати дані у таблицю
        row_index = 0
        for product in products:
            self.ui.tableWidget.setItem(row_index, 0, QTableWidgetItem(product['name']))
            self.ui.tableWidget.setItem(row_index, 1, QTableWidgetItem(product['surname']))
            self.ui.tableWidget.setItem(row_index, 2, QTableWidgetItem(product['adres']))
            self.ui.tableWidget.setItem(row_index, 3, QTableWidgetItem(product['kg']))
            self.ui.tableWidget.setItem(row_index, 4, QTableWidgetItem(product['money']))
            self.ui.tableWidget.setItem(row_index, 5, QTableWidgetItem(product['number']))
            row_index += 1


            self.ui.tableWidget.setRowCount(len(products))
    def loadProductss(self):
        products = []

        # прочитати дані з файлу
        with open('data\\tow.txt', 'r') as f:
            for line in f:
                row_data = line.strip().split(',')
                product = {
                    'name_tow': row_data[0],
                    'purchase': row_data[1],
                    'sale': row_data[2]
                }
                products.append(product)

        # встановити кількість рядків у таблиці
        self.ui.tableWidget_2.setRowCount(len(products))

        # додати дані у таблицю
        row_index = 0
        for product in products:
            self.ui.tableWidget_2.setItem(row_index, 0, QTableWidgetItem(product['name_tow']))
            self.ui.tableWidget_2.setItem(row_index, 1, QTableWidgetItem(product['purchase']))
            self.ui.tableWidget_2.setItem(row_index, 2, QTableWidgetItem(product['sale']))
            row_index += 1

            self.ui.tableWidget_2.setRowCount(len(products))


    def data_delete(self):
        selected_row_indexes = set(index.row() for index in self.ui.tableWidget.selectedIndexes())
        if len(selected_row_indexes) > 0:
            reply = QMessageBox.question(self, 'Delete Rows', f"Are you sure you want to delete {len(selected_row_indexes)} row(s)?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                with open("data\\data.txt", "r") as f:
                    lines = f.readlines()
                with open("data\\data.txt", "w") as f:
                    for i, line in enumerate(lines):
                        if i not in selected_row_indexes:
                            f.write(line)
                for row_index in sorted(selected_row_indexes, reverse=True):
                    self.ui.tableWidget.removeRow(row_index)
            else:
                QMessageBox.warning(self, 'Delete Rows', 'Please select at least one row to delete.', QMessageBox.Ok)


    def delete_data(self):
        selected_row_indexes = set(index.row() for index in self.ui.tableWidget_2.selectedIndexes())
        if len(selected_row_indexes) > 0:
            reply = QMessageBox.question(self, 'Delete Rows', f"Are you sure you want to delete {len(selected_row_indexes)} row(s)?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                with open("data\\tow.txt", "r") as f:
                    lines = f.readlines()
                with open("data\\tow.txt", "w") as f:
                    for i, line in enumerate(lines):
                        if i not in selected_row_indexes:
                            f.write(line)
                for row_index in sorted(selected_row_indexes, reverse=True):
                    self.ui.tableWidget_2.removeRow(row_index)
        else:
            QMessageBox.warning(self, 'Delete Rows', 'Please select at least one row to delete.', QMessageBox.Ok)

    def generate_receipt_text(self):
        rows = []
        for row_index in range(self.ui.tableWidget.rowCount()):
            name = self.ui.tableWidget.item(row_index, 0).text()
            surname = self.ui.tableWidget.item(row_index, 1).text()
            adres = self.ui.tableWidget.item(row_index, 2).text()
            kg = self.ui.tableWidget.item(row_index, 3).text()
            money = self.ui.tableWidget.item(row_index, 4).text()
            number = self.ui.tableWidget.item(row_index, 5).text()
            row = f"Name: {name}\nSurname: {surname}\nAdres: {adres}\nKg: {kg}\nMoney: {money}\nNumber: {number}\n"
            rows.append(row)
        receipt_text = "\n".join(rows)
        return receipt_text

    def print_receipt(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.Accepted:
            receipt_text = self.generate_receipt_text()
            document = QTextDocument()
            document.setPlainText(receipt_text)
            document.print_(printer)

def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())
create_app()
