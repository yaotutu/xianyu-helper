import asyncio
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
    
    async def run(self):
        """运行任务"""
        try:
            Logger.info(f'=== 开始任务: {self.name} ===')
            
            while self.running:
                try:
                    # 等待进入首页
                    if not await self.page_factory.wait_for_page(HomePage, timeout=10):
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
                                # 在详情页停留一段时间
                                await asyncio.sleep(5)
                                # 返回首页
                                self.driver.back()
                                await asyncio.sleep(2)
                                # 重新获取首页
                                await self.page_factory.wait_for_page(HomePage, timeout=5)
                            
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