import os
import time
import subprocess
import cv2
import numpy as np
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.action_chains import ActionChains


capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    # appPackage='com.android.chrome',
    # appActivity='com.google.android.apps.chrome.Main',
    noReset="true",
    # dontStopAppOnReset="true",
    # chromedriverExecutable="C:/Users/Bleaktea945/node_modules/appium-chromium-driver/node_modules/appium-chromedriver/chromedriver/win/chromedriver.exe",
)

appium_server_url = 'http://localhost:4723'
driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

deviceName = subprocess.check_output("adb devices").decode("utf-8")
print("-", deviceName)

def click_element(locat):
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, locat))).click()
    except Exception:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((AppiumBy.XPATH, locat))).click()
    except Exception as e:
        print(e)

def send_keys(xpath, keys):
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath))).send_keys(keys)
    except Exception as e:
        print(e)

chrome = click_element('new UiSelector().text("Chrome")')

search = click_element('//android.widget.EditText[@resource-id="com.android.chrome:id/search_box_text"]')

url = send_keys('//android.widget.EditText[@resource-id="com.android.chrome:id/url_bar"]', "https://www.cathaybk.com.tw/cathaybk/")

driver.press_keycode(66)  
time.sleep(2)

driver.save_screenshot("Cathay-United-Bank.png")  
time.sleep(2)

menu = click_element('new UiSelector().description(\"  \").instance(0)')

product = click_element('new UiSelector().text("產品介紹")')

card = click_element('new UiSelector().text("信用卡")')
time.sleep(2)

driver.save_screenshot("Cathay-United-Bank_2.png")
time.sleep(2)

# 嘗試計算信用卡選單下面有多少個項目
try:
    # 等待最多 10 秒，直到父層元素出現
    parent_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.view.View").instance(36)'
        ))
    )

    # 搜尋父層底下所有 resource-id 包含 "lnk_Link" 的子元素
    child_elements_with_lnk_link = parent_element.find_elements(
        AppiumBy.XPATH, './/*[contains(@resource-id, "lnk_Link")]'
    )

    # 打印符合條件的子元素數量
    child_count = len(child_elements_with_lnk_link)
    print("信用卡選單下面共有:", child_count, "項目")

except Exception as e:
    print("找不到項目:", e)

cardIntro = click_element('new UiSelector().description("search").instance(1)')
time.sleep(2)

# 滑動
actions = ActionChains(driver)
actions.w3c_actions.pointer_action.move_to_location(750, 940).pointer_down().move_to_location(100, 940).release()
actions.perform()

cardIntro = click_element('new UiSelector().description("停發卡")')

time.sleep(2)

# 使用圖像辨識計算停發卡有幾張並截圖
stopcard = 0
while True:
    # 1. 截取當前畫面
    screenshot = driver.get_screenshot_as_png()

    # 2. 將截圖保存為文件
    filename = 'stopcard_1.png'
    counter = 1
    while os.path.exists(filename):
        filename = f'stopcard_{counter}.png'
        counter += 1
    with open(filename, 'wb') as f:
        f.write(screenshot)

    # 3. 將截圖轉換為 OpenCV 格式
    nparr = np.frombuffer(screenshot, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # 4. 向右滑動畫面
    actions = ActionChains(driver)
    actions.w3c_actions.pointer_action.move_to_location(925, 950).pointer_down().move_to_location(200, 950).release()
    actions.perform()
    time.sleep(2)  # 等待滑動完成

    # 5. 截取滑動後的畫面
    new_screenshot = driver.get_screenshot_as_png()
    new_nparr = np.frombuffer(new_screenshot, np.uint8)
    new_img = cv2.imdecode(new_nparr, cv2.IMREAD_COLOR)  
    
    # 6. 使用之前的截圖作為模板，在滑動後的畫面中進行匹配
    res = cv2.matchTemplate(new_img, img, cv2.TM_CCOEFF_NORMED)  # 使用彩色圖進行匹配
    threshold = 0.97  # 匹配閾值
    loc = np.where(res >= threshold)

    stopcard += 1
    # 7. 檢查是否有匹配結果
    if len(loc[0]) > 0:  # 如果有匹配結果
        print("找到匹配的圖像！")
        break  # 找到匹配，退出循環
    else:  # 如果沒有匹配結果
        print("未找到匹配的圖像，繼續循環...")

# 輸出總共有幾張停發卡
print(f"停發信用卡數量共 {stopcard} 個")

print("測試全部完成")
driver.quit()
print("關閉驅動程式")