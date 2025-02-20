import asyncio
import random
from utils.logger import Logger
from .base_task import BaseTask
from core.pages.home_page import HomePage
from core.pages.detail_page import DetailPage

class BrowseItemsTask(BaseTask):
    """浏览商品任务（养号）"""
    
    @property
    def name(self) -> str:
        return "浏览商品"
    
    @property
    def description(self) -> str:
        return "自动浏览商品详情页，模拟正常用户行为"
    
    async def ensure_home_page(self):
        """确保在首页
        
        如果在详情页则返回，如果在其他页面则等待进入首页
        
        Returns:
            bool: 是否成功进入首页
        """
        try:
            # 首先检查当前页面
            current_page = await self.page_factory.get_current_page()
            
            # 如果在详情页，返回上一页
            if isinstance(current_page, DetailPage):
                Logger.info('当前在详情页，返回首页...')
                self.driver.back()
                await asyncio.sleep(2)
            
            # 等待进入首页
            for _ in range(3):  # 最多尝试3次
                if await self.page_factory.wait_for_page(HomePage, timeout=5):
                    return True
                await asyncio.sleep(2)
            
            return False
            
        except Exception as e:
            Logger.error('确保首页时出错', e)
            return False

    async def browse_detail_page(self, detail_page):
        """浏览详情页
        
        Args:
            detail_page: DetailPage实例
        """
        try:
            Logger.info('===== 开始浏览详情页 =====')
            Logger.info(f'传入的页面类型: {type(detail_page).__name__}')
            
            # 先等待页面加载
            Logger.info('等待详情页加载...')
            await asyncio.sleep(2)
            
            # 检查是否真的在详情页
            current_page = await self.page_factory.get_current_page()
            Logger.info(f'当前页面类型: {type(current_page).__name__}')
            
            if not isinstance(current_page, DetailPage):
                Logger.error('当前不在详情页，跳过浏览')
                return
            
            # 执行3-5次滑动
            scroll_times = random.randint(3, 5)
            Logger.info(f'计划滑动 {scroll_times} 次')
            
            for i in range(scroll_times):
                try:
                    # 滑动页面
                    Logger.info(f'[{i+1}/{scroll_times}] 准备执行滑动...')
                    
                    # 获取滑动前的页面状态
                    try:
                        window_size = detail_page.driver.get_window_size()
                        Logger.debug(f'当前窗口尺寸: {window_size}')
                    except Exception as e:
                        Logger.error('获取窗口尺寸失败', e)
                    
                    # 执行滑动
                    await detail_page.scroll_page()
                    Logger.success(f'[{i+1}/{scroll_times}] 滑动操作执行完成')
                    
                    # 随机等待1-3秒
                    wait_time = random.uniform(1, 3)
                    Logger.debug(f'等待 {wait_time:.1f} 秒...')
                    await asyncio.sleep(wait_time)
                    
                except Exception as scroll_error:
                    Logger.error(f'第 {i+1} 次滑动失败: {str(scroll_error)}')
                    Logger.error(f'错误类型: {type(scroll_error).__name__}')
                    continue  # 继续下一次滑动
            
            # 最后停留2-4秒
            final_wait = random.uniform(2, 4)
            Logger.info(f'浏览完成，最后停留 {final_wait:.1f} 秒')
            await asyncio.sleep(final_wait)
            Logger.info('===== 详情页浏览结束 =====')
            
        except Exception as e:
            Logger.error('浏览详情页时出错', e)
            Logger.error(f'错误类型: {type(e).__name__}')
            Logger.error(f'错误详情: {str(e)}')
    
    async def run(self):
        """运行任务"""
        try:
            Logger.info(f'=== 开始任务: {self.name} ===')
            
            while self.running:
                try:
                    # 确保在首页
                    if not await self.ensure_home_page():
                        Logger.warn('未能进入首页，重试中...')
                        await asyncio.sleep(2)
                        continue
                    
                    home_page = await self.page_factory.get_current_page()
                    if not isinstance(home_page, HomePage):
                        continue
                    
                    # 获取商品列表容器
                    container = await home_page.get_item_container()
                    if not container:
                        Logger.warn('未找到商品列表容器，等待重试...')
                        await asyncio.sleep(2)
                        continue
                    
                    # 获取并处理商品列表
                    items = await home_page.get_items(container)
                    if not items:
                        Logger.info('当前页面没有商品，准备滚动...')
                        await home_page.scroll_page()
                        await asyncio.sleep(2)  # 等待页面加载
                        continue
                    
                    # 处理商品列表
                    for item in items:
                        if not self.running:
                            break
                            
                        try:
                            # 获取商品标题
                            title = await home_page.get_item_title(item)
                            if not title:
                                continue
                                
                            Logger.info(f'浏览商品: {title}')
                            
                            # 点击商品
                            try:
                                if not item.is_displayed():
                                    continue
                                item.click()
                                await asyncio.sleep(2)
                            except Exception as e:
                                Logger.warn(f'点击商品失败: {str(e)}')
                                continue
                            
                            # 等待进入详情页
                            if await self.page_factory.wait_for_page(DetailPage, timeout=5):
                                detail_page = await self.page_factory.get_current_page()
                                if isinstance(detail_page, DetailPage):
                                    # 浏览详情页
                                    await self.browse_detail_page(detail_page)
                                # 返回首页
                                self.driver.back()
                                await asyncio.sleep(2)
                                # 确保返回到首页
                                if not await self.ensure_home_page():
                                    break
                            
                        except Exception as e:
                            Logger.error('处理商品时出错', e)
                            continue
                    
                    # 滚动页面并等待加载
                    await home_page.scroll_page()
                    await asyncio.sleep(2)  # 等待页面加载
                    
                except Exception as e:
                    Logger.error('任务执行出错', e)
                    await asyncio.sleep(2)  # 出错后等待一段时间再重试
                
        except asyncio.CancelledError:
            Logger.info(f'任务被取消: {self.name}')
        except Exception as error:
            Logger.error(f'任务执行出错: {self.name}', error)
        finally:
            Logger.info(f'=== 结束任务: {self.name} ===') 