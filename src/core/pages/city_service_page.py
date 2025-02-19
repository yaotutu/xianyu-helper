from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class CityServicePage(BasePage):
    # 页面特征元素
    IDENTIFIERS = [
        # 扫一扫按钮
        (AppiumBy.XPATH, "//*[@content-desc='扫一扫']"),
        # 未选中状态的闲鱼tab（使用正则表达式匹配）
        ("content-desc-pattern", r"^闲鱼，未选中状态$"),
    ]

    # 页面元素定位器
    LOCATORS = {
        'scan_button': (AppiumBy.XPATH, "//*[@content-desc='扫一扫']"),
        'home_tab': ("content-desc-pattern", r"^闲鱼，未选中状态$"),
    }

    async def is_city_service_page(self):
        """验证当前是否为城市服务页面"""
        # 检查扫一扫按钮存在，且闲鱼tab是未选中状态
        scan_exists = await self.is_element_present(self.LOCATORS['scan_button'])
        home_tab_unselected = await self.is_element_present(self.LOCATORS['home_tab'])
        return scan_exists and home_tab_unselected

    async def click_scan(self):
        """点击扫一扫按钮"""
        return await self.click_element(self.LOCATORS['scan_button']) 