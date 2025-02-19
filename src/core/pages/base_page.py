from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import asyncio
import re

from utils.logger import Logger

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10  # 默认超时时间（秒）

    async def wait_for_element(self, locator, timeout=None):
        """等待元素出现"""
        timeout = timeout or self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            # 元素未找到时不记录错误，这是正常情况
            return None
        except Exception as e:
            # 其他异常才记录错误
            Logger.error(f"查找元素时出错: {locator}", e)
            return None

    async def find_element_by_content_desc_pattern(self, pattern, timeout=3):
        """使用正则表达式匹配content-desc"""
        try:
            # 首先获取所有可能的元素
            elements = self.driver.find_elements(AppiumBy.XPATH, "//*[@content-desc]")
            for element in elements:
                content_desc = element.get_attribute('content-desc')
                if content_desc and re.match(pattern, content_desc):
                    if element.is_displayed():
                        return element
            return None
        except Exception as e:
            Logger.error(f"查找元素出错: {pattern}", e)
            return None

    async def is_element_present(self, locator, timeout=1):  # 减少默认超时时间
        """检查元素是否存在"""
        try:
            if isinstance(locator, tuple) and len(locator) == 2 and locator[0] == "content-desc-pattern":
                element = await self.find_element_by_content_desc_pattern(locator[1], timeout)
                is_displayed = element is not None
            else:
                element = await self.wait_for_element(locator, timeout)
                is_displayed = element is not None and element.is_displayed()
            
            if is_displayed and element:
                try:
                    text = element.text
                    content_desc = element.get_attribute('content-desc')
                    if text or content_desc:  # 只在有内容时输出日志
                        Logger.debug(f"元素存在 - Text: {text}, Content-desc: {content_desc}")
                except:
                    pass
            return is_displayed
        except:
            return False

    async def get_element_text(self, locator, timeout=None):
        """获取元素文本"""
        element = await self.wait_for_element(locator, timeout)
        return element.text if element else None

    async def click_element(self, locator, timeout=None):
        """点击元素"""
        if isinstance(locator, tuple) and len(locator) == 2 and locator[0] == "content-desc-pattern":
            element = await self.find_element_by_content_desc_pattern(locator[1], timeout)
        else:
            element = await self.wait_for_element(locator, timeout)
        
        if element:
            element.click()
            return True
        return False

    def find_elements_by_text(self, text):
        """通过文本内容查找元素"""
        return self.driver.find_elements(
            AppiumBy.XPATH, 
            f"//*[contains(@text,'{text}')]"
        )

    def find_elements_by_content_desc(self, desc):
        """通过content-desc查找元素"""
        return self.driver.find_elements(
            AppiumBy.XPATH, 
            f"//*[contains(@content-desc,'{desc}')]"
        ) 