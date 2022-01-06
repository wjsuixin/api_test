#encoding=UTF-8
import json
import ddt
import unittest
import os,sys
import datetime
from base.base_request import base_request
from util.handle_excel import handle_excel
from util.handle_ini import handle_ini
from util.condition_data import generated_datas
from util.handle_header import write_token
from util.handle_header import updata_header
from BeautifulReport import BeautifulReport
from util.handle_result_json import handle_result_json
base_path=os.path.dirname(os.path.dirname(__file__))

sys.path.append(base_path)

index = int(handle_ini.get_value("index", "SheetIndex"))
request_data = []
for n in handle_excel.getExcelData(index):
    n[-1]=None
    n[-2]=None
    request_data.append(n)

@ddt.ddt
class TestRunCaseDdt(unittest.TestCase):
    """
    执行case的类
    """
    @ddt.data(*request_data)
    def test_main_case(self,request_data):
        """
        执行case的方法
        """
        case_num = request_data[int(handle_ini.get_value("case_num"))-1]
        depend = request_data[int(handle_ini.get_value("depend"))-1]
        method = request_data[int(handle_ini.get_value("method"))-1]
        url = request_data[int(handle_ini.get_value("url"))-1]
        re_data = request_data[int(handle_ini.get_value("data"))-1]
        header = request_data[int(handle_ini.get_value("header"))-1]
        is_run = request_data[int(handle_ini.get_value("is_run"))-1]
        token_operate = request_data[int(handle_ini.get_value("token_operate"))-1]
        expected_method = request_data[int(handle_ini.get_value("expected_method"))-1]
        expected_result = str(request_data[int(handle_ini.get_value("expected_result"))-1])
        col_result = int(handle_ini.get_value("result"))
        col_res = int(handle_ini.get_value("response"))
        i = handle_excel.getRowsNumber(case_num,index)
        print(f"本次执行的测试用例为：{request_data}")
        if is_run == "yes" or is_run == "Yes":
            try:
                if depend=="否":
                    depend=None
                if header=="\\":
                    header=None
                if depend!=None:
                    if re_data=="\\":
                        re_data=None
                    else:
                        if type(generated_datas(depend, sent_data=re_data,index=index)) == str:
                            re_data = bytes(generated_datas(depend, sent_data=re_data,index=index).encode('utf-8'))
                        else:
                            re_data = json.dumps(generated_datas(depend, sent_data=re_data,index=index))
                if token_operate == "with_token":
                    if header == None:
                        header = updata_header()
                    else:
                        header = updata_header(eval(header))
                    res = base_request.run_main( method, index, url, re_data, header)
                    code = res["code"]
                    msg = res["msg"]
                    if expected_method == "code":
                        try:
                            self.assertEqual(code,expected_result)
                            handle_excel.writeData(i,col_result,"pass",index)
                            handle_excel.writeData(i,col_res,json.dumps(res),index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res),index)
                            raise e
                    if expected_method == "msg":
                        try:
                            self.assertEqual(msg,expected_result)
                            handle_excel.writeData(i,col_result,"pass",index)
                            handle_excel.writeData(i,col_res,json.dumps(res),index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res),index)
                            raise e
                    if expected_method=="json":
                        expected_result = json.loads(expected_result)
                        result = handle_result_json(res, expected_result)
                        try:
                            self.assertTrue(result)
                            handle_excel.writeData(i, col_result, "pass", index)
                            handle_excel.writeData(i, col_res, json.dumps(res), index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res),index)
                            raise e
                elif token_operate == "write_token":
                    header = eval(header)
                    res = base_request.run_main(method,index,url,re_data,header)
                    code = res["code"]
                    msg = res["msg"]
                    if expected_method == "code":
                        try:
                            self.assertEqual(code, expected_result)
                            write_token(res)
                            handle_excel.writeData(i,col_result,"pass",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                            raise e
                    if expected_method == "msg":
                        try:
                            self.assertEqual(msg,expected_result)
                            write_token(res)
                            handle_excel.writeData(i,col_result,"pass",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                            raise e
                    if expected_method=="json":
                        expected_result = json.loads(expected_result)
                        result = handle_result_json(res, expected_result)
                        try:
                            self.assertTrue(result)
                            write_token(res)
                            handle_excel.writeData(i, col_result, "pass", index)
                            handle_excel.writeData(i, col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                            raise e
                else:
                    header = eval(header)
                    res = base_request.run_main(method,index,url,re_data,header)
                    code = res["code"]
                    msg = res["msg"]
                    if expected_method == "code":
                        try:
                            self.assertEqual(code, expected_result)
                            handle_excel.writeData(i, col_result, "pass", index)
                            handle_excel.writeData(i, col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        except Exception as e:
                            handle_excel.writeData(i, col_result, "fail", index)
                            handle_excel.writeData(i, col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                            raise e
                    if expected_method == "msg":
                        try:
                            self.assertEqual(msg, expected_result)
                            handle_excel.writeData(i, col_result, "pass", index)
                            handle_excel.writeData(i, col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        except Exception as e:
                            handle_excel.writeData(i, col_result, "fail", index)
                            handle_excel.writeData(i, col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                            raise e
                    if expected_method=="json":
                        expected_result = json.loads(expected_result)
                        result = handle_result_json(res, expected_result)
                        try:
                            self.assertTrue(result)
                            handle_excel.writeData(i, col_result, "pass", index)
                            handle_excel.writeData(i, col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                            raise e
            except Exception as e:
                handle_excel.writeData(i, col_result, "fail", index)
                raise e


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')
    case_path=base_path+"/run"
    report_path=base_path+"/report"
    discover = unittest.defaultTestLoader.discover(case_path, pattern='test*.py')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
    filename = 'yohitrip interface_' + str(now)
    BeautifulReport(discover).report(description='yohitrip interface test', filename=filename, report_dir=report_path)
