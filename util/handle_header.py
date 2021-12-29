import os,sys
from util.handle_ini import handle_ini
from util.handle_excel import handle_excel
base_path=os.path.dirname(os.path.dirname(__file__))
file_path=os.path.join(base_path,"config/header.ini")
sys.path.append(base_path)
def get_token(data):
    """
    获取token值
    """
    token=data["data"]["token"]
    return token

def write_token(data):
    """
    将获取到的token，写入到header.ini文件中
    """
    index=int(handle_ini.get_value("index","SheetIndex")) # 获取到文件路径下的"SheetIndex"section下的"index"的value
    sheet_name=handle_excel.get_sheet_names()[index] # 获取到正在执行sheetname
    return handle_ini.set_value(sheet_name,"authorization",get_token(data),file_path) #将获取到的token值，写入到file_path文件中的section为"sheetname"下的"authorization"

def updata_header(header=None):
    """
    更新header，将传入的header加上登录模块生成的token
    """
    index = int(handle_ini.get_value("index", "SheetIndex")) # 获取到文件路径下的"SheetIndex"section下的"index"的value
    sheet_name = handle_excel.get_sheet_names()[index] # 获取到正在执行sheetname
    try:
        value = handle_ini.get_value("authorization", sheet_name, file_path) # 获取到该”sheetname“section下的"authorization"对应的值
        if header==None:
            header={"authorization":value} # 增加判断，如果excel表读取的header为None,即未填写，则创建header并将读取到"authorization"、value值增加到header中
        else:
            header["authorization"]=value # 增加判断，如果excel表读取的header为存在数据,则将读取到"authorization"、value值增加到header中
    except:
        header=None
    return header
