const { remote } = require('webdriverio');

const XIANYU_PACKAGE = 'com.taobao.idlefish';

// 定义关键元素选择器
const SELECTORS = {
    ITEM_CONTAINER: 'androidx.recyclerview.widget.RecyclerView',
    ITEM_CONTAINER_ID: 'com.taobao.idlefish:id/nested_recycler_view',
    ITEM_TITLE: 'android.widget.TextView'
};

/**
 * 日志工具
 */
const Logger = {
    info: (message) => {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] [INFO] ${message}`);
    },
    warn: (message) => {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] [WARN] ${message}`);
    },
    error: (message, error) => {
        const timestamp = new Date().toLocaleTimeString();
        console.error(`[${timestamp}] [ERROR] ${message}`);
        if (error?.stack) {
            console.error(`[${timestamp}] [STACK] ${error.stack}`);
        }
    },
    success: (message) => {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] [SUCCESS] ${message}`);
    },
    debug: (message) => {
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] [DEBUG] ${message}`);
    }
};

const capabilities = {
    platformName: 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'Android',
    'appium:noReset': true,
    'appium:appPackage': XIANYU_PACKAGE,
    'appium:dontStopAppOnReset': true,
    'appium:autoLaunch': false
};

const wdOpts = {
    hostname: process.env.APPIUM_HOST || 'localhost',
    port: parseInt(process.env.APPIUM_PORT, 10) || 4723,
    logLevel: 'info',
    capabilities,
};

/**
 * 等待元素加载
 * @param {WebdriverIO.Browser} driver WebdriverIO实例
 * @param {string} selector 元素选择器
 * @param {number} timeout 超时时间（毫秒）
 */
async function waitForElement(driver, selector, timeout = 5000) {
    Logger.debug(`等待元素加载: ${selector}`);
    try {
        await driver.$(selector).waitForExist({ timeout });
        Logger.success(`元素已加载: ${selector}`);
    } catch (error) {
        Logger.error(`等待元素超时: ${selector}`, error);
        throw error;
    }
}

/**
 * 获取商品列表容器
 * @param {WebdriverIO.Browser} driver WebdriverIO实例
 * @returns {Promise<WebdriverIO.Element>} 商品列表容器元素
 */
async function getItemContainer(driver) {
    Logger.debug('尝试获取商品列表容器');
    try {
        // 优先使用 resource-id 定位
        const container = await driver.$(`android=new UiSelector().resourceId("${SELECTORS.ITEM_CONTAINER_ID}")`);
        if (await container.isExisting()) {
            Logger.success('使用 resource-id 成功定位到商品列表容器');
            return container;
        }
        // 备用方案：使用类名定位
        Logger.warn('使用 resource-id 定位失败，尝试使用类名定位');
        const backupContainer = await driver.$(SELECTORS.ITEM_CONTAINER);
        if (await backupContainer.isExisting()) {
            Logger.success('使用类名成功定位到商品列表容器');
            return backupContainer;
        }
        throw new Error('无法定位商品列表容器');
    } catch (error) {
        Logger.error('获取商品列表容器失败', error);
        throw error;
    }
}

/**
 * 获取商品块的标题
 * @param {WebdriverIO.Element} itemElement 商品元素
 * @returns {Promise<string>} 商品标题
 */
async function getItemTitle(itemElement) {
    try {
        Logger.debug('尝试获取商品标题');
        const titleElement = await itemElement.$(SELECTORS.ITEM_TITLE);
        if (await titleElement.isExisting()) {
            const title = await titleElement.getText();
            Logger.success(`成功获取商品标题: ${title}`);
            return title;
        }
        Logger.warn('未找到商品标题元素');
    } catch (error) {
        Logger.error('获取商品标题失败', error);
    }
    return '';
}

/**
 * 检查标题是否符合要求
 * @param {string} title 商品标题
 * @returns {boolean} 是否符合要求
 */
