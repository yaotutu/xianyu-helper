import asyncio
import sys
from pathlib import Path

# 将 src 目录添加到 Python 路径
src_path = str(Path(__file__).parent.absolute())
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from utils.logger import Logger
from core.automation import XianyuAutomation
from core.signal import SignalHandler

async def run_automation():
    """运行自动化程序的主函数"""
    automation = XianyuAutomation()
    signal_handler = SignalHandler(automation.stop)
    
    try:
        await automation.run()
    except Exception as e:
        Logger.error('程序异常退出', e)
        raise
    finally:
        signal_handler.cleanup()

def main():
    """程序入口函数"""
    try:
        asyncio.run(run_automation())
    except KeyboardInterrupt:
        pass  # 优雅退出，不显示错误堆栈
    except Exception as e:
        Logger.error('程序运行出错', e)
        raise

if __name__ == '__main__':
    main() 