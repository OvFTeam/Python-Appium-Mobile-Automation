from concurrent.futures import ThreadPoolExecutor

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy


def test(device):
    options = AppiumOptions()
    options.load_capabilities({
        "deviceName": f"{device}",
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "udid": f"{device}"
    })

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    driver.find_element(
        by=AppiumBy.XPATH, value="//androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View[2]/android.view.View[1]/android.view.View/android.view.View[1]").click()
    driver.find_element(by=AppiumBy.CLASS_NAME,
                        value="android.widget.TextView").clear()
    driver.find_element(by=AppiumBy.CLASS_NAME,
                        value="android.widget.EditText").send_keys("Facebook"+"\n")
    driver.quit()

def process_payment(devices,bank):
    max_threads = len(devices)
    executor = ThreadPoolExecutor(max_workers=max_threads)
    futures = [executor.submit(bank, device) for device in devices]
    for future in futures:
        future.result()


# devices = ["9ca06bc0"]
# process_payment(devices, test)