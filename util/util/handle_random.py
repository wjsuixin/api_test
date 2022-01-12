# -*- coding: utf-8 -*-
# author： wujiang
# datetime： 2022/1/6 14:38
from faker import Faker
from util.handle_log import Logger
import json
import re
logger=Logger(logger="HandleRandom").getlog()

class HandleRandom:
    def handle_random_data(self,data):
        match_data=re.findall(r'faker.(.+?)"',data)
        dict={}
        for i in match_data:
            try:
                dict["faker."+i]=self.faker_date(i)
                print(dict)
            except Exception as e:
                logger.error(f"随机数据生成失败。错误信息：{e}")
        return dict

    def faker_date(self,data):
        faker = Faker(locale="zh_CN")
        try:
            return getattr(faker,data)()
        except Exception as e:
            logger.error(f"生成随机的数据失败，请检查！错误信息：{e}")

    def data_replace(self,data):
        for key,value in self.handle_random_data(data).items():
            if data.find(key)!=-1:
                if value!=None:
                    data=data.replace(key,value)
        return data
handle_random=HandleRandom()
if __name__ == '__main__':
    handle_random=HandleRandom()
    data1={"name":"faker.job","description":"faker.s1entence"}
    datas=json.dumps(data1)
    #print(handle_random.faker_date(data1))
    #print(handle_random.handle_random_data(data1))
    print(handle_random.data_replace(datas))
