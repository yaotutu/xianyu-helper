from typing import Dict, Type
import asyncio
from utils.logger import Logger
from .base_task import BaseTask
from .browse_items_task import BrowseItemsTask

class TaskManager:
    """任务管理器"""
    
    def __init__(self, driver, page_factory):
        self.driver = driver
        self.page_factory = page_factory
        self.current_task = None
        self._task_classes: Dict[str, Type[BaseTask]] = {}
        self._register_tasks()
    
    def _register_tasks(self):
        """注册所有可用任务"""
        self._task_classes = {
            'browse_items': BrowseItemsTask,
            # 后续可以在这里添加更多任务
            # 'playground': PlaygroundTask,
            # 'activity': ActivityTask,
        }
    
    def get_available_tasks(self):
        """获取所有可用任务"""
        tasks = []
        for task_id, task_class in self._task_classes.items():
            task = task_class(self.driver, self.page_factory)
            tasks.append({
                'id': task_id,
                'name': task.name,
                'description': task.description
            })
        return tasks
    
    def stop_current_task(self):
        """停止当前任务"""
        if self.current_task:
            self.current_task.stop()
            self.current_task = None
    
    async def run_task(self, task_id: str):
        """运行指定任务"""
        if task_id not in self._task_classes:
            raise ValueError(f'未知的任务ID: {task_id}')
        
        # 停止当前任务
        self.stop_current_task()
        
        # 创建并运行新任务
        task_class = self._task_classes[task_id]
        self.current_task = task_class(self.driver, self.page_factory)
        
        try:
            await self.current_task.run()
        except Exception as e:
            Logger.error(f'运行任务出错: {task_id}', e)
            raise
        finally:
            self.current_task = None 