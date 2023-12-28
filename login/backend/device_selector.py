import subprocess


def get_devices():
    devices = {}
    for device in subprocess.run(["adb", "devices", "-l"], capture_output=True).stdout.decode().split("\n")[1:-2]:
        if device.strip():
            device_adb_name = device.split()[0].strip()
            device_name = subprocess.run(
                ["adb", "-s", f"{device_adb_name}", "shell", "getprop", "ro.product.model"], capture_output=True).stdout.decode().strip()
            if device_name:
                devices[device_name] = device_adb_name
    return devices

devices = get_devices()
def select_devices(selected_device_names):
    selected_device_adb_names = []
    for selected_device_name in selected_device_names:
        if selected_device_name in devices:
            selected_device_adb_names.append(devices[selected_device_name])
        else:
            return "Vui lòng khởi động lại để quét thiết bị Offline"
    return selected_device_adb_names