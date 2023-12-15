def get_list_devices():
    devices = ['127.0.0.1:5555', '127.0.0.1:5556',
               '127.0.0.1:5557', '127.0.0.1:5558', '127.0.0.1:5559']
    return devices


list_devices = get_list_devices()


def get_device_name(device_name):
    device_name = f"Máy {device_name.split(':')[-1]}"
    return device_name

# gọi hàm bên dưới để hiển thị ra danh sách các thiết bị
# làm dạng danh sách có thể bôi đen để chọn


def get_list_device_names(list_devices):
    device_names = []
    for device_name in list_devices:
        device_names.append(get_device_name(device_name))
    return device_names


list_device_names = get_list_device_names(list_devices)

# làm một nút chọn để gửi tham số vào hàm bên dưới(bôi đen để chọn)
# (dưới dạng mảng| Ví dụ: ["Máy 5555","Máy 5556"])


def select_devices(selected_device_names):
    selected_device_adb_names = []
    for selected_device_name in selected_device_names:
        selected_device_index = list_device_names.index(selected_device_name)
        selected_device_adb_name = list_devices[selected_device_index]
        selected_device_adb_names.append(selected_device_adb_name)
    return selected_device_adb_names
