#!/usr/bin/env python3
from appium import webdriver
from appium.options.common.base import AppiumOptions
import asyncio
import os

from utils.logger import Logger
from config.app_config import APPIUM_CONFIG
from core.pages.detail_page import DetailPage

async def test_detail_scroll():
    """测试详情页滚动功能"""
    try:
        # 初始化 Appium
        Logger.info('初始化 Appium...')
        options = AppiumOptions()
        for key, value in APPIUM_CONFIG['capabilities'].items():
            options.set_capability(key, value)
        
        driver = webdriver.Remote(
            command_executor='http://localhost:4723',
            options=options
        )
        Logger.success('Appium 连接成功')

        # 创建详情页实例
        detail_page = DetailPage(driver)
        
        try:
            # 等待页面加载
            Logger.info('等待2秒让页面完全加载...')
            await asyncio.sleep(2)
            
            # 执行5次滑动测试
            for i in range(5):
                Logger.info(f'执行第 {i+1} 次滑动测试')
                
                # 直接使用滑动
                window_size = driver.get_window_size()
                width = window_size['width']
                height = window_size['height']
                
                # 从屏幕下方滑动到上方
                start_x = width * 0.5
                start_y = height * 0.8  # 从更靠下的位置开始
                end_x = width * 0.5
                end_y = height * 0.2    # 滑动到更靠上的位置
                
                Logger.debug(f'滑动参数: 从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})')
                driver.swipe(start_x, start_y, end_x, end_y, 1500)  # 增加滑动时间
                
                Logger.success(f'完成第 {i+1} 次滑动')
                await asyncio.sleep(2)  # 等待页面稳定
                
        except Exception as e:
            Logger.error('测试过程出错', e)
            raise
        finally:
            # 清理资源
            Logger.info('测试完成，清理资源...')
            driver.quit()
            
    except Exception as e:
        Logger.error('测试初始化失败', e)
        raise

def main():
    """主函数"""
    try:
        asyncio.run(test_detail_scroll())
    except KeyboardInterrupt:
        Logger.info('测试被用户中断')
    except Exception as e:
        Logger.error('测试执行失败', e)
        raise

if __name__ == '__main__':
    main() 