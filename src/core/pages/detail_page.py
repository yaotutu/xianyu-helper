from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

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