function isTitleMatch(title) {
    const isMatch = title.includes('约尔');
    if (isMatch) {
        Logger.success(`标题匹配成功: ${title}`);
    } else {
        Logger.debug(`标题不匹配: ${title}`);
    }
    return isMatch;
}

/**
 * 滑动页面
 * @param {WebdriverIO.Browser} driver WebdriverIO实例
 */
async function scrollPage(driver) {
    try {
        Logger.debug('准备滑动页面');
        const container = await getItemContainer(driver);

        const result = await driver.execute('mobile: scrollGesture', {
            elementId: container.elementId,
            direction: 'up',
            percent: 0.6
        });

        if (result) {
            Logger.success('页面滑动完成');
        } else {
            Logger.warn('滑动操作未触发，可能已到达页面底部');
        }

        await driver.pause(1500); // 等待页面稳定
    } catch (error) {
        Logger.error('页面滑动失败', error);
        throw error;
    }
}

async function runTest() {
    let driver;
    try {
        Logger.info('=== 开始运行自动化任务 ===');
        driver = await remote(wdOpts);
        Logger.success('WebDriver 会话已创建');

        Logger.info('检查闲鱼是否运行...');
        const currentPackage = await driver.getCurrentPackage();

        if (currentPackage !== XIANYU_PACKAGE) {
            Logger.info('闲鱼未运行，正在启动...');
            await driver.execute('mobile: activateApp', { appId: XIANYU_PACKAGE });
            await driver.pause(5000);
            Logger.success('闲鱼已启动');
        } else {
            Logger.success('闲鱼已在运行');
        }

        await waitForElement(driver, `android=new UiSelector().resourceId("${SELECTORS.ITEM_CONTAINER_ID}")`);
        Logger.success('商品列表已加载，开始处理商品');

        const processedItems = new Set();
        let totalProcessed = 0;
        let totalMatched = 0;

        while (true) {
            const container = await getItemContainer(driver);
            const items = await container.$$('android.widget.FrameLayout');
            Logger.info(`本次扫描发现 ${items.length} 个商品块`);

            let foundNewItem = false;

            for (const item of items) {
                try {
                    const bounds = await item.getAttribute('bounds');
                    if (processedItems.has(bounds)) {
                        continue;
                    }

                    if (!(await item.isDisplayed())) {
                        Logger.debug('跳过不可见商品');
                        continue;
                    }

                    const title = await getItemTitle(item);
                    totalProcessed++;
                    Logger.info(`[${totalProcessed}] 处理商品: ${title}`);

                    if (isTitleMatch(title)) {
                        totalMatched++;
                        Logger.success(`=== 匹配成功 [${totalMatched}/${totalProcessed}] ===`);
                        await item.click();
                        Logger.debug('进入商品详情页');
                        await driver.pause(2000);
                        await driver.back();
                        Logger.debug('返回列表页');
                        await driver.pause(1000);
                    }

                    processedItems.add(bounds);
                    foundNewItem = true;
                } catch (error) {
                    Logger.error('处理商品时出错', error);
                }
            }

            if (!foundNewItem) {
                Logger.info('本页商品处理完毕，准备滑动到下一页');
                await scrollPage(driver);
                processedItems.clear();
                Logger.info(`当前统计 - 总处理: ${totalProcessed}, 匹配成功: ${totalMatched}`);
            }

            await driver.pause(1000);
        }
    } catch (error) {
        Logger.error('任务执行出错', error);
    } finally {
        if (driver) {
            Logger.info('正在关闭会话...');
            await driver.deleteSession();
            Logger.success('会话已关闭');
        }
    }
}

// 添加进程退出处理
process.on('SIGINT', async () => {
    Logger.info('\n收到退出信号，正在清理...');
    process.exit();
});

Logger.info('=== 闲鱼自动化助手启动 ===');
runTest().catch(error => Logger.error('程序异常退出', error));