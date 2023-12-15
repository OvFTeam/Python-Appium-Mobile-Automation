## 📦 **Module: Device Manager - Quản lý Thiết bị ADB** 💻📱

Module này cung cấp các chức năng để quản lý thiết bị Android bằng ADB. Nó cho phép lấy danh sách các thiết bị đã kết nối, lấy tên của các thiết bị và chọn thiết bị cụ thể để thực hiện các thao tác khác (bao gồm cả Appium).

### 📥 Cài đặt

Để sử dụng module Device Manager, bạn cần cài đặt Python và ADB.

1. **Python**: Truy cập [trang tải Python](https://www.python.org/downloads/) để tải về và cài đặt phiên bản Python phù hợp.

2. **ADB**: Truy cập [trang tải Platform Tools](https://developer.android.com/tools/releases/platform-tools) của Android để tải về và cài đặt ADB.

### 🚀 Sử dụng

1. Import module:
```python
from backend.device_manager import get_list_device_names, get_list_devices, select_devices
```

2. Lấy danh sách các thiết bị đã kết nối:
```python
list_adb_devices = get_list_devices()
```

**Ví dụ:**

**Đầu vào:**
```python
list_adb_devices = ['emulator-5554', '192.168.0.101:5555']
```

**Đầu ra (danh sách tên thiết bị):**
```python
list_device_names = ['Android Emulator', 'Samsung Galaxy S10']
```

3. Lấy tên của các thiết bị tương ứng với các tên thiết bị ADB:
```python
list_device_names = get_list_device_names(list_adb_devices)
```

4. Chọn các thiết bị cụ thể:
```python
selected_device_names = ["Thiết bị 1", "Thiết bị 2", ...]
selected_device_adb_names = select_devices(selected_device_names)
```

*Ví dụ:*
```python
selected_device_names = ["SM-A908N", "SM-G973N"]
selected_device_adb_names = select_devices(selected_device_names)
```

**Đầu vào (chọn thiết bị):**
```python
selected_device_names = ['Samsung Galaxy S10']
```

**Đầu ra (danh sách tên thiết bị ADB đã chọn):**
```python
selected_device_adb_names = ['192.168.0.101:5555']
```

Danh sách `list_adb_devices` chứa các tên thiết bị ADB đã kết nối. Hàm `get_list_device_names` sẽ lấy danh sách các tên thiết bị tương ứng với các tên thiết bị ADB. Sau đó, khi chọn thiết bị `"Samsung Galaxy S10"` từ danh sách `list_device_names`, hàm `select_devices` sẽ trả về danh sách các tên thiết bị ADB đã chọn là `['192.168.0.101:5555']`.

## Ví dụ với PyQt6

Cửa sổ Popup cơ bản với Module ***device_manager***

```python
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QScrollArea, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)

from backend.device_manager import (get_list_device_names, get_list_devices,
                                    select_devices)


class DeviceTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Danh sách thiết bị")
        self.setGeometry(100, 100, 400, 300)
        list_devices = get_list_devices()

        scroll_area = QScrollArea()

        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setRowCount(len(list_devices))
        self.table.setHorizontalHeaderLabels(["Tên thiết bị"])

        device_names = get_list_device_names(list_devices)
        for row, device_name in enumerate(device_names):
            item = QTableWidgetItem(device_name)
            self.table.setItem(row, 0, item)

        self.table.resizeColumnsToContents()
        column_width = self.table.columnWidth(0)
        self.table.setColumnWidth(0, column_width + 20)

        self.send_button = QPushButton("Chạy")
        self.send_button.clicked.connect(self.send_selected_devices)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.send_button)

        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def send_selected_devices(self):
        selected_rows = [index.row()
                         for index in self.table.selectionModel().selectedRows()]
        selected_device_names = [self.table.item(
            row, 0).text() for row in selected_rows]
        selected_device_adb_names = select_devices(selected_device_names)
        for adb_name in selected_device_adb_names:
            print(adb_name)  # hiện tại đang là test nên để print


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Danh sách thiết bị")
        widget = DeviceTableWidget()
        self.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.setCentralWidget(widget)
        self.setFixedSize(300, 260)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```