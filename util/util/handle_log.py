# -*- coding: utf-8 -*-
# author： wujiang
# datetime： 2022/1/10 9:48
import logging
import time
import os
import sys
base_path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

class Logger:
    """
    创建日志类
    """
    def __init__(self,logger):

        #创建一个logger
        self.logger=logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        #创建一个handle,用于输出到控制台
        ch=logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        #创建一个hangdle,用于输出日志到文件中
        rq=time.strftime("%Y%m%d%H%M",time.localtime(time.time()))
        file_path=base_path+f"/log/{rq}.txt"
        fh=logging.FileHandler(filename=file_path,encoding="utf-8")
        fh.setLevel(logging.DEBUG)

        #创建handle输入的内容格式
        self.formatter=logging.Formatter("%(asctime)s - %(name)s - %(lineno)d -  %(levelname)s - %(message)s")
        ch.setFormatter(self.formatter)
        fh.setFormatter(self.formatter)

        #将handle添加到logger中
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def getlog(self):
        return self.logger


