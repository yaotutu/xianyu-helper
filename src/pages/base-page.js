import DriverManager from '../core/driver.js';
import GestureManager from '../core/gesture.js';

class BasePage {
    constructor() {
        this.driver = null;
    }

    async initialize() {
        this.driver = await DriverManager.getDriver();
    }

    /**
     * 等待元素可见
     * @param {string} selector 元素选择器
     * @param {number} timeout 超时时间（毫秒）
     * @returns {Promise<boolean>} 是否找到元素
     */
    async waitForElement(selector, timeout = 10000) {
        try {
            const element = await this.driver.$(selector);
            await element.waitForDisplayed({ timeout });
            return true;
        } catch (error) {
            return false;
        }
    }

    /**
     * 通过多种定位策略查找元素
     * @param {Object} locators 多种定位策略的选择器
     * @returns {Promise<WebdriverIO.Element|null>} 找到的元素或null
     */
    async findElementByMultipleLocators(locators) {
        const strategies = [
            { type: 'accessibility id', selector: locators.accessibilityId },
            { type: 'id', selector: locators.resourceId },
            { type: 'xpath', selector: locators.xpath },
            { type: 'class name', selector: locators.className }
        ];

        for (const strategy of strategies) {
            if (!strategy.selector) continue;

            try {
                const element = await this.driver.$(`${strategy.type}:${strategy.selector}`);
                if (await element.isDisplayed()) {
                    return element;
                }
            } catch (error) {
                continue;
            }
        }
        return null;
    }

    /**
     * 点击元素
     * @param {Object} locators 元素定位器
     * @param {number} retries 重试次数
     * @returns {Promise<boolean>} 是否点击成功
     */
    async clickElement(locators, retries = 3) {
        for (let i = 0; i < retries; i++) {
            try {
                const element = await this.findElementByMultipleLocators(locators);
                if (element) {
                    await element.click();
                    return true;
                }

                // 如果找不到元素，尝试滚动页面
                if (i < retries - 1) {
                    await GestureManager.swipeUp();
                }
            } catch (error) {
                if (i === retries - 1) {
                    console.error('Failed to click element:', error);
                    return false;
                }
            }
        }
        return false;
    }

    /**
     * 获取元素文本
     * @param {Object} locators 元素定位器
     * @returns {Promise<string|null>} 元素文本或null
     */
    async getElementText(locators) {
        try {
            const element = await this.findElementByMultipleLocators(locators);
            if (element) {
                return await element.getText();
            }
        } catch (error) {
            console.error('Failed to get element text:', error);
        }
        return null;
    }

    /**
     * 检查元素是否存在
     * @param {Object} locators 元素定位器
     * @returns {Promise<boolean>} 元素是否存在
     */
    async isElementPresent(locators) {
        const element = await this.findElementByMultipleLocators(locators);
        return element !== null;
    }

    /**
     * 等待元素消失
     * @param {Object} locators 元素定位器
     * @param {number} timeout 超时时间（毫秒）
     * @returns {Promise<boolean>} 元素是否消失
     */
    async waitForElementToDisappear(locators, timeout = 10000) {
        const startTime = Date.now();
        while (Date.now() - startTime < timeout) {
            const isPresent = await this.isElementPresent(locators);
            if (!isPresent) {
                return true;
            }
            await new Promise(resolve => setTimeout(resolve, 500));
        }
        return false;
    }
}

export default BasePage; 