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

    async def browse_page(self):
        """浏览详情页"""
        # 配置详情页的浏览参数
        scroll_config = {
            'min_times': 3,      # 最少滑动3次
            'max_times': 5,      # 最多滑动5次
            'up_probability': 0.8,  # 80%概率向上滑动
            'initial_wait': (2, 4),  # 初始等待2-4秒
            'scroll_wait': (1, 3),   # 每次滑动后等待1-3秒
            'final_wait': (2, 4)     # 最后等待2-4秒
        }
        
        return await self.simulate_browse(scroll_config)

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