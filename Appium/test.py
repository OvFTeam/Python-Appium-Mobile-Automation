import os
import random

device = "your_device_identifier"
count = 1  # Đặt giá trị count của bạn
random_name = ''.join(random.choices(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

cwd = os.getcwd()
image_path = os.path.join(
    cwd, "images", f"{count}_Bill_VPBank_{random_name}.png")
command = f"adb -s {device} exec-out screencap -p > {image_path}"
os.system(command)
