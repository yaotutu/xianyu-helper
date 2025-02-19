from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class HomePage(BasePage):
    # 页面特征元素
    IDENTIFIERS = [
        # 使用 content-desc 定位扫一扫按钮
        (AppiumBy.XPATH, "//*[@content-desc='扫一扫']"),
        # 底部导航栏选中的闲鱼tab（使用正则表达式匹配）
        ("content-desc-pattern", r"^闲鱼，未读消息数\d*，选中状态$"),
    ]

    # 页面元素定位器
    LOCATORS = {
        'scan_button': (AppiumBy.XPATH, "//*[@content-desc='扫一扫']"),
        'search_box': (AppiumBy.ID, "com.taobao.idlefish:id/search_term"),  # 这个ID可能会变
        'item_container': (AppiumBy.ID, "com.taobao.idlefish:id/nested_recycler_view"),
        # 底部导航栏
        'home_tab': ("content-desc-pattern", r"^闲鱼，未读消息数\d*，选中状态$"),
    }

    async def is_home_page(self):
        """验证当前是否为首页"""
        # 检查两个特征元素：扫一扫按钮和选中状态的闲鱼tab
        scan_exists = await self.is_element_present(self.LOCATORS['scan_button'])
        home_tab_exists = await self.is_element_present(self.LOCATORS['home_tab'])
        return scan_exists and home_tab_exists

    async def click_scan(self):
        """点击扫一扫按钮"""
        return await self.click_element(self.LOCATORS['scan_button'])

    async def click_search(self):
        """点击搜索框"""
        return await self.click_element(self.LOCATORS['search_box'])

    async def get_item_container(self):
        """获取商品列表容器"""
        return await self.wait_for_element(self.LOCATORS['item_container']) 