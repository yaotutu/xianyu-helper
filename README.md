# 闲鱼自动化助手

这是一个基于 Python 和 Appium 的闲鱼自动化工具，用于自动浏览和筛选闲鱼商品。

## 环境要求

- Python 3.7+
- Appium Server
- Android 设备或模拟器
- ADB 工具

## 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd xianyu-helper
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 确保 Appium 服务器已启动：
```bash
appium
```

## 配置

1. 确保 Android 设备已通过 USB 调试模式连接，或者模拟器已运行
2. 可以通过环境变量配置 Appium 服务器地址：
   - `APPIUM_HOST`: Appium 服务器地址（默认：localhost）
   - `APPIUM_PORT`: Appium 服务器端口（默认：4723）

## 使用

运行主程序：
```bash
python src/main.py
```

## 功能

- 自动检测并启动闲鱼应用
- 自动滚动浏览商品列表
- 根据标题关键词匹配商品
- 自动进入匹配商品详情页
- 详细的日志记录

## 注意事项

1. 使用前请确保闲鱼应用已安装在设备上
2. 确保设备已解锁并保持亮屏状态
3. 建议在使用过程中不要手动操作设备 