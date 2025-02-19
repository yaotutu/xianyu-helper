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
        # 首先检查当前页面是否仍然有效
        if self.current_page:
            page = self._get_page_instance(self.current_page.__class__)
            # 只检查第一个标识符，提高效率
            first_identifier = self._page_identifiers[self.current_page.__class__][0]
            try:
                if await page.is_element_present(first_identifier, timeout=1):
                    return self.current_page
            except Exception:
                pass

        # 如果当前页面无效，则检查所有已注册的页面
        Logger.debug("开始识别当前页面...")
        
        for page_class, identifiers in self._page_identifiers.items():
            if not identifiers:
                continue
                
            page = self._get_page_instance(page_class)
            # 只检查第一个标识符
            first_identifier = identifiers[0]
            
            try:
                if await page.is_element_present(first_identifier, timeout=1):
                    # 如果找到第一个标识符，再检查其他标识符
                    all_present = True
                    for locator in identifiers[1:]:
                        if not await page.is_element_present(locator, timeout=1):
                            all_present = False
                            break
                    
                    if all_present:
                        if self.current_page != page:
                            Logger.info(f"页面切换: {page_class.__name__}")
                            self.current_page = page
                        return page
            except Exception as e:
                Logger.debug(f"检查页面 {page_class.__name__} 时出错: {str(e)}")
                continue
        
        self.current_page = None
        Logger.debug("无法识别当前页面")
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