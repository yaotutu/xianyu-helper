from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import os
import time
import traceback

XIANYU_PACKAGE = 'com.taobao.idlefish'
XIANYU_ACTIVITY = '.maincontainer.activity.MainFrameworkActivity'

# 定义关键元素选择器
SELECTORS = {
    'ITEM_CONTAINER': {
        'id': 'com.taobao.idlefish:id/nested_recycler_view',
        'class': 'androidx.recyclerview.widget.RecyclerView'
    },
    'ITEM_FRAME': {
        'class': 'android.widget.FrameLayout'
    },
    'ITEM_TITLE': {
        'class': 'android.widget.TextView'
    }
}

class Logger:
    @staticmethod
    def _log(level: str, message: str, error=None):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f'[{timestamp}] [{level}] {message}')
        if error:
            print(f'[{timestamp}] [STACK] {traceback.format_exc()}')

    @classmethod
    def info(cls, message: str):
        cls._log('INFO', message)

    @classmethod
    def warn(cls, message: str):
        cls._log('WARN', message)

    @classmethod
    def error(cls, message: str, error=None):
        cls._log('ERROR', message, error)

    @classmethod
    def success(cls, message: str):
        cls._log('SUCCESS', message)

    @classmethod
    def debug(cls, message: str):
        cls._log('DEBUG', message)

class XianyuAutomation:
    def __init__(self):
        try:
            Logger.info('初始化自动化配置...')
            options = AppiumOptions()
            options.set_capability('platformName', 'Android')
            options.set_capability('automationName', 'UiAutomator2')
            options.set_capability('deviceName', 'Android')
            options.set_capability('noReset', True)
            options.set_capability('appPackage', XIANYU_PACKAGE)
            options.set_capability('appActivity', XIANYU_ACTIVITY)
            options.set_capability('dontStopAppOnReset', True)
            options.set_capability('autoLaunch', True)
            options.set_capability('newCommandTimeout', 60)
            
            self.appium_host = os.getenv('APPIUM_HOST', 'localhost')
            self.appium_port = int(os.getenv('APPIUM_PORT', '4723'))
            
            Logger.info(f'连接 Appium 服务器: http://{self.appium_host}:{self.appium_port}')
            self.driver = webdriver.Remote(
                command_executor=f'http://{self.appium_host}:{self.appium_port}',
                options=options
            )
            Logger.success('Appium 连接成功')
            
            self.processed_items = set()
        except Exception as e:
            Logger.error('初始化失败', e)
            raise

    async def wait_for_element(self, by, value: str, timeout: int = 10000):
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
            # 使用 resource-id 定位
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
            # 遍历所有文本元素，找到商品标题
            for title_element in title_elements:
                if title_element.is_displayed():
                    title = title_element.text
                    if title:  # 确保标题不为空
                        Logger.success(f'成功获取商品标题: {title}')
                        return title
            Logger.warn('未找到有效的商品标题')
            return ''
        except Exception as error:
            Logger.error('获取商品标题失败', error)
            return ''

    def is_title_match(self, title: str) -> bool:
        """检查标题是否匹配搜索条件"""
        is_match = 'chiikawa' in title
        if is_match:
            Logger.success(f'标题匹配成功: {title}')
        else:
            Logger.debug(f'标题不匹配: {title}')
        return is_match

    async def scroll_page(self):
        """滚动页面"""
        try:
            Logger.debug('准备滑动页面')
            
            # 获取屏幕尺寸
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']
            
            # 计算滑动位置
            start_x = width * 0.5
            start_y = height * 0.7
            end_x = width * 0.5
            end_y = height * 0.3
            
            # 执行滑动
            self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
            Logger.success('页面滑动完成')
            time.sleep(1.5)  # 等待页面稳定
            
        except Exception as error:
            Logger.error('页面滑动失败', error)
            raise

    async def process_item(self, item, total_processed: int):
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
            
            if self.is_title_match(title):
                Logger.success(f'=== 匹配成功 [{total_processed}] ===')
                item.click()
                Logger.debug('进入商品详情页')
                time.sleep(5)  # 在详情页停留5秒
                self.driver.back()
                Logger.debug('返回列表页')
                time.sleep(1)
            
            self.processed_items.add(bounds)
            return True, total_processed
        except Exception as error:
            Logger.error('处理商品时出错', error)
            return False, total_processed

    async def run(self):
        try:
            Logger.info('=== 开始运行自动化任务 ===')
            
            # 等待商品列表加载
            container = await self.get_item_container()
            Logger.success('商品列表已加载，开始处理商品')

            total_processed = 0
            while True:
                # 获取当前页面的商品
                items = await self.get_items(container)
                if not items:
                    Logger.warn('未找到商品，准备滚动页面')
                    await self.scroll_page()
                    continue

                # 处理当前页面的商品
                found_new_item = False
                for item in items:
                    processed, total_processed = await self.process_item(item, total_processed)
                    found_new_item = found_new_item or processed

                # 如果当前页面没有新商品，滚动到下一页
                if not found_new_item:
                    Logger.info('当前页面处理完毕，准备滚动到下一页')
                    await self.scroll_page()
                    self.processed_items.clear()  # 清除已处理商品的记录
                    Logger.info(f'当前已处理商品数: {total_processed}')

                time.sleep(1)

        except Exception as error:
            Logger.error('任务执行出错', error)
            raise
        finally:
            if hasattr(self, 'driver'):
                Logger.info('正在关闭会话...')
                self.driver.quit()
                Logger.success('会话已关闭')

if __name__ == '__main__':
    import asyncio
    automation = XianyuAutomation()
    asyncio.run(automation.run()) 