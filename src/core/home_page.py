from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import asyncio
import time

from utils.logger import Logger
from config.selectors import SELECTORS

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.processed_items = set()

    async def wait_for_element(self, by, value: str, timeout: int = 10000):
        """等待元素加载"""
        Logger.debug(f'等待元素加载: {value}')
        try:
            element = WebDriverWait(self.driver, timeout/1000).until(
                EC.presence_of_element_located((by, value))
            )
            Logger.success(f'元素已加载: {value}')
            return element
        except Exception as error:
            Logger.error(f'等待元素超时: {value}', error)
            try:
                screenshot_path = f'error_screenshot_{int(time.time())}.png'
                self.driver.get_screenshot_as_file(screenshot_path)
                Logger.info(f'错误截图已保存: {screenshot_path}')
            except:
                pass
            raise

    async def get_item_container(self):
        """获取商品列表容器"""
        Logger.debug('尝试获取商品列表容器')
        try:
            container = await self.wait_for_element(
                AppiumBy.ID, 
                SELECTORS['ITEM_CONTAINER']['id']
            )
            if container and container.is_displayed():
                Logger.success('成功定位到商品列表容器')
                return container
            raise Exception('商品列表容器不可见')
        except Exception as error:
            Logger.error('获取商品列表容器失败', error)
            raise

    async def get_items(self, container):
        """获取商品列表"""
        try:
            items = container.find_elements(
                by=AppiumBy.CLASS_NAME, 
                value=SELECTORS['ITEM_FRAME']['class']
            )
            visible_items = [item for item in items if item.is_displayed()]
            Logger.info(f'找到 {len(visible_items)} 个可见商品')
            return visible_items
        except Exception as error:
            Logger.error('获取商品列表失败', error)
            return []

    async def get_item_title(self, item_element):
        """获取商品标题"""
        try:
            Logger.debug('尝试获取商品标题')
            title_elements = item_element.find_elements(
                by=AppiumBy.CLASS_NAME, 
                value=SELECTORS['ITEM_TITLE']['class']
            )
            for title_element in title_elements:
                if title_element.is_displayed():
                    title = title_element.text
                    if title:
                        Logger.success(f'成功获取商品标题: {title}')
                        return title
            Logger.warn('未找到有效的商品标题')
            return ''
        except Exception as error:
            Logger.error('获取商品标题失败', error)
            return ''

    async def scroll_page(self):
        """滚动页面"""
        try:
            Logger.debug('准备滑动页面')
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            
            start_x = width * 0.5
            start_y = height * 0.7
            end_x = width * 0.5
            end_y = height * 0.3
            
            self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
            Logger.success('页面滑动完成')
            await asyncio.sleep(1.5)
            
        except Exception as error:
            Logger.error('页面滑动失败', error)
            raise

    async def browse_items(self, title_matcher, on_item_found=None, should_continue=lambda: True):
        """
        浏览商品列表
        
        Args:
            title_matcher: 标题匹配函数
            on_item_found: 找到匹配商品时的回调函数
            should_continue: 控制是否继续执行的函数
        """
        try:
            # 等待商品列表加载
            container = await self.get_item_container()
            Logger.success('商品列表已加载，开始处理商品')

            total_processed = 0
            while should_continue():
                try:
                    # 获取当前页面的商品
                    items = await self.get_items(container)
                    if not items:
                        Logger.warn('未找到商品，准备滚动页面')
                        await self.scroll_page()
                        continue

                    # 处理当前页面的商品
                    found_new_item = False
                    for item in items:
                        if not should_continue():
                            return
                        processed, total_processed = await self._process_item(
                            item, 
                            total_processed, 
                            title_matcher,
                            on_item_found
                        )
                        found_new_item = found_new_item or processed

                    # 如果当前页面没有新商品，滚动到下一页
                    if not found_new_item:
                        Logger.info('当前页面处理完毕，准备滚动到下一页')
                        await self.scroll_page()
                        self.processed_items.clear()
                        Logger.info(f'当前已处理商品数: {total_processed}')

                    await asyncio.sleep(1)
                except asyncio.CancelledError:
                    Logger.info('浏览任务被取消')
                    return
                except Exception as error:
                    Logger.error('处理页面时出错', error)
                    await asyncio.sleep(1)  # 出错时等待一秒再继续

        except asyncio.CancelledError:
            Logger.info('浏览任务被取消')
            return
        except Exception as error:
            Logger.error('浏览商品失败', error)
            raise

    async def _process_item(self, item, total_processed: int, title_matcher, on_item_found=None):
        """处理单个商品"""
        try:
            bounds = item.get_attribute('bounds')
            if bounds in self.processed_items:
                return False, total_processed
            
            if not item.is_displayed():
                return False, total_processed
            
            title = await self.get_item_title(item)
            if not title:
                return False, total_processed
                
            total_processed += 1
            Logger.info(f'[{total_processed}] 处理商品: {title}')
            
            if title_matcher(title):
                Logger.success(f'=== 匹配成功 [{total_processed}] ===')
                if on_item_found:
                    await on_item_found(item, title)
            
            self.processed_items.add(bounds)
            return True, total_processed
        except Exception as error:
            Logger.error('处理商品时出错', error)
            return False, total_processed 