#!/usr/bin/env python3
from appium import webdriver
from appium.options.common.base import AppiumOptions
import asyncio
import signal
import os

from utils.logger import Logger
from config.app_config import APPIUM_CONFIG
from core.pages.page_factory import PageFactory
from core.pages.home_page import HomePage
from core.pages.city_service_page import CityServicePage
from core.pages.detail_page import DetailPage

class PageMonitor:
    def __init__(self):
        self.driver = None
        self.page_factory = None
        self.running = True
        self._last_page_type = None

    async def setup(self):
        """初始化 Appium"""
        try:
            Logger.info('初始化自动化配置...')
            options = AppiumOptions()
            for key, value in APPIUM_CONFIG['capabilities'].items():
                options.set_capability(key, value)
            
            self.driver = webdriver.Remote(
                command_executor=f'http://localhost:4723',
                options=options
            )
            Logger.success('Appium 连接成功')

            # 初始化页面工厂
            self.page_factory = PageFactory(self.driver)
            self.page_factory.register_page(HomePage, HomePage.IDENTIFIERS)
            self.page_factory.register_page(CityServicePage, CityServicePage.IDENTIFIERS)
            self.page_factory.register_page(DetailPage, DetailPage.IDENTIFIERS)
            
            return True
        except Exception as e:
            Logger.error('初始化失败', e)
            return False

    def stop(self):
        """停止监控"""
        if self.running:
            self.running = False
            Logger.info('正在停止监控...')

    async def cleanup(self):
        """清理资源"""
        if self.driver:
            try:
                Logger.info('正在关闭会话...')
                self.driver.quit()
                Logger.success('会话已关闭')
            except Exception as e:
                Logger.error('关闭会话时出错', e)

    async def monitor_pages(self):
        """监控页面状态"""
        try:
            Logger.info('=== 开始页面监控 ===')
            Logger.info('提示：按 Ctrl+C 停止监控')
            
            while self.running:
                try:
                    current_page = await self.page_factory.get_current_page()
                    current_type = type(current_page) if current_page else None
                    
                    # 只在页面类型发生变化时输出日志
                    if current_type != self._last_page_type:
                        if isinstance(current_page, HomePage):
                            Logger.info('当前页面: 首页')
                        elif isinstance(current_page, CityServicePage):
                            Logger.info('当前页面: 城市服务页面')
                        elif isinstance(current_page, DetailPage):
                            Logger.info('当前页面: 商品详情页')
                        else:
                            Logger.debug('当前页面: 未知页面')
                        self._last_page_type = current_type
                    
                    await asyncio.sleep(1)  # 缩短检查间隔，提高响应性
                except Exception as e:
                    Logger.error('页面检查出错', e)
                    await asyncio.sleep(1)

        except asyncio.CancelledError:
            Logger.info('监控被取消')
        except Exception as error:
            Logger.error('监控出错', error)
        finally:
            await self.cleanup()

async def main():
    monitor = PageMonitor()
    
    def signal_handler():
        monitor.stop()
    
    if not await monitor.setup():
        return
    
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await monitor.monitor_pages()
    except Exception as e:
        Logger.error('程序异常退出', e)
    finally:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # 优雅退出，不显示错误堆栈 