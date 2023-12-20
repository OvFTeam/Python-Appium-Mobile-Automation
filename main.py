import codecs
import json
import sys

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QMouseEvent, QPalette
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

import backend.device_selector

df = pd.read_excel('du_lieu/data.xlsx')
customer_code = df.iloc[:, 0].dropna().values.tolist()
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BillEaseBank")
        self.layout = QVBoxLayout()

        palette = QPalette()

        palette.setColor(QPalette.Window, QColor("#282a36"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#282a36"))
        palette.setColor(QPalette.AlternateBase, QColor("#353746"))
        palette.setColor(QPalette.ToolTipBase, QColor("#f8f8f2"))
        palette.setColor(QPalette.ToolTipText, QColor("#f8f8f2"))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#6272a4"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor("#ff79c6"))
        palette.setColor(QPalette.Highlight, QColor("#bd93f9"))
        palette.setColor(QPalette.HighlightedText, QColor("#282a36"))
        self.setPalette(palette)

        self.scan_button = QPushButton("Quét thiết bị")
        self.start_button = QPushButton("Chạy")
        self.stop_button = QPushButton("Dừng")
        self.save_button = QPushButton("Lưu dữ liệu")
        self.refresh_button = QPushButton("Refresh")
        self.screenshot_checkbox = QCheckBox("Chụp màn hình")
        self.username_label = QLabel("Tên tài khoản")
        self.username_label.setStyleSheet("border: none;")
        self.username_input = QLineEdit()
        self.bank_combobox = QComboBox()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderItem(0, QTableWidgetItem("STT"))
        self.table.setHorizontalHeaderItem(
            1, QTableWidgetItem("Mã khách hàng"))
        self.table.setHorizontalHeaderItem(2, QTableWidgetItem("Trạng thái"))
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setShowGrid(True)
        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self.table.setColumnWidth(0, 20)
        self.table.setColumnWidth(1, 140)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.scan_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.save_button)

        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.username_label, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.bank_combobox)
        self.layout.addWidget(self.screenshot_checkbox)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.scan_button.clicked.connect(self.scan_devices)
        self.start_button.clicked.connect(self.start_process)
        self.stop_button.clicked.connect(self.stop_process)
        self.save_button.clicked.connect(self.save_data)
        self.refresh_button.clicked.connect(self.update_table)
        self.screenshot_checkbox.stateChanged.connect(self.toggle_screenshot)
        with codecs.open('banks.json', 'r', 'utf-8-sig') as f:
            banks = json.load(f)
        self.bank_combobox.addItem("Chọn ngân hàng")
        self.bank_combobox.addItems(banks)
        self.fill_default_values()
        self.update_table()

        self.table.setStyleSheet("""
            QTableWidget::item {
                padding-top: 3px;
                padding-bottom: 3px;
            }
        """)

        self.setStyleSheet("""
            * {
                font-family: 'JetBrains Mono', monospace;
                color: #f8f8f2;
                background-color: #282a36;
                font-size: 16px;
            }
            QPushButton, QLineEdit, QCheckBox, QTableWidget, QHeaderView::section {
                font-size: 16px;
            }
            QPushButton, QLineEdit {
                background-color: #44475A;
                color: #f8f8f2;
                padding: 15px;
                text-align: center;
                text-decoration: none;
                margin: 4px 2px;
                border-radius: 20px;
            }
            QPushButton {
                background-color: #6272a4;
            }
            QPushButton:hover {
                background-color: #44475a;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 30px;
                height: 30px;
                border-radius: 15px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #44475a;
                border: 1px solid #bd93f9;
            }
            QCheckBox::indicator:checked {
                background-color: #bd93f9;
            }
            QTableWidget {
                background-color: #282a36;
                color: #f8f8f2;
                gridline-color: #6272a4;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                border: 1px solid #6272a4;
            }
            QHeaderView::section {
                background-color: #282a36;
                color: white;
                padding: 4px;
                border: none;
            }
            QTableView {
                selection-background-color: #6272A4;
                selection-color: #F8F8F2;
            }
            QTableView::item:selected {
                background-color: #6272A4;
                color: #F8F8F2;
                border: none;
            }
        """)
        self.bank_combobox.setStyleSheet("""
            QComboBox {
                background-color: #44475A;
                font-size: 16px;
                border: none;
                padding: 10px;
                color: #f8f8f2;
            }
            QComboBox::drop-down {
                background-color: #44475A;
                border-radius: 20px;
            }
        """)

        self.showMaximized()

    def update_table(self):
        try:
            df = pd.read_excel('du_lieu/data.xlsx')
            customer_code = df.iloc[:, 0].dropna().values.tolist()
            row_count = len(customer_code)
            self.table.setRowCount(row_count)
            index = 0
            for row in range(row_count):
                index += 1
                self.table.setItem(row, 0, QTableWidgetItem(str(index)))
                self.table.setItem(row, 1, QTableWidgetItem(customer_code[row]))
                self.table.item(row, 0).setTextAlignment(Qt.AlignCenter)
                self.table.item(row, 1).setTextAlignment(Qt.AlignCenter)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error occurred while updating table: {str(e)}")

    def fill_default_values(self):
        if self.username_input.text().strip() == "":
            self.username_input.setPlaceholderText("Điền tên tài khoản")
            self.bank_combobox.setCurrentText("Chọn ngân hàng")

    def scan_devices(self):
        popup = ScanPopup()
        popup.exec_()

    def start_process(self):
        pass

    def stop_process(self):
        pass

    def save_data(self):
        pass

    def toggle_screenshot(self, state):
        print(state)


class ScanPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.devices = backend.device_selector.get_devices()
        self.selected_devices = []

        self.setWindowTitle("Chọn thiết bị khởi chạy")
        self.layout = QVBoxLayout()
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.select_all_checkbox = QCheckBox("Chọn tất cả")
        self.select_all_checkbox.stateChanged.connect(self.select_all_devices)
        self.select_all_checkbox.setStyleSheet("border: none;")
        self.layout.addWidget(self.select_all_checkbox)
        self.empty_label = QLabel("Không tìm thấy thiết bị")
        self.empty_label.setStyleSheet(
            "font-size: 20px;border: none;text-align: center;")
        self.empty_label.hide()
        self.layout.addWidget(self.empty_label)
        self.draggable = True
        self.dragging_threshold = 5
        self.drag_start_position = None

        self.device_checkboxes = []
        for device_name in self.devices:
            checkbox = QCheckBox(device_name)
            checkbox.setStyleSheet("border: none;")
            self.device_checkboxes.append(checkbox)
            self.layout.addWidget(checkbox)

        self.button_layout = QHBoxLayout()

        if len(self.devices) > 0:
            self.save_button = QPushButton("Lưu")
            self.save_button.clicked.connect(self.save_devices)
            self.button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Huỷ")
        self.cancel_button.clicked.connect(self.cancel_scan)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

        if len(self.devices) == 0:
            self.empty_label.show()
            self.select_all_checkbox.hide()
        if len(self.device_checkboxes) == 1:
            self.select_all_checkbox.hide()
            self.device_checkboxes[0].setChecked(True)
        self.setStyleSheet("""
        * {
            font-family: 'JetBrains Mono', monospace;
            margin: 1px;
        }
        QWidget {
            background-color: #282a36;
            color: #f8f8f2;
            font-size: 16px;
            width: 300px;
            border-radius: 20px;
            border: 2px solid #44475A;
        }
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 30px;
            height: 30px;
            border-radius: 15px;
        }
        QCheckBox::indicator:unchecked {
            background-color: #44475a;
            border: 1px solid #bd93f9;
            border-radius: 15px;
        }
        QCheckBox::indicator:checked {
            background-color: #bd93f9;
            border-radius: 15px;
        }
        QPushButton {
            background-color: #6272a4;
            border: none;
            color: #f8f8f2;
            padding: 15px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
        }
        QPushButton:hover {
            background-color: #44475a;
        }
    """)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.draggable:
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag_start_position is not None and self.draggable:
            if (event.globalPos() - self.drag_start_position).manhattanLength() >= self.dragging_threshold:
                self.move(self.pos() + event.globalPos() -
                          self.drag_start_position)
                self.drag_start_position = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.draggable:
            self.drag_start_position = None

    def select_all_devices(self, state):
        for checkbox in self.device_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

    def save_devices(self):
        selected_device_names = [
            checkbox.text() for checkbox in self.device_checkboxes if checkbox.isChecked()]
        selected_device_adb_names = backend.device_selector.select_devices(
            selected_device_names)

        if isinstance(selected_device_adb_names, str):
            QMessageBox.warning(self, "Lỗi", selected_device_adb_names)
        else:
            with open("selected.json", "w") as file:
                json.dump(selected_device_adb_names, file)
        self.close()

    def cancel_scan(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
