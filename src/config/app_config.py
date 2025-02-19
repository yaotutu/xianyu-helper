# 应用配置
XIANYU_PACKAGE = 'com.taobao.idlefish'
XIANYU_ACTIVITY = '.maincontainer.activity.MainFrameworkActivity'

# 搜索配置
SEARCH_CONFIG = {
    'keywords': ['chiikawa', '奇卡瓦'],  # 在这里添加要匹配的关键词，支持多个关键词
    'case_sensitive': False,  # 是否区分大小写
}

# Appium 配置
APPIUM_CONFIG = {
    'host': 'localhost',
    'port': 4723,
    'capabilities': {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': 'Android',
        'noReset': True,
        'dontStopAppOnReset': True,
        'autoLaunch': True,
        'newCommandTimeout': 60
    }
} 