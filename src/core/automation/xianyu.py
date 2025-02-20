from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import os
import random

from utils.logger import Logger
from config.app_config import XIANYU_PACKAGE, XIANYU_ACTIVITY, SEARCH_CONFIG, APPIUM_CONFIG
from core.home_page import HomePage
from core.pages.detail_page import DetailPage

class XianyuAutomation:
    def __init__(self, driver=None):
        """初始化闲鱼自动化
        
        Args:
            driver: 可选，Appium WebDriver 实例
        """
        self.driver = driver
        self.running = True
        
        if not self.driver:
            try:
                Logger.info('初始化 Appium...')
                options = AppiumOptions()
                for key, value in APPIUM_CONFIG['capabilities'].items():
                    options.set_capability(key, value)
                options.set_capability('appPackage', XIANYU_PACKAGE)
                options.set_capability('appActivity', XIANYU_ACTIVITY)
                
                self.driver = webdriver.Remote(
                    command_executor='http://localhost:4723',
                    options=options
                )
                Logger.success('Appium 连接成功')
                
            except Exception as e:
                Logger.error('初始化失败', e)
                raise
        
        # 初始化页面对象
        self.home_page = HomePage(self.driver)
        self.detail_page = DetailPage(self.driver)

    def stop(self):
        """停止自动化任务"""
        self.running = False
        Logger.info('正在停止自动化任务...')

    async def cleanup(self):
        """清理资源"""
        if self.driver:
            try:
                Logger.info('正在关闭会话...')
                self.driver.quit()
                Logger.success('会话已关闭')
            except Exception as e:
                Logger.error('关闭会话时出错', e)

    def title_matcher(self, title: str) -> bool:
        """标题匹配函数"""
        if not SEARCH_CONFIG['case_sensitive']:
            title = title.lower()
            keywords = [k.lower() for k in SEARCH_CONFIG['keywords']]
        else:
            keywords = SEARCH_CONFIG['keywords']

        for keyword in keywords:
            if keyword in title:
                Logger.success(f'标题匹配成功: {title} (匹配关键词: {keyword})')
                return True
        
        Logger.debug(f'标题不匹配: {title}')
        return False

    async def on_item_found(self, item, title):
        """找到匹配商品时的回调函数"""
        if not self.running:
            return
        item.click()
        await self.process_item_detail()

    async def run(self):
        """运行自动化任务"""
        try:
            Logger.info('=== 开始运行自动化任务 ===')
            await self.home_page.browse_items(
                title_matcher=self.title_matcher,
                on_item_found=self.on_item_found,
                should_continue=lambda: self.running
            )
        except asyncio.CancelledError:
            Logger.info('任务被取消')
        except KeyboardInterrupt:
            Logger.info('用户中断任务')
        except Exception as error:
            Logger.error('任务执行出错', error)
        finally:
            await self.cleanup()

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
            raise

    async def process_item_detail(self):
        """处理商品详情页"""
        try:
            Logger.debug('进入商品详情页')
            await asyncio.sleep(2)  # 等待页面加载
            
            # 执行3-5次滑动
            scroll_times = random.randint(3, 5)
            Logger.info(f'计划滑动 {scroll_times} 次')
            
            for i in range(scroll_times):
                try:
                    await self.detail_page.scroll_page()
                    Logger.success(f'完成第 {i+1}/{scroll_times} 次滑动')
                    
                    # 随机等待1-3秒
                    wait_time = random.uniform(1, 3)
                    await asyncio.sleep(wait_time)
                    
                except Exception as e:
                    Logger.error(f'滑动失败: {str(e)}')
                    continue
            
            # 最后停留2-4秒
            final_wait = random.uniform(2, 4)
            await asyncio.sleep(final_wait)
            
            self.driver.back()
            Logger.debug('返回列表页')
            await asyncio.sleep(1)
            
            return True
        except asyncio.CancelledError:
            Logger.info('详情页处理被取消')
            return False
        except Exception as error:
            Logger.error('处理商品详情页失败', error)
            return False 