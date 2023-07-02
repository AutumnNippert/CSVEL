import csv
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QAction, QFileDialog, QPushButton


class CSVEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CSVE")
        self.setStyleSheet('''
            QMainWindow {
                background-color: #f1f1f1;
            }

            QTableWidget {
                background-color: white;
                gridline-color: #c6c6c6;
            }

            QPushButton {
                background-color: #4caf50;
                color: white;
                border: none;
                padding: 5px 10px;
                font-size: 12px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        ''')

        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)

        self.file_path = None
        self.data = []

        self.create_menu()
        self.create_toolbar()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_csv)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_csv)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_csv)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_as_csv)
        file_menu.addAction(save_as_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Toolbar")

        add_row_button = QPushButton("Add Row", self)
        add_row_button.clicked.connect(self.add_row)
        toolbar.addWidget(add_row_button)

        add_column_button = QPushButton("Add Column", self)
        add_column_button.clicked.connect(self.add_column)
        toolbar.addWidget(add_column_button)

    def open_csv(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setDefaultSuffix("csv")
        file_path, _ = file_dialog.getOpenFileName()

        if file_path:
            self.file_path = file_path
            self.data = []
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.data.append(row)

            self.display_table()

    def save_csv(self):
        if self.file_path:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.get_table_data())
        else:
            self.save_as_csv()
            
    def save_as_csv(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        file_dialog.setDefaultSuffix("csv")
        file_path, _ = file_dialog.getSaveFileName()

        if file_path:
            self.file_path = file_path
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.get_table_data())

    def new_csv(self):
        self.table.clear()
        self.file_path = None
        self.data = []

    def display_table(self):
        num_rows = len(self.data)
        num_cols = len(self.data[0])

        self.table.setRowCount(num_rows)
        self.table.setColumnCount(num_cols)

        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.table.setItem(i, j, item)

    def get_table_data(self):
        table_data = []
        for i in range(self.table.rowCount()):
            row = []
            for j in range(self.table.columnCount()):
                item = self.table.item(i, j)
                row.append(item.text())
            table_data.append(row)
        return table_data

    def add_row(self):
        num_rows = self.table.rowCount()
        self.table.insertRow(num_rows)
        for j in range(self.table.columnCount()):
            item = QTableWidgetItem('')
            self.table.setItem(num_rows, j, item)

    def add_column(self):
        num_cols = self.table.columnCount()
        self.table.insertColumn(num_cols)
        for i in range(self.table.rowCount()):
            item = QTableWidgetItem('')
            self.table.setItem(i, num_cols, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    csv_editor = CSVEditor()
    csv_editor.show()
    sys.exit(app.exec_())
