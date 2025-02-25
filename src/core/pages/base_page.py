from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import asyncio
import re
import random

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

    async def scroll_up(self, distance_ratio=0.5):
        """向上滑动（内容向上移动）
        
        Args:
            distance_ratio: 滑动距离占屏幕高度的比例，默认0.5
        """
        try:
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            
            # 添加一些随机性
            start_x = width * random.uniform(0.4, 0.6)  # 起点x坐标在屏幕中间附近随机
            start_y = height * random.uniform(0.7, 0.8)  # 起点y坐标在屏幕下方随机
            end_x = width * random.uniform(0.4, 0.6)    # 终点x坐标在屏幕中间附近随机
            end_y = height * random.uniform(0.2, 0.3)   # 终点y坐标在屏幕上方随机
            
            # 滑动时间也添加随机性
            duration = random.randint(500, 1500)  # 500-1500毫秒
            
            Logger.debug(f'向上滑动: ({start_x:.0f}, {start_y:.0f}) -> ({end_x:.0f}, {end_y:.0f}), 持续{duration}ms')
            self.driver.swipe(
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                duration=duration
            )
            return True
            
        except WebDriverException as e:
            Logger.error('滑动操作失败', e)
            return False
        except Exception as e:
            Logger.error('滑动时出错', e)
            return False

    async def scroll_down(self, distance_ratio=0.5):
        """向下滑动（内容向下移动）
        
        Args:
            distance_ratio: 滑动距离占屏幕高度的比例，默认0.5
        """
        try:
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            
            # 添加一些随机性
            start_x = width * random.uniform(0.4, 0.6)  # 起点x坐标在屏幕中间附近随机
            start_y = height * random.uniform(0.2, 0.3)  # 起点y坐标在屏幕上方随机
            end_x = width * random.uniform(0.4, 0.6)    # 终点x坐标在屏幕中间附近随机
            end_y = height * random.uniform(0.7, 0.8)   # 终点y坐标在屏幕下方随机
            
            # 滑动时间也添加随机性
            duration = random.randint(500, 1500)  # 500-1500毫秒
            
            Logger.debug(f'向下滑动: ({start_x:.0f}, {start_y:.0f}) -> ({end_x:.0f}, {end_y:.0f}), 持续{duration}ms')
            self.driver.swipe(
                start_x=start_x,
                start_y=start_y,
                end_x=end_x,
                end_y=end_y,
                duration=duration
            )
            return True
            
        except WebDriverException as e:
            Logger.error('滑动操作失败', e)
            return False
        except Exception as e:
            Logger.error('滑动时出错', e)
            return False

    async def simulate_browse(self, scroll_config=None):
        """模拟浏览行为
        
        模拟人工浏览页面的行为，包括：
        - 随机次数的滑动
        - 随机的滑动方向
        - 随机的等待时间
        
        Args:
            scroll_config: 滑动配置，可选，包含以下字段：
                - min_times: 最少滑动次数，默认3
                - max_times: 最多滑动次数，默认5
                - up_probability: 向上滑动的概率，默认0.8
                - initial_wait: (min, max) 初始等待时间范围，默认(2, 4)
                - scroll_wait: (min, max) 每次滑动后等待时间范围，默认(1, 3)
                - final_wait: (min, max) 最终等待时间范围，默认(2, 4)
        
        Returns:
            bool: 是否成功完成所有滑动
        """
        try:
            Logger.debug('===== 开始模拟浏览 =====')
            
            # 默认配置
            config = {
                'min_times': 3,
                'max_times': 5,
                'up_probability': 0.8,
                'initial_wait': (2, 4),
                'scroll_wait': (1, 3),
                'final_wait': (2, 4)
            }
            
            # 更新配置
            if scroll_config:
                config.update(scroll_config)
            
            # 先等待页面加载
            initial_wait = random.uniform(*config['initial_wait'])
            Logger.debug(f'初始等待 {initial_wait:.1f} 秒...')
            await asyncio.sleep(initial_wait)
            
            # 执行随机次数的滑动
            scroll_times = random.randint(config['min_times'], config['max_times'])
            Logger.info(f'计划滑动 {scroll_times} 次')
            
            for i in range(scroll_times):
                try:
                    # 随机决定滑动方向
                    is_scroll_up = random.random() < config['up_probability']
                    
                    # 执行滑动
                    if is_scroll_up:
                        Logger.debug(f'[{i+1}/{scroll_times}] 向上滑动')
                        success = await self.scroll_up()
                    else:
                        Logger.debug(f'[{i+1}/{scroll_times}] 向下滑动')
                        success = await self.scroll_down()
                    
                    if not success:
                        Logger.warn('滑动失败，停止模拟')
                        return False
                    
                    # 随机等待
                    wait_time = random.uniform(*config['scroll_wait'])
                    Logger.debug(f'等待 {wait_time:.1f} 秒...')
                    await asyncio.sleep(wait_time)
                    
                except Exception as e:
                    Logger.error(f'第 {i+1} 次滑动失败', e)
                    continue
            
            # 最后停留一会
            final_wait = random.uniform(*config['final_wait'])
            Logger.debug(f'最后停留 {final_wait:.1f} 秒...')
            await asyncio.sleep(final_wait)
            
            Logger.debug('===== 模拟浏览完成 =====')
            return True
            
        except Exception as e:
            Logger.error('模拟浏览失败', e)
            return False 