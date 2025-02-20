from abc import ABC, abstractmethod
from utils.logger import Logger

class BaseTask(ABC):
    """任务基类
    
    所有具体任务都应该继承这个基类，并实现必要的抽象方法。
    基类提供了任务的基本功能，如：
    - 任务名称和描述
    - 任务的运行状态控制
    - 任务的运行和停止
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