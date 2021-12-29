import configparser
import os,sys
from util.handle_excel import handle_excel
base_path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
class HandleIni:

    def load_ini(self,file_path=None):
        """
        加载ini文件
        """
        if file_path==None:
            file_path=os.path.join(base_path,"config/Base_conf.ini")
        conf=configparser.ConfigParser() # 将对象实例化
        conf.read(file_path,encoding="utf-8") # 读取ini文件
        return conf

    def get_value(self,key,section_name=None,file_path=None):
        """
        获取某一个section下的key对应的Value值
        """
        if section_name==None:
            section_name="columns"
        cf=self.load_ini(file_path)
        data=cf.get(section_name,key) # 获取到section_name下对应key的value值
        return data

    def set_value(self,section,key,value,file_path=None):
        """
        在传入的section中，增加key=Value
        """
        conf=self.load_ini(file_path)
        section_list=conf.sections() # 列出该文件路径下的section列表
        if section not in section_list:
            conf.add_section(section) # 判断传入的section如果不在列表中，则增加该section
        else:
            conf.remove_section(section) # 先清除原有的section，重新加入新的
            conf.add_section(section)
        conf.set(section,key,value) # 在section中设置key=value
        file_open=open(file_path,"w",encoding="utf-8") # 打开ini文件
        conf.write(file_open) # 将设置的key=value写入到ini文件中
        file_open.close() # 关闭ini文件

    def remove_value(self,file_path=None):
        """
        删除section下的key
        """
        conf = self.load_ini(file_path)
        index = int(handle_ini.get_value("index", "SheetIndex"))  # 获取到文件路径下的"SheetIndex"section下的"index"的value
        sheet_name = handle_excel.get_sheet_names()[index]
        conf.remove_section(sheet_name)

handle_ini=HandleIni()

if __name__ == '__main__':
    handle_ini=HandleIni()


