# -*- coding: utf-8 -*-
# author： wujiang
# datetime： 2021/12/31 15:01
import yaml
import os
import sys
from util.handle_log import Logger
logger=Logger(logger="HandleYaml").getlog()
base_path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
class HandleYaml:
    """
    操作yaml类型的数据
    """
    def load_yaml(self,file):
        """
        加载yaml文件
        """
        files = base_path + file
        try:
            cf=open(files,"r",encoding="utf-8")
            return yaml.load(cf,Loader=yaml.FullLoader)
        except Exception as e:
            logger.error(f"该配置文件：'{files}'不存在。错误信息：{e}")

    def get_data(self,key,file):
        """
        获取数据
        """
        data=self.load_yaml(file)
        if data!=None:
            if key in data.keys():
                result=data.get(key)
                if result!=None:
                    return result
            else:
                logger.error(f"'{key}'值不存在,请检查传递参数的正确性！")
        else:
            return False

handle_yaml=HandleYaml()

if __name__ == '__main__':
    handle_yaml=HandleYaml()
    file="/config/depend_sql.yaml"
    data=handle_yaml.get_data("yanxue_ERP",file)
    print(data)