import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView)

from ui_main import Ui_MainWindow
from ui_add_edit_coffee import Ui_Form


class AddCoffeeWidget(QMainWindow, Ui_Form):
    def __init__(self, parent, coffee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.coffee_id = coffee_id

        self.roast.addItems(["Светлая", "Средняя", "Темная"])
        self.grind.addItems(["В зернах", "Молотый"])
        self.taste.setFixedHeight(70)
        self.price.setRange(0, 100000)
        self.price.setSuffix(" руб.")
        self.volume.setRange(0, 10000)
        self.volume.setSuffix(" г")
        self.btn.clicked.connect(self.save)

        if coffee_id:
            self.load_data()
            self.btn.setText("Сохранить")
            self.setWindowTitle("Редактирование")
        else:
            self.setWindowTitle("Добавление")

    def load_data(self):
        con = sqlite3.connect("data/coffee.sqlite")
        row = con.execute(
            "SELECT name, roast, grind_type, taste_description, price, package_volume "
            "FROM coffee WHERE id = ?", (self.coffee_id,)
        ).fetchone()
        con.close()
        if row:
            self.name.setText(row[0])
            self.roast.setCurrentText(row[1])
            self.grind.setCurrentText(row[2])
            self.taste.setPlainText(row[3] or "")
            self.price.setValue(row[4])
            self.volume.setValue(row[5])

    def save(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название.")
            return
        con = sqlite3.connect("data/coffee.sqlite")
        cur = con.cursor()
        if self.coffee_id:
            cur.execute(
                "UPDATE coffee SET name=?, roast=?, grind_type=?, "
                "taste_description=?, price=?, package_volume=? WHERE id=?",
                (self.name.text(), self.roast.currentText(), self.grind.currentText(),
                 self.taste.toPlainText(), self.price.value(), self.volume.value(),
                 self.coffee_id)
            )
        else:
            cur.execute(
                "INSERT INTO coffee (name, roast, grind_type, taste_description, price, package_volume) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (self.name.text(), self.roast.currentText(), self.grind.currentText(),
                 self.taste.toPlainText(), self.price.value(), self.volume.value())
            )
        con.commit()
        con.close()
        self.parent.update_table()
        self.close()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)

        self.addButton.clicked.connect(self.add)
        self.editButton.clicked.connect(self.edit)

        self.update_table()

    def update_table(self):
        con = sqlite3.connect("data/coffee.sqlite")
        rows = con.execute(
            "SELECT id, name, roast, grind_type, taste_description, price, package_volume FROM coffee"
        ).fetchall()
        con.close()

        headers = ["ID", "Название", "Обжарка", "Тип", "Вкус", "Цена", "Объем"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val) if val is not None else ""))

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def add(self):
        self.window = AddCoffeeWidget(self)
        self.window.show()

    def edit(self):
        row = self.table.currentRow()
        if row < 0:
            return
        coffee_id = int(self.table.item(row, 0).text())
        self.window = AddCoffeeWidget(self, coffee_id)
        self.window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec())