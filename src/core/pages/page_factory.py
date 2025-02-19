import asyncio
from utils.logger import Logger

class PageFactory:
    def __init__(self, driver):
        self.driver = driver
        self.current_page = None
        self._pages = {}  # 页面实例缓存
        self._page_identifiers = {}  # 页面标识符配置

    def register_page(self, page_class, identifiers):
        """
        注册页面类及其标识符
        
        Args:
            page_class: 页面类
            identifiers: 页面标识符列表，每个标识符是 (定位方式, 定位值) 的元组
        """
        self._page_identifiers[page_class] = identifiers
        Logger.debug(f"注册页面类: {page_class.__name__}")

    async def get_current_page(self):
        """识别当前页面并返回对应的页面对象"""
        Logger.debug("开始识别当前页面...")
        
        for page_class, identifiers in self._page_identifiers.items():
            Logger.debug(f"检查是否为 {page_class.__name__}...")
            
            for locator in identifiers:
                try:
                    page = self._get_page_instance(page_class)
                    Logger.debug(f"检查特征元素: {locator}")
                    if await page.is_element_present(locator, timeout=2):
                        Logger.debug(f"✓ 找到特征元素: {locator}")
                    else:
                        Logger.debug(f"✗ 未找到特征元素: {locator}")
                        break
                except Exception as e:
                    Logger.debug(f"检查特征元素出错: {locator}, 错误: {str(e)}")
                    break
            else:
                # 所有特征元素都找到了
                if self.current_page != page:
                    Logger.info(f"页面切换: {page_class.__name__}")
                    self.current_page = page
                return page
        
        Logger.warn("无法识别当前页面")
        return None

    def _get_page_instance(self, page_class):
        """获取或创建页面实例"""
        if page_class not in self._pages:
            self._pages[page_class] = page_class(self.driver)
        return self._pages[page_class]

    async def wait_for_page(self, expected_page_class, timeout=10):
        """
        等待直到出现指定页面
        
        Args:
            expected_page_class: 期望的页面类
            timeout: 超时时间（秒）
        
        Returns:
            bool: 是否成功等待到指定页面
        """
        start_time = asyncio.get_event_loop().time()
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            current_page = await self.get_current_page()
            if isinstance(current_page, expected_page_class):
                return True
            await asyncio.sleep(0.5)
        return False 