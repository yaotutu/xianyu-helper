from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class DetailPage(BasePage):
    # 页面特征元素
    IDENTIFIERS = [
        (AppiumBy.ID, "com.taobao.idlefish:id/detail_title"),
        (AppiumBy.ID, "com.taobao.idlefish:id/price_view"),
    ]

    # 页面元素定位器
    LOCATORS = {
        'title': (AppiumBy.ID, "com.taobao.idlefish:id/detail_title"),
        'price': (AppiumBy.ID, "com.taobao.idlefish:id/price_view"),
        'description': (AppiumBy.ID, "com.taobao.idlefish:id/description"),
        'contact_button': (AppiumBy.ID, "com.taobao.idlefish:id/contact_seller"),
        'favorite_button': (AppiumBy.ID, "com.taobao.idlefish:id/favorite"),
        'back_button': (AppiumBy.ID, "com.taobao.idlefish:id/back"),
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