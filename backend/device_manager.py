import subprocess


def get_list_devices():
    subprocess.run(["adb", "start-server"])
    devices = []
    for device in subprocess.run(["adb", "devices"], capture_output=True).stdout.decode().split("\n")[1:-1]:
        if device.strip():
            devices.append(device.split("\t")[0].strip())
    return devices


list_adb_devices = get_list_devices()


def get_device_name(device_adb_name):
    output = subprocess.run(
        ["adb", "-s", f"{device_adb_name}", "shell", "getprop", "ro.product.model"], capture_output=True).stdout
    return output.decode().strip()

# gọi hàm bên dưới để hiển thị ra danh sách các thiết bị
# làm dạng danh sách có thể bôi đen để chọn
def get_list_device_names(list_devices):
    device_names = []
    for device_adb_name in list_devices:
        device_names.append(get_device_name(device_adb_name))
    return device_names


list_device_names = get_list_device_names(list_adb_devices)

# làm một nút chọn để gửi tham số vào hàm bên dưới(bôi đen để chọn)
# (dưới dạng mảng| Ví dụ: ["SM-A908N","SM-G973N"])
def select_devices(selected_device_names):
    selected_device_adb_names = []
    for selected_device_name in selected_device_names:
        selected_device_index = list_device_names.index(selected_device_name)
        selected_device_adb_name = list_adb_devices[selected_device_index]
        selected_device_adb_names.append(selected_device_adb_name)
    return selected_device_adb_names
