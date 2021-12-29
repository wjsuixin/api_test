#encoding=UTF-8
import json,os,logging
from base.base_request import base_request
from util.handle_excel import handle_excel
from util.handle_ini import handle_ini
from util.condition_data import generated_data,generated_datas
from util.handle_header import write_token,updata_header
from util.handle_result_json import handle_result_json

class RunMain:
    """
    执行case的类
    """
    def run_case(self):
        """
        执行case的方法
        """
        index = int(handle_ini.get_value("index","SheetIndex"))
        rows=handle_excel.getRows(index)

        col_result = int(handle_ini.get_value("result"))
        col_res = int(handle_ini.get_value("response"))
        for i in range(rows-1): # 由于读取到sheet的数据行为rows,存在1行标题行，故有效数据循环遍历的次数为row-1
            handle_excel.writeData(i+2,col_result,"",index)# 初始化，将上次执行结果删除
            handle_excel.writeData(i+2,col_res,"",index)
            data=handle_excel.getRowValue(i+2,index) # 第一条有效数据实际行数为2，i取值是从0开始的，故使用i+2
            depend=data[int(handle_ini.get_value("depend"))-1]
            method=data[int(handle_ini.get_value("method"))-1]
            url=data[int(handle_ini.get_value("url"))-1]
            re_data=data[int(handle_ini.get_value("data"))-1]
            header=data[int(handle_ini.get_value("header"))-1]
            is_run=data[int(handle_ini.get_value("is_run"))-1]
            token_operate=data[int(handle_ini.get_value("token_operate"))-1]
            expected_method=data[int(handle_ini.get_value("expected_method"))-1]
            expected_result=str(data[int(handle_ini.get_value("expected_result"))-1])
            if is_run=="yes" or is_run=="Yes":
                if depend=="否":
                    depend=None
                if header=="\\":
                    header=None
                if depend!=None:
                    if re_data=="\\":
                        re_data=None
                    if depend.find(",")==-1:
                        re_data=generated_data(depend,re_data)
                    else:
                        re_data=generated_datas(depend,re_data)
                if token_operate == "with_token":
                    header = updata_header(header)
                    res=base_request.run_main(method,index,url,re_data,header)
                    print(res)
                    code = res["code"]
                    msg = res["msg"]
                    if expected_method == "code":
                        if code == expected_result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            handle_excel.writeData(i+2,col_result,"pass",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i+2,col_result,"fail",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                    if expected_method == "msg":
                        if msg == expected_result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            handle_excel.writeData(i+2,col_result,"pass",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i+2,col_result,"fail",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                    if expected_method == "json":
                        expected_result = json.loads(expected_result)
                        result=handle_result_json(res,expected_result)
                        if result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            handle_excel.writeData(i + 2, col_result, "pass", index)
                            handle_excel.writeData(i + 2, col_res, json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i + 2, col_result, "fail", index)
                            handle_excel.writeData(i + 2, col_res, json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                elif token_operate=="write_token":
                    header=eval(header)
                    res = base_request.run_main(method,index,url,re_data,header)
                    print(res)
                    code = res["code"]
                    msg = res["msg"]
                    if expected_method == "code":
                        if code == expected_result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            write_token(res)
                            handle_excel.writeData(i+2,col_result,"pass",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i+2,col_result,"fail",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                    if expected_method == "msg":
                        if msg == expected_result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            write_token(res)
                            handle_excel.writeData(i+2,col_result,"pass",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i+2,col_result,"fail",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                    if expected_method == "json":
                        expected_result = json.loads(expected_result)
                        result=handle_result_json(res,expected_result)
                        if result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            handle_excel.writeData(i + 2, col_result, "pass", index)
                            handle_excel.writeData(i + 2, col_res, json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i + 2, col_result, "fail", index)
                            handle_excel.writeData(i + 2, col_res, json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                else:
                    header = eval(header)
                    res = base_request.run_main(method,index,url,re_data,header)
                    print(res)
                    code = res["code"]
                    msg = res["msg"]
                    if expected_method=="code":
                        if code==expected_result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            handle_excel.writeData(i+2,col_result,"pass",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i+2,col_result,"fail",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                    if expected_method=="msg":
                        if msg==expected_result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            handle_excel.writeData(i+2,col_result,"pass",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i+2,col_result,"fail",index)
                            handle_excel.writeData(i+2,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                    if expected_method == "json":
                        expected_result = json.loads(expected_result)
                        result=handle_result_json(res,expected_result)
                        if result:
                            print("预期校验方式的结果与实际结果一致,该用例测试通过")
                            handle_excel.writeData(i + 2, col_result, "pass", index)
                            handle_excel.writeData(i + 2, col_res, json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        else:
                            print("预期校验方式的结果与实际结果不一致,该用例执行失败")
                            handle_excel.writeData(i + 2, col_result, "fail", index)
                            handle_excel.writeData(i + 2, col_res, json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)

if __name__ == '__main__':
    run_case=RunMain()
    run_case.run_case()