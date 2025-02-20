from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from .base_page import BasePage
import asyncio

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

    async def get_items(self, container, max_retries=3):
        """获取商品列表，带重试机制
        
        Args:
            container: 商品列表容器元素
            max_retries: 最大重试次数
            
        Returns:
            list: 商品元素列表
        """
        for attempt in range(max_retries):
            try:
                # 确保容器可见
                if not container.is_displayed():
                    return []
                
                # 获取商品列表
                items = container.find_elements(
                    by=AppiumBy.CLASS_NAME,
                    value="android.widget.FrameLayout"  # 直接使用类名而不是从配置读取
                )
                
                # 过滤出可见的商品
                visible_items = [
                    item for item in items 
                    if item.is_displayed()
                ]
                
                return visible_items
                
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                    # 重新获取容器
                    container = await self.wait_for_element(self.LOCATORS['item_container'])
                    if not container:
                        return []
                continue
            except Exception as e:
                self.logger.error('获取商品列表失败', e)
                return []
        
        return []

    async def get_item_container(self, max_retries=3):
        """获取商品列表容器，带重试机制"""
        for attempt in range(max_retries):
            try:
                container = await self.wait_for_element(self.LOCATORS['item_container'])
                if container and container.is_displayed():
                    return container
            except Exception as e:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                continue
        return None

    async def get_item_title(self, item, max_retries=3):
        """获取商品标题，带重试机制"""
        for attempt in range(max_retries):
            try:
                if not item.is_displayed():
                    return None
                    
                title_elements = item.find_elements(
                    by=AppiumBy.CLASS_NAME,
                    value="android.widget.TextView"
                )
                
                for title_element in title_elements:
                    if title_element.is_displayed():
                        title = title_element.text
                        if title:
                            return title
                return None
                
            except StaleElementReferenceException:
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                continue
            except Exception as e:
                self.logger.error('获取商品标题失败', e)
                return None
        
        return None 