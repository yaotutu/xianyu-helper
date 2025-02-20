from abc import ABC, abstractmethod
import random
import asyncio
from utils.logger import Logger

class BaseTask(ABC):
    """任务基类
    
    所有具体任务都应该继承这个基类，并实现必要的抽象方法。
    基类提供了任务的基本功能，如：
    - 任务名称和描述
    - 任务的运行状态控制
    - 任务的运行和停止
    - 通用的人工行为模拟
    """
    
    def __init__(self, driver, page_factory):
        """初始化任务
        
        Args:
            driver: Appium WebDriver 实例
            page_factory: 页面工厂实例
        """
        self.driver = driver
        self.page_factory = page_factory
        self.running = True
    
    @property
    @abstractmethod
    def name(self) -> str:
        """任务名称
        
        Returns:
            str: 任务的显示名称
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """任务描述
        
        Returns:
            str: 任务的详细描述
        """
        pass
    
    def stop(self):
        """停止任务
        
        将任务的运行状态设置为 False，任务实现应该在适当的时候检查此状态并停止执行。
        """
        self.running = False
        Logger.info(f'停止任务: {self.name}')
    
    async def simulate_scroll(self, page, scroll_config=None):
        """模拟人工滑动行为
        
        使用页面的基础滑动功能来模拟人工浏览行为，包括：
        - 随机的滑动次数
        - 随机的滑动方向
        - 随机的等待时间
        
        Args:
            page: 页面对象，必须继承自BasePage
            scroll_config: 滑动配置，可选，包含以下字段：
                - min_times: 最少滑动次数，默认2
                - max_times: 最多滑动次数，默认4
                - up_probability: 向上滑动的概率，默认0.7
                - initial_wait: (min, max) 初始等待时间范围，默认(2, 4)
                - scroll_wait: (min, max) 每次滑动后等待时间范围，默认(1, 3)
                - final_wait: (min, max) 最终等待时间范围，默认(2, 4)
        
        Returns:
            bool: 是否成功完成所有滑动
        """
        try:
            # 默认配置
            config = {
                'min_times': 2,
                'max_times': 4,
                'up_probability': 0.7,
                'initial_wait': (2, 4),
                'scroll_wait': (1, 3),
                'final_wait': (2, 4)
            }
            
            # 更新配置
            if scroll_config:
                config.update(scroll_config)
            
            Logger.info('开始模拟浏览行为...')
            
            # 初始等待，假装在看页面内容
            initial_wait = random.uniform(*config['initial_wait'])
            Logger.debug(f'初始停留 {initial_wait:.1f} 秒...')
            await asyncio.sleep(initial_wait)
            
            # 随机决定滑动次数
            scroll_times = random.randint(config['min_times'], config['max_times'])
            Logger.debug(f'计划滑动 {scroll_times} 次')
            
            # 执行滑动
            for i in range(scroll_times):
                # 随机决定滑动方向
                is_scroll_up = random.random() < config['up_probability']
                
                # 使用页面的基础滑动方法
                if is_scroll_up:
                    Logger.debug(f'第 {i+1} 次滑动 - 向上')
                    success = await page.scroll_up()
                else:
                    Logger.debug(f'第 {i+1} 次滑动 - 向下')
                    success = await page.scroll_down()
                
                if not success:
                    Logger.warn('滑动失败，停止模拟')
                    return False
                
                # 滑动后等待，模拟看内容
                wait_time = random.uniform(*config['scroll_wait'])
                Logger.debug(f'停留 {wait_time:.1f} 秒...')
                await asyncio.sleep(wait_time)
            
            # 最后停留一会，表示对内容感兴趣
            final_wait = random.uniform(*config['final_wait'])
            Logger.debug(f'最后停留 {final_wait:.1f} 秒...')
            await asyncio.sleep(final_wait)
            
            Logger.info('完成模拟浏览')
            return True
            
        except Exception as e:
            Logger.error('模拟浏览行为时出错', e)
            return False
    
    @abstractmethod
    async def run(self):
        """运行任务
        
        这是任务的主要执行方法，所有具体任务都必须实现这个方法。
        该方法应该：
        1. 实现任务的主要逻辑
        2. 定期检查 self.running 状态
        3. 适当处理异常
        4. 在结束时进行清理
        """
        pass 