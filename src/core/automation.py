from appium import webdriver
from appium.options.common.base import AppiumOptions
import asyncio
import os

from utils.logger import Logger
from config.app_config import XIANYU_PACKAGE, XIANYU_ACTIVITY, APPIUM_CONFIG
from core.pages.page_factory import PageFactory
from core.pages.home_page import HomePage
from core.pages.city_service_page import CityServicePage
from core.pages.detail_page import DetailPage
from core.tasks.task_manager import TaskManager

class XianyuAutomation:
    def __init__(self):
        self.driver = None
        self.page_factory = None
        self.task_manager = None
        self.running = True
        
        try:
            Logger.info('初始化自动化配置...')
            options = AppiumOptions()
            for key, value in APPIUM_CONFIG['capabilities'].items():
                options.set_capability(key, value)
            options.set_capability('appPackage', XIANYU_PACKAGE)
            options.set_capability('appActivity', XIANYU_ACTIVITY)
            
            self.appium_host = os.getenv('APPIUM_HOST', APPIUM_CONFIG['host'])
            self.appium_port = int(os.getenv('APPIUM_PORT', APPIUM_CONFIG['port']))
            
            Logger.info(f'连接 Appium 服务器: http://{self.appium_host}:{self.appium_port}')
            self.driver = webdriver.Remote(
                command_executor=f'http://{self.appium_host}:{self.appium_port}',
                options=options
            )
            Logger.success('Appium 连接成功')
            
            # 初始化页面工厂
            self.page_factory = PageFactory(self.driver)
            self.page_factory.register_page(HomePage, HomePage.IDENTIFIERS)
            self.page_factory.register_page(CityServicePage, CityServicePage.IDENTIFIERS)
            self.page_factory.register_page(DetailPage, DetailPage.IDENTIFIERS)
            
            # 初始化任务管理器
            self.task_manager = TaskManager(self.driver, self.page_factory)
            
        except Exception as e:
            Logger.error('初始化失败', e)
            raise

    def stop(self):
        """停止自动化任务"""
        self.running = False
        if self.task_manager:
            self.task_manager.stop_current_task()
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

    async def run(self):
        """运行自动化任务"""
        try:
            Logger.info('=== 开始运行自动化任务 ===')
            
            # 显示可用任务
            available_tasks = self.task_manager.get_available_tasks()
            Logger.info('可用任务:')
            for task in available_tasks:
                Logger.info(f"- {task['name']}: {task['description']}")
            
            # 运行浏览商品任务
            await self.task_manager.run_task('browse_items')
            
        except asyncio.CancelledError:
            Logger.info('任务被取消')
        except Exception as error:
            Logger.error('任务执行出错', error)
        finally:
            await self.cleanup() 