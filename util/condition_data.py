#encoding=utf-8
import json
import sys,os
import random
from util.handle_excel import handle_excel
from jsonpath_rw import parse
from util.handle_ini import handle_ini
from util.handle_sql import HandleSQl
from util.handle_yaml import handle_yaml
base_path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

def split_data(data):
    """
    获取依赖数据规则并分离出case_num/sql,rule_data,replace_value
    """
    case_num=data.split(">")[0]
    if data.split(">")[1].find("@")!=-1:
        rule_data=data.split(">")[1].split("@")[0]
        replace_value=data.split(">")[1].split("@")[1]
    else:
        rule_data = data.split(">")[1]
        replace_value =None
    return case_num,rule_data,replace_value

def depend_type(data):
    """
    判断数据的依赖类型
    """
    if split_data(data)[0].find("sql#")!=-1:
        return "sql"
    elif split_data(data)[0].find("case_") != -1:
        return "case"
    else:
        print("请检查数据依赖类型的正确性")


def depend_data(data,index=None):
    """
    获取到所依赖数据集合,返回case_num对应接口返回的数据
    """
    if split_data(data)[0].find("sql#")==-1:
        case_num=split_data(data)[0].strip()
        row=handle_excel.getRowsNumber(case_num,index)
        col_res=int(handle_ini.get_value("response"))
        #print("根据依赖case_num:{},获取到的依赖case返回数据：{}".format(case_num,handle_excel.getCellValue(row,col_res,index)))
        return handle_excel.getCellValue(row,col_res,index)
    else:
        depend_database=split_data(data)[0].split("#")[1].split("+")[0]
        sql_case=split_data(data)[0].split("#")[1].split("+")[1]
        sheet=handle_excel.get_sheet_names()[int(handle_ini.get_value("index","SheetIndex"))]
        sql_result=handle_yaml.get_data(sheet,"/config/depend_sql.yaml")[sql_case]
        depend_type=split_data(data)[0].split("#")[0]
        if depend_type.find("sql")!=-1 and sql_result!=None:
            return random.choice(HandleSQl(depend_database).query(sql_result))
        else:
            print("sql依赖的case,请检查依赖数据是否正确或者sql语句是否传递！")


def get_depend_data(res_data,key):
    """
    获取依赖数据字段，传入依赖数据集合，以及key:即定义匹配的字段路径
    """
    res_data=json.loads(res_data) # 将res_data反序列化，转为dict类
    json_exe=parse(key) # 将路径转换成特定的对象
    madle=json_exe.find(res_data) # res_data为目标json串，在目标json中查找要匹配的值，这里madle是查找后得到的一个对象
    return [math.value for math in madle][0] # 取到列表一个元素的value值，固定写法

def get_data(data,index=None):
    """
    传入依赖数据值，返回获取依赖数据
    """
    if split_data(data)[0].find("sql#")==-1:
        res_data=depend_data(data,index) # 返回依赖数据集合
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

def generated_datas(data,sent_data=None,index=None):
    """
    将取到的依赖数据循环合成新的数据，进行传输
    """
    depend_case=[]
    if data.find("&")==-1: # 判断是否是多数据依赖
        depend_case.append(data)
    else:
        for i in data.split("&"):
           depend_case.append(i)
    for de_data in depend_case:
        if split_data(de_data)[0].find("sql#") == -1:  # 判断是否是case依赖
            if sent_data == None:
                print("传递参数为空，依赖值无可替换的key,请检查！")
            else:
                if split_data(de_data)[2] == None:
                    print("该用例为case依赖，缺少替换值参数的依赖值的key")
                else:
                    if type(sent_data)==dict:
                        sent_data=json.dumps(sent_data)
                    if sent_data.find(split_data(de_data)[2]) != -1:
                        if type(get_data(de_data,index))==dict:
                            sent_data = sent_data.replace(split_data(de_data)[2],json.dumps(get_data(de_data,index)))
                        else:
                            sent_data = sent_data.replace(split_data(de_data)[2], get_data(de_data,index))
                    else:
                        print("用例依赖替换值与参数中的替换值不一致或参数中替换值缺失，请检查！")
        else:
            old_data = depend_data(de_data)
            depend = eval(split_data(de_data)[1])
            for key1, value in depend.items():
                for key2 in old_data.keys():
                    if depend[key1] == key2:
                        depend[key1] = old_data[key2]
            if sent_data == None:
                if split_data(de_data)[2] == None:
                    sent_data = depend
                else:
                    print("参数为空，此时无法替换依赖值！")
            else:
                if split_data(de_data)[2] == None:
                    if type(sent_data)==dict:
                        sent_data = dict(sent_data, **depend)
                    else:
                        sent_data = dict(eval(sent_data), **depend)
                else:
                    if sent_data.find(split_data(de_data)[2]) != -1:
                        sent_data = sent_data.replace(split_data(de_data)[2], json.dumps(depend))
                    else:
                        print("sql依赖值的替换值与参数中的不一致，请检查用例！")
    return sent_data

if __name__ == '__main__':
    data="case_001>data.token"
    data1="case_001>data.(id,name),case_001>data"
    data2 = "sql#yanxue_common_fat>{'supplierId':'id','supplierName':'name'}@#name1#&sql#yanxue_common_fat>{'alternativeSupplierId':'id','alternativeSupplierName':'name'}@#name2#&case_001>data.token#token#"
    data21 = "sql#yanxue_common_fat+case_004>{'supplierId':'id','supplierName':'name'}"
    data4 = "sql#yanxue_common_fat>{'supplierId':'id','supplierName':'name'}&case_001>data.token"
    #print(split_data(data))
    #print(split_key(data2))
    data3={"data":{
                "customer":{
                    "id":111,
                    "toekn":"#name1#"}},
            "token":"#token#"
            }
    depend_data(data)
    #print(type(json.loads(depend_data(data))))
    #print(jsonpath.jsonpath(json.loads(depend_data(data)),"$.data.token"))
    data6='sql#yanxue_common_fat+case_004>{"supplierId":"id","supplierName":"name"}@#name1#'
    sql = "SELECT id,name FROM `yx_common_fat`.`supplier` WHERE `audit_status` = '3' AND `enable_status` LIKE '%1%' LIMIT 0,1000"

    #print(depend_data(data6,sql))
    #print(split_key(data2))
    #print(generated_datas(data4,sql=sql,sent_data=data3))
    data7={'supplierId': 545, 'supplierName': '丁天测试银行账户', 'alternativeSupplierId': 534, 'alternativeSupplierName': '头发公司时代风格'}
    #print(dict(data3["data"]["customer"],**data7))
    data8='{"name":"#name1#","status":1,"code":"#name2#","pageNo":1,"pageSize":10,"token":"#token#"}'
    data9='case_001>data.customer.cityName@#name1#&case_001>data.token@#token#&sql#yanxue_common_fat+case_004>{"supplierId":"id","supplierName":"name"}'
    data91 = "case_001>data.customer@#token#"
    #print(depend_data(data2,sql=sql))
    #print(get_data(data9))
    #print(generated_datas(data9,sent_data=data8,sql=sql))
    #print(data8.replace(split_data(data9)[2], get_data(data9)))
    #print(depend_data(data6))
    print(generated_datas(data91,sent_data=json.dumps(data3)))
    #print(generated_datas(data9, sent_data=json.dumps(data3)))












