from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common.base import AppiumOptions
import time
import random

class ScrollTest:
    def __init__(self):
        # Appium 配置
        options = AppiumOptions()
        options.set_capability('platformName', 'Android')
        options.set_capability('automationName', 'UiAutomator2')
        options.set_capability('deviceName', 'Android')
        options.set_capability('noReset', True)
        options.set_capability('dontStopAppOnReset', True)
        options.set_capability('autoLaunch', False)
        
        # Appium 服务器配置
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4723',
            options=options
        )
        
        # 设置屏幕尺寸
        self.window_size = self.driver.get_window_size()
        self.width = self.window_size['width']
        self.height = self.window_size['height']

    def scroll_up(self):
        """向上滑动"""
        start_x = self.width * 0.5
        start_y = self.height * 0.7
        end_x = self.width * 0.5
        end_y = self.height * 0.3
        
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
        print("向上滑动")

    def scroll_down(self):
        """向下滑动"""
        start_x = self.width * 0.5
        start_y = self.height * 0.3
        end_x = self.width * 0.5
        end_y = self.height * 0.7
        
        self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
        print("向下滑动")

    def random_scroll(self):
        """随机上下滑动"""
        if random.random() > 0.5:
            self.scroll_up()
        else:
            self.scroll_down()

    def run_test(self, duration_minutes=5):
        """运行测试
        
        Args:
            duration_minutes: 测试持续时间（分钟）
        """
        print(f"开始滑动测试，持续 {duration_minutes} 分钟...")
        end_time = time.time() + (duration_minutes * 60)
        
        scroll_count = 0
        try:
            while time.time() < end_time:
                self.random_scroll()
                scroll_count += 1
                print(f"已完成 {scroll_count} 次滑动")
                # 随机等待 0.5-2 秒
                time.sleep(random.uniform(0.5, 2))
                
        except KeyboardInterrupt:
            print("\n用户中断测试")
        except Exception as e:
            print(f"测试出错: {str(e)}")
        finally:
            print(f"测试结束，共完成 {scroll_count} 次滑动")
            self.driver.quit()

if __name__ == "__main__":
    # 创建测试实例并运行 5 分钟
    test = ScrollTest()
    test.run_test(5)