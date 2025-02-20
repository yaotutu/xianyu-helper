from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import asyncio
from utils.logger import Logger

class DetailPage(BasePage):
    # 页面特征元素 - 只使用已确认的元素
    IDENTIFIERS = [
        (AppiumBy.XPATH, "//android.view.View[@content-desc='卖同款, 卖同款']"),
        (AppiumBy.XPATH, "//android.view.View[@content-desc='我想要, 我想要']")
    ]

    # 页面元素定位器 - 只保留已确认的元素
    LOCATORS = {
        'sell_similar': (AppiumBy.XPATH, "//android.view.View[@content-desc='卖同款, 卖同款']"),
        'want_item': (AppiumBy.XPATH, "//android.view.View[@content-desc='我想要, 我想要']")
    }

    async def scroll_page(self):
        """滚动页面"""
        try:
            Logger.debug('===== 开始执行详情页滑动 =====')
            
            # 获取窗口尺寸
            Logger.debug('获取窗口尺寸...')
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            Logger.debug(f'窗口尺寸: 宽={width}, 高={height}')
            
            # 计算滑动参数
            start_x = width * 0.5
            start_y = height * 0.8
            end_x = width * 0.5
            end_y = height * 0.2
            
            Logger.debug(f'滑动参数: 从 ({start_x:.0f}, {start_y:.0f}) 到 ({end_x:.0f}, {end_y:.0f})')
            Logger.debug('开始执行滑动操作...')
            
            # 执行滑动
            try:
                self.driver.swipe(start_x, start_y, end_x, end_y, 1500)
                Logger.success('滑动操作执行成功')
            except Exception as swipe_error:
                Logger.error(f'滑动操作失败: {str(swipe_error)}')
                Logger.error(f'错误类型: {type(swipe_error).__name__}')
                raise
            
            # 等待页面稳定
            Logger.debug('等待页面稳定 (2秒)...')
            await asyncio.sleep(2)
            Logger.debug('===== 详情页滑动完成 =====')
            
        except Exception as error:
            Logger.error('详情页滑动失败', error)
            Logger.error(f'错误类型: {type(error).__name__}')
            Logger.error(f'错误详情: {str(error)}')
            raise

    async def get_item_info(self):
        """获取商品信息"""
        title = await self.get_element_text(self.LOCATORS['title'])
        price = await self.get_element_text(self.LOCATORS['price'])
        description = await self.get_element_text(self.LOCATORS['description'])
        
        return {
            'title': title,
            'price': price,
            'description': description
        }

    async def contact_seller(self):
        """联系卖家"""
        return await self.click_element(self.LOCATORS['contact_button'])

    async def add_to_favorite(self):
        """收藏商品"""
        return await self.click_element(self.LOCATORS['favorite_button'])

    async def go_back(self):
        """返回上一页"""
        return await self.click_element(self.LOCATORS['back_button'])
    
    async def sell_similar_item(self):
        """点击卖同款"""
        return await self.click_element(self.LOCATORS['sell_similar'])
    
    async def want_this_item(self):
        """点击我想要"""
        return await self.click_element(self.LOCATORS['want_item']) 