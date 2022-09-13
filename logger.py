import logging
import os
import time

myloger = None

def __logger_config__():
    '''
    配置log
    :return:
    '''
    '''
    logger是日志对象，handler是流处理器，console是控制台输出（没有console也可以，将不会在控制台输出，会在日志文件中输出）
    '''
    #log_path = os.getenv("TEST_BASE") + "/log/test_" + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    # log_path =  "E:\\work\\test\\log\\test_" + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    log_path =  os.getcwd() + "/log/test_" + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    logging_name = "AutoTest_" + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    # 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
    logger.setLevel(level=logging.DEBUG)
    # 获取文件日志句柄并设置日志级别，第二层过滤
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # console相当于控制台输出，handler文件输出。获取流句柄并设置日志级别，第二层过滤
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 为logger对象添加句柄
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger

def __createinstance__():
    global myloger
    if myloger is None:
        myloger = __logger_config__()
    return myloger

__createinstance__()