import { remote } from 'webdriverio';
import capabilities from '../config/capabilities.js';

class DriverManager {
    static driver = null;

    static async initDriver() {
        if (!this.driver) {
            this.driver = await remote({
                protocol: 'http',
                hostname: '127.0.0.1',
                port: 4723,
                path: '/wd/hub',
                capabilities: capabilities,
                logLevel: 'info'
            });
        }
        return this.driver;
    }

    static async getDriver() {
        if (!this.driver) {
            await this.initDriver();
        }
        return this.driver;
    }

    static async quitDriver() {
        if (this.driver) {
            await this.driver.deleteSession();
            this.driver = null;
        }
    }
}

export default DriverManager; 