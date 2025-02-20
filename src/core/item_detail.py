from appium.webdriver.common.appiumby import AppiumBy
import asyncio
import random
from utils.logger import Logger
from config.selectors import SELECTORS

class ItemDetail:
    def __init__(self, driver):
        self.driver = driver

    async def process_item_detail(self):
        """处理商品详情页"""
        try:
            Logger.debug('进入商品详情页')
            await asyncio.sleep(2)  # 等待页面加载
            
            # 执行3-5次滑动
            scroll_times = random.randint(3, 5)
            Logger.info(f'计划滑动 {scroll_times} 次')
            
            for i in range(scroll_times):
                try:
                    # 获取窗口尺寸
                    window_size = self.driver.get_window_size()
                    width = window_size['width']
                    height = window_size['height']
                    
                    # 从屏幕下方滑动到上方
                    start_x = width * 0.5
                    start_y = height * 0.8
                    end_x = width * 0.5
                    end_y = height * 0.2
                    
                    Logger.debug(f'执行第 {i+1}/{scroll_times} 次滑动')
                    self.driver.swipe(start_x, start_y, end_x, end_y, 1500)
                    Logger.success(f'完成第 {i+1} 次滑动')
                    
                    # 随机等待1-3秒
                    wait_time = random.uniform(1, 3)
                    await asyncio.sleep(wait_time)
                    
                except Exception as e:
                    Logger.error(f'滑动失败: {str(e)}')
                    continue
            
            # 最后停留2-4秒
            final_wait = random.uniform(2, 4)
            await asyncio.sleep(final_wait)
            
            self.driver.back()
            Logger.debug('返回列表页')
            await asyncio.sleep(1)
            
            return True
        except asyncio.CancelledError:
            Logger.info('详情页处理被取消')
            return False
        except Exception as error:
            Logger.error('处理商品详情页失败', error)
            return False 