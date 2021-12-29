import json
import sys,os
import jsonpath
from util.handle_excel import handle_excel
from jsonpath_rw import parse
from util.handle_ini import handle_ini
base_path=os.path.dirname(os.path.dirname(__file__))

sys.path.append(base_path)
def split_data(data):
    """
    获取依赖数据规则并分离出case_num,rule_data
    """
    case_num=data.split(">")[0]
    rule_data=data.split(">")[1]
    return case_num,rule_data

def depend_data(data):
    """
    获取到所依赖数据集合,返回case_num对应接口返回的数据
    """
    case_num=split_data(data)[0]
    #print("依赖的数据的case_num:{}".format(case_num))
    row=handle_excel.getRowsNumber(case_num)
    col_res=int(handle_ini.get_value("response"))
    #print("根据依赖case_num:{},获取到的依赖case返回数据：{}".format(case_num,handle_excel.getCellValue(row,col_res)))
    return handle_excel.getCellValue(row,col_res)

def get_depend_data(res_data,key):
    """
    获取依赖数据字段，传入依赖数据集合，以及key:即定义匹配的字段路径
    """
    res_data=json.loads(res_data) # 将res_data反序列化，转为dict类
    json_exe=parse(key) # 将路径转换成特定的对象
    madle=json_exe.find(res_data) # res_data为目标json串，在目标json中查找要匹配的值，这里madle是查找后得到的一个对象
    return [math.value for math in madle][0] # 取到列表一个元素的value值，固定写法

def get_data(data):
    """
    传入依赖数据值，返回获取依赖数据
    """
    res_data=depend_data(data) # 返回依赖数据集合
    rule_data=split_data(data)[1] # 返回切割后的依赖key
    #print("根据获取到的case依赖返回数据：{}，以及rule_data：{}，获取到依赖值：{}".format(res_data,rule_data,get_depend_data(res_data,rule_data)))
    return get_depend_data(res_data,rule_data)

def split_key(data):
    """
    将依赖数据路径规则分割，获取到最底层的路径名
    """
    rule_data=split_data(data)[1]
    routine_list = [] # 存放rule_data路径的分割列表，如果路径存在"."，则按照"."完成分割，并全部存入
    if rule_data.find(".")!=-1:
        for i in rule_data.split("."):
            routine_list.append(i)
    else:
        routine_list.append(rule_data)
    return routine_list[-1]

def generated_data(data,sent_data=None):
    """
    将路径提取的值与分割的路径名，合成新的k=value数据
    """
    if sent_data==None:
        sent_data={split_key(data):get_data(data)}
    else:
        sent_data[split_key(data)]=get_data(data)
    return sent_data

def generated_datas(data,sent_data=None):
    """
    存在多个依赖数据时，将取到的依赖数据循环合成新的数据，进行传输
    """
    if sent_data==None:
        temp_data = {}
        for i in data.split(","):
            for key,value in generated_data(i).items():
                temp_data[key]=value
    else:
        temp_data=sent_data
        for i in data.split(","):
            for key,value in generated_data(i).items():
                temp_data[key]=value
    #print("组合依赖数据值后生成的新data:{}".format(temp_data))
    return temp_data

if __name__ == '__main__':
    data="case_001>data.token"
    data1="case_001>data.token,case_001>data"
    data2 = "case_001>data"
    #print(split_data(data))
    #print(split_key(data2))
    data3={"111":111}
    generated_datas(data1,data3)
    #depend_data(data)
    #print(type(json.loads(depend_data(data))))
    #print(jsonpath.jsonpath(json.loads(depend_data(data)),"$.data.token"))






