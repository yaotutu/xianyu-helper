import DriverManager from './driver.js';

class GestureManager {
    static async tap(x, y) {
        const driver = await DriverManager.getDriver();
        await driver.touchAction([
            { action: 'tap', x: x, y: y }
        ]);
    }

    static async swipe(startX, startY, endX, endY, duration = 800) {
        const driver = await DriverManager.getDriver();
        await driver.touchAction([
            { action: 'press', x: startX, y: startY },
            { action: 'wait', ms: duration },
            { action: 'moveTo', x: endX, y: endY },
            { action: 'release' }
        ]);
    }

    static async swipeUp(startPercentage = 0.8, endPercentage = 0.2, duration = 800) {
        const driver = await DriverManager.getDriver();
        const { width, height } = await driver.getWindowSize();

        const startX = width * 0.5;
        const startY = height * startPercentage;
        const endX = width * 0.5;
        const endY = height * endPercentage;

        await this.swipe(startX, startY, endX, endY, duration);
    }

    static async swipeDown(startPercentage = 0.2, endPercentage = 0.8, duration = 800) {
        await this.swipeUp(startPercentage, endPercentage, duration);
    }
}

export default GestureManager; 