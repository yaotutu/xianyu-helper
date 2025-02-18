from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
import os
import time

# Appium配置
capabilities = {
    'platformName': 'Android',
    'automationName': 'UiAutomator2',
    'deviceName': 'Android',
    'appPackage': 'com.android.settings',
    'appActivity': '.Settings',
    'noReset': True
}

# WebDriver配置
appium_server_url = "http://127.0.0.1:4723"

def run_test():
    try:
        print("正在连接Appium服务器...")
        print(f"服务器URL: {appium_server_url}")
        print(f"Capabilities: {capabilities}")
        
        # 创建driver实例
        driver = webdriver.Remote(appium_server_url, capabilities)
        print("成功创建driver实例")
        
        # 等待2秒确保会话建立
        time.sleep(2)
        
        # 获取屏幕尺寸
        screen_size = driver.get_window_size()
        print(f"屏幕尺寸: {screen_size}")
        
        # 执行滑动操作
        print("执行滑动操作...")
        
        actions = ActionChains(driver)
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        
        actions.w3c_actions = ActionBuilder(driver, mouse=finger, duration=250)
        actions.w3c_actions.pointer_action.move_to_location(100, 250)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(300, 100)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        
        print("滑动操作完成")
               
        # 等待1秒
        time.sleep(1)
        
    except Exception as e:
        print(f"发生错误: {e}")
        print(f"错误类型: {type(e)}")
        import traceback
        print(f"详细错误信息: {traceback.format_exc()}")
        
    finally:
        # 清理会话
        if 'driver' in locals():
            print("正在关闭driver...")
            driver.quit()
            print("driver已关闭")

if __name__ == '__main__':
    run_test()