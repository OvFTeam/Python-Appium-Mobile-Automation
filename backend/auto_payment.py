from concurrent.futures import ThreadPoolExecutor

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def vpbank(device, account_name, ma_khach_hang):
    options = AppiumOptions()
    options.load_capabilities({
        "deviceName": f"{device}",
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "udid": f"{device}"
    })

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    wait = WebDriverWait(driver, 5)
    wait_thanh_toan_hoa_don = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "(//android.widget.ImageView[@resource-id=\"com.vnpay.vpbankonline:id/icon\"])[1]")))
    wait_thanh_toan_hoa_don.click()
    wait_hoa_don_tien_dien = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "(//android.widget.ImageView[@resource-id='com.vnpay.vpbankonline:id/icon'])[1]")))
    wait_hoa_don_tien_dien.click()
    wait_new_bill = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.LinearLayout[@resource-id="com.vnpay.vpbankonline:id/ll_create_new_bill"]')))
    wait_new_bill.click()
    wait_nha_cung_cap = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.LinearLayout[@resource-id=\"com.vnpay.vpbankonline:id/mainLayout\"]/android.widget.LinearLayout")))
    wait_nha_cung_cap.click()
    wait_dien_luc_toan_quoc = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.vnpay.vpbankonline:id/rvList"]/android.widget.LinearLayout[4]')))
    wait_dien_luc_toan_quoc.click()
    try:
        wait_tai_khoan_nguon = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, "//android.widget.LinearLayout[@resource-id='com.vnpay.vpbankonline:id/selectAccount']/android.widget.LinearLayout/android.widget.LinearLayout")))
        wait_tai_khoan_nguon.click()
    except StaleElementReferenceException:
        wait_tai_khoan_nguon = wait.until(EC.visibility_of_element_located(
            (AppiumBy.XPATH, "//android.widget.LinearLayout[@resource-id='com.vnpay.vpbankonline:id/selectAccount']/android.widget.LinearLayout/android.widget.LinearLayout")))
        wait_tai_khoan_nguon.click()
    except Exception as e:
        return e

    def chon_tai_khoan_nguon(account):
        valid_input = False
        while not valid_input:
            elements = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.ListView[@resource-id='com.vnpay.vpbankonline:id/listAccount']") \
                .find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.TextView")
            for element in elements:
                if element.text == account:
                    valid_input = True
                    return element
            return "Chỉ cần nhập số thẻ hoặc loại thẻ"

    chon_tai_khoan_nguon(account_name).click()
    wait_ma_khach_hang = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.vnpay.vpbankonline:id/edtCustomerCode"]')))
    wait_ma_khach_hang.send_keys(ma_khach_hang)
    wait_tiep_tuc = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//androidx.cardview.widget.CardView[@resource-id="com.vnpay.vpbankonline:id/btnAction"]')))
    wait_tiep_tuc.click()
    so_tien = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.vnpay.vpbankonline:id/tvTotalAmount"]')))
    wait_tiep_tuc2 = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="com.vnpay.vpbankonline:id/tvTitleAction"]')))
    wait_tiep_tuc2.click()
    print("Số tiền: ", so_tien.text)
    driver.quit()


def process_payment(devices, account_name, ma_khach_hang, bank):
    max_threads = len(devices)
    executor = ThreadPoolExecutor(max_workers=max_threads)
    futures = [executor.submit(
        bank, device, account_name, ma_khach_hang) for device in devices]
    for future in futures:
        future.result()


# devices = ["192.168.100.97:5555"]
# account_name = "VISA Shopee Platinum Credit"
# ma_khach_hang = "PD29007350798"
# process_payment(devices, account_name, ma_khach_hang, vpbank)