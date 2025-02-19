from datetime import datetime
import traceback

class Logger:
    @staticmethod
    def _log(level: str, message: str, error=None):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f'[{timestamp}] [{level}] {message}')
        if error:
            print(f'[{timestamp}] [STACK] {traceback.format_exc()}')

    @classmethod
    def info(cls, message: str):
        cls._log('INFO', message)

    @classmethod
    def warn(cls, message: str):
        cls._log('WARN', message)

    @classmethod
    def error(cls, message: str, error=None):
        cls._log('ERROR', message, error)

    @classmethod
    def success(cls, message: str):
        cls._log('SUCCESS', message)

    @classmethod
    def debug(cls, message: str):
        cls._log('DEBUG', message) 