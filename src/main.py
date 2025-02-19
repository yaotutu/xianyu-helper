from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
import asyncio
import os
import signal

from utils.logger import Logger
from config.app_config import XIANYU_PACKAGE, XIANYU_ACTIVITY, SEARCH_CONFIG, APPIUM_CONFIG
from core.home_page import HomePage
from core.item_detail import ItemDetail

class XianyuAutomation:
    def __init__(self):
        self.driver = None
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
            
            self.home_page = HomePage(self.driver)
            self.item_detail = ItemDetail(self.driver)
            
        except Exception as e:
            Logger.error('初始化失败', e)
            raise

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
        await self.item_detail.process_item_detail()

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

async def main():
    automation = XianyuAutomation()
    
    def signal_handler():
        Logger.info('收到中断信号')
        automation.stop()
    
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await automation.run()
    except Exception as e:
        Logger.error('程序异常退出', e)
        raise
    finally:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # 优雅退出，不显示错误堆栈 