import json
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime
from appium import webdriver
import time
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

def auto_payment(screenshot = 0):
    def test(device, count, screenshot=False):
        options = AppiumOptions()
        options.load_capabilities({
            "deviceName": f"{device}",
            "platformName": "Android",
            "automationName": "UiAutomator2",
            "udid": f"{device}"
        })

        try:
            driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        except:
            driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        try:
            find_box = driver.find_element(
                by=AppiumBy.XPATH, value="//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]")
            find_box.click()
            enter_text = driver.find_element(
                by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            enter_text.send_keys(f"Facebook{count}")
            time.sleep(2)
            random_name = datetime.now().strftime("%H_%M_%S")
            if screenshot:
                image_path = os.path.join(
                    os.getcwd(), "images", f"{count}_Bill_VPBank_{random_name}.png")
                os.system(f"adb -s {device} exec-out screencap -p > {image_path}")
            driver.execute_script('mobile: pressKey', {"keycode": 4})
            driver.execute_script('mobile: pressKey', {"keycode": 4})
            driver.quit()
        except NoSuchElementException:
            pass
        except:
            os.system("adb kill-server")
            driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
            find_box = driver.find_element(
                by=AppiumBy.XPATH, value="//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]")
            find_box.click()
            enter_text = driver.find_element(
                by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
            enter_text.send_keys(f"Facebook{count}")
            time.sleep(2)
            random_name = datetime.now().strftime("%H_%M_%S")
            if screenshot:
                image_path = os.path.join(
                    os.getcwd(), "images", f"{count}_Bill_VPBank_{random_name}.png")
                os.system(f"adb -s {device} exec-out screencap -p > {image_path}")
            driver.execute_script('mobile: pressKey', {"keycode": 4})
            driver.execute_script('mobile: pressKey', {"keycode": 4})
            driver.quit()

    screen_shot = False
    if screenshot == 2:
        screen_shot = True

    def process_payment(devices, func):
        max_threads = len(devices)
        executor = ThreadPoolExecutor(max_workers=max_threads)
        futures = []
        for count, device in enumerate(devices, start=1):
            futures.append(executor.submit(func, device, count, screen_shot))
        for future in futures:
            future.result()


    with open('selected.json', 'r') as file:
        data = json.load(file)
    process_payment(data, test)