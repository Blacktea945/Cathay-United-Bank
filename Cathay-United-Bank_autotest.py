import os
import unittest
import time
import subprocess
import cv2
import numpy as np
import base64
import imutils
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image as PILImage

# 輸出連線裝置的名稱
deviceName = subprocess.check_output(["adb", "devices"]).decode("utf-8")
print(deviceName)

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    # appPackage='com.android.chrome',
    # appActivity='com.google.android.apps.chrome.Main',
    noReset="true",
    # dontStopAppOnReset="true",
    chromedriverExecutable="C:/Users/Bleaktea945/node_modules/appium-chromium-driver/node_modules/appium-chromedriver/chromedriver/win/chromedriver.exe",
)

appium_server_url = 'http://localhost:4723'
driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
time.sleep(2)

# 嘗試點擊Google APP
try:
    # 等待最多 10 秒，直到元素出現
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Chrome")'
        ))
    )
    # 點擊元素
    element.click()
    print("Google APP點擊成功")
except Exception as e:
    print("找不到或已啟動Google APP")

# 嘗試點擊搜尋框
try:
    # 等待最多 10 秒，直到元素出現
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.widget.EditText[@resource-id="com.android.chrome:id/search_box_text"]'
        ))
    )
    # 點擊元素
    element.click()
    print("搜尋框點擊成功")
except Exception as e:
    print("找不到搜尋框:", e)
time.sleep(2)

# 輸入文本
element = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@resource-id="com.android.chrome:id/url_bar"]')
element.send_keys("https://www.cathaybk.com.tw/cathaybk/")
time.sleep(2)

#按下Enter鍵
driver.press_keycode(66)  
time.sleep(2)

# 截圖國泰銀行首頁, 並保存至py啟動位置
driver.save_screenshot("Cathay-United-Bank.png")  
time.sleep(2)

# 嘗試點擊國泰銀行首頁選單列表
try:
    # 等待最多 10 秒，直到元素出現
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description(\"  \").instance(0)'
        ))
    )
    # 點擊元素
    element.click()
    print("選單列表點擊成功")
except Exception as e:
    print("找不到選單列表:", e)

# 嘗試點擊產品介紹
try:
    # 等待最多 10 秒，直到元素出現
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("產品介紹")'
        ))
    )
    # 點擊元素
    element.click()
    print("產品介紹點擊成功")
except Exception as e:
    print("找不到產品介紹:", e)

# 嘗試點擊信用卡列表
try:
    # 等待最多 10 秒，直到元素出現
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((
            AppiumBy.XPATH,
            '//android.widget.EditText[@resource-id="searchBox"], '
        ))
    )
    # 點擊元素
    element.click()
    print("信用卡列表點擊成功 (XPATH)")
except Exception as e:
    try:
        # 使用 UiSelector 搜尋元素
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("信用卡")'
            ))
        )
        # 點擊元素
        element.click()
        print("信用卡列表點擊成功 (UiSelector)")
    except Exception as e:
        print("UiSelector 也找不到信用卡列表:", e)
time.sleep(3)

driver.save_screenshot("Cathay-United-Bank_2.png")  #截圖當前畫面,並保存至py啟動位置
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

# 嘗試點擊卡片介紹
try:
    # 等待最多 10 秒，直到元素出現
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("search").instance(1)'
        ))
    )
    # 點擊元素
    element.click()
    print("卡片介紹點擊成功")
except Exception as e:
    print("找不到卡片介紹:", e)
time.sleep(3)

# 滑動
actions = ActionChains(driver)
actions.w3c_actions.pointer_action.move_to_location(750, 940).pointer_down().move_to_location(100, 940).release()
actions.perform()
time.sleep(3)

# 嘗試點擊停發卡
try:
    # 等待最多 10 秒，直到元素出現
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().description("停發卡")'
        ))
    )
    # 點擊元素
    element.click()
    print("停發卡點擊成功")
except Exception as e:
    print("找不到停發卡:", e)

# 使用圖像辨識計算停發卡有幾張並截圖
stopcard = 0
while True:
    # 1. 截取當前畫面
    screenshot = driver.get_screenshot_as_png()
    # print("步驟 1: 截取當前畫面")

    # 2. 將截圖保存為文件
    filename = 'stopcard_1.png'
    counter = 1
    while os.path.exists(filename):
        filename = f'stopcard_{counter}.png'  # 使用 f-string 動態生成文件名
        counter += 1
    with open(filename, 'wb') as f:
        f.write(screenshot)
    # print(f"步驟 2: 保存截圖為 {filename}")

    # 3. 將截圖轉換為 OpenCV 格式
    nparr = np.frombuffer(screenshot, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)  # 保持彩色圖
    # print("步驟 3: 將截圖轉換為 OpenCV 格式")

    # 4. 向右滑動畫面
    actions = ActionChains(driver)
    actions.w3c_actions.pointer_action.move_to_location(925, 950).pointer_down().move_to_location(200, 950).release()
    actions.perform()
    # print("步驟 4: 向右滑動畫面")
    time.sleep(2)  # 等待滑動完成

    # 5. 截取滑動後的畫面
    new_screenshot = driver.get_screenshot_as_png()
    new_nparr = np.frombuffer(new_screenshot, np.uint8)
    new_img = cv2.imdecode(new_nparr, cv2.IMREAD_COLOR)  # 保持彩色圖
    # print("步驟 5: 截取滑動後的畫面")
    
    # 6. 使用之前的截圖作為模板，在滑動後的畫面中進行匹配
    res = cv2.matchTemplate(new_img, img, cv2.TM_CCOEFF_NORMED)  # 使用彩色圖進行匹配
    threshold = 0.97  # 匹配閾值
    loc = np.where(res >= threshold)
    # print("步驟 6: 進行模板匹配")

    stopcard += 1
    # 7. 檢查是否有匹配結果
    if len(loc[0]) > 0:  # 如果有匹配結果
        print("找到匹配的圖像！")
        break  # 找到匹配，退出循環
    else:  # 如果沒有匹配結果
        print("未找到匹配的圖像，繼續循環...")

# 輸出總共有幾張停發卡
print(f"停發信用卡數量共 {stopcard} 個")


try:
    # 你的測試程式碼
    pass
    print("測試全部完成")
finally:
    # 關閉驅動程式
    driver.quit()
    print("關閉驅動程式")