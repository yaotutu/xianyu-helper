import asyncio
import signal
from typing import Callable

from utils.logger import Logger

class SignalHandler:
    """信号处理器类，用于管理程序的信号处理逻辑"""
    def __init__(self, stop_callback: Callable[[], None]):
        self.loop = asyncio.get_running_loop()
        self.stop_callback = stop_callback
        self._setup_handlers()
    
    def _setup_handlers(self):
        """设置信号处理器"""
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.loop.add_signal_handler(sig, self._signal_handler)
        Logger.info('信号处理器已设置')
    
    def _signal_handler(self):
        """信号处理函数"""
        Logger.info('收到中断信号')
        self.stop_callback()
    
    def cleanup(self):
        """清理信号处理器"""
        for sig in (signal.SIGINT, signal.SIGTERM):
            self.loop.remove_signal_handler(sig)
        Logger.info('信号处理器已清理') 