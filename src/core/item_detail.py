from appium.webdriver.common.appiumby import AppiumBy
import asyncio
from utils.logger import Logger
from config.selectors import SELECTORS
from core.pages.detail_page import DetailPage

class ItemDetail:
    def __init__(self, driver):
        self.driver = driver
        self.detail_page = DetailPage(driver)

    async def process_item_detail(self):
        """处理商品详情页"""
        try:
            Logger.debug('进入商品详情页')
            await asyncio.sleep(2)  # 等待页面加载
            
            # 使用DetailPage的浏览方法
            success = await self.detail_page.browse_page()
            if not success:
                Logger.warn('详情页浏览异常')
            
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