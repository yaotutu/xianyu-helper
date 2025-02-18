const { remote } = require('webdriverio');

const capabilities = {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'Android',
    'appium:appPackage': 'com.android.settings',
    'appium:appActivity': '.Settings',
};

const wdOpts = {
    hostname: process.env.APPIUM_HOST || 'localhost',
    port: parseInt(process.env.APPIUM_PORT, 10) || 4723,
    logLevel: 'info',
    capabilities,
};

async function runTest() {
    const driver = await remote(wdOpts);
    try {
        // 获取屏幕尺寸
        const screenSize = await driver.getWindowSize();
        console.log(screenSize);
        await driver.pause(2000); // 等待2秒，确保会话已完全建立

        // 滑动屏幕：从 x=500, y=1500 滑动到 x=500, y=500
        driver.touchPerform([
            { action: 'press', options: { x: 100, y: 250 } },
            { action: 'moveTo', options: { x: 300, y: 100 } },
            { action: 'release' }
        ]);

        await driver.deleteSession();

    } catch (error) {
        console.error(error);
    } finally {
        // 延迟并删除会话
        await driver.pause(1000);
        await driver.deleteSession();
    }
}

runTest().catch(console.error);