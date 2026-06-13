import logging.handlers

from config import BASE_PATH


def log_config():
    """日志配置"""
    logger = logging.getLogger()
    # 清除已有的handler，避免重复添加
    if logger.handlers:
        logger.handlers.clear()
    """
    CRITICAL: '严重信息',
    ERROR: '错误信息',
    WARNING: '警告信息', # 系统默认级别(CRITICAL+ERROR+WARNING会输出,其他的不会输出!)
    INFO: '普通信息', # 测试常用级别
    DEBUG: '调试信息' # 开发常用
    """
    # 设置输出日志级别
    logger.setLevel(logging.INFO)
    #控制器
    sh=logging.StreamHandler()#输出到控制台（屏幕）
    # 输出到日志文件: RotatingFileHandler()
    fh=logging.handlers.RotatingFileHandler(filename=f'{BASE_PATH}'+'/log/log_test.log',
                                            maxBytes=1024*1024*6,#文件大小
                                            backupCount=3,#保留文件的数量
                                            encoding='utf-8')
    fmt='[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
    formatter=logging.Formatter(fmt)
    #格式器添加到控制器,控制器添加到日志器
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger
if __name__ == '__main__':
    logger=log_config()
    logger.info('开始测试')