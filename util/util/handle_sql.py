# -*- coding: utf-8 -*-
# author： wujiang
# datetime： 2021/12/23 13:59
import os,sys
base_path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
from util.handle_ini import HandleIni
from dbutils.pooled_db import PooledDB
from util.handle_log import Logger
import pymysql
import configparser
import random
logger=Logger(logger="HandleSQl").getlog()

read_ini=HandleIni()
class HandleSQl:
    """
    数据库连接池相关
    """
    def __init__(self,dbName="master",database=None):
        config=configparser.ConfigParser()
        path=os.path.dirname(os.path.dirname(__file__))+"/config/db.conf"
        config.read(path,encoding="UTF-8")
        sections=config.sections()
        #数据库工厂
        dbFactory={}
        for dbName in sections:
            #读取相关属性
            maxconnections=config.get(dbName,"maxconnections")
            mincached=config.get(dbName,"mincached",)
            maxcached=config.get(dbName,"maxcached")
            host=config.get(dbName,"host")
            port=config.get(dbName,"port")
            user=config.get(dbName,"user")
            password=config.get(dbName,"password")
            database=database
            databasePooled=PooledDB(creator=pymysql,
                                    maxconnections=int(maxconnections),
                                    maxcached=int(maxcached),
                                    mincached=int(mincached),
                                    blocking=True,
                                    cursorclass=pymysql.cursors.DictCursor,
                                    host=host,
                                    port=int(port),
                                    user=user,
                                    password=password,
                                    database=database)
            dbFactory[dbName]=databasePooled
            self.connect=dbFactory[dbName].connection()
            self.cursor=self.connect.cursor()
            logger.info(f"获取数据库连接对象成功，连接池对象：{self.connect}")

    def query(self,sql):
        """
        查询数据库
        """
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        return result

    def excute_db(self, sql):
        """更新、删除、插入"""
        try:
            # 使用execute()执行sql
            self.cursor.execute(sql)
            # 提交事物
            self.connect.commit()
        except Exception as e:
            print(f"操作出现错误：{e}")
            # 回滚所有更改
            self.connect.rollback()

if __name__ == '__main__':
    database="yx_common_fat"
    mysql=HandleSQl(database)
    sql="SELECT id,name FROM `yx_common_fat`.`supplier` WHERE `audit_status` = '3' AND `enable_status` LIKE '%1%' LIMIT 0,1000"



