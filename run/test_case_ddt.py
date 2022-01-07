#encoding=UTF-8
import json
import ddt
import unittest
import os,sys
import datetime
import HTMLTestRunnerCN
from base.base_request import base_request
from util.handle_excel import handle_excel
from util.handle_ini import handle_ini
from util.condition_data import generated_datas
from util.handle_header import write_token
from util.handle_header import updata_header
from BeautifulReport import BeautifulReport
from HTMLTestRunner import HTMLTestRunner
from util.handle_result_json import handle_result_json
from util.handle_random import handle_random
from util.email_psot import send_email
base_path=os.path.dirname(os.path.dirname(__file__))

sys.path.append(base_path)

index = int(handle_ini.get_value("index", "SheetIndex"))
request_data = []
for n in handle_excel.getExcelData(index):
    n[-2]=None
    n[-3]=None
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
        mock_data = str(request_data[int(handle_ini.get_value("mock_data"))-1])
        col_result = int(handle_ini.get_value("result"))
        col_res = int(handle_ini.get_value("response"))
        i = handle_excel.getRowsNumber(case_num,index)
        print(f"本次执行的测试用例为：{request_data}")
        if is_run == "yes" or is_run == "Yes":
            try:
                if re_data.find("faker.") != -1:
                    re_data = handle_random.data_replace(re_data)
                if depend != None and "否" and "\\":
                    if re_data == "\\":
                        re_data = None
                    re_data = generated_datas(depend, sent_data=re_data, index=index)
                if type(re_data) == str:
                    re_data = bytes(re_data.encode('utf-8'))
                else:
                    re_data = json.dumps(re_data)
                if token_operate == "with_token":
                    if header == None:
                        header = updata_header()
                    else:
                        header = updata_header(eval(header))
                    if method.find("mock_")!=-1:
                        res=base_request.mock_request(base_request.run_main,method,url,re_data,header,mock_data)
                    else:
                        res = base_request.run_main( method, index, url, re_data, header)
                    code = res["code"]
                    msg = res["msg"]
                    if expected_method == "code":
                        try:
                            self.assertEqual(code,expected_result)
                            handle_excel.writeData(i,col_result,"pass",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                            raise e
                    if expected_method == "msg":
                        try:
                            self.assertEqual(msg,expected_result)
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
                            handle_excel.writeData(i, col_result, "pass", index)
                            handle_excel.writeData(i, col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False), index)
                        except Exception as e:
                            handle_excel.writeData(i,col_result,"fail",index)
                            handle_excel.writeData(i,col_res,json.dumps(res,indent=4,sort_keys=True,ensure_ascii=False),index)
                            raise e
                elif token_operate == "write_token":
                    header = eval(header)
                    if method.find("mock_")!=-1:
                        res=base_request.mock_request(base_request.run_main,method,url,re_data,header,mock_data)
                    else:
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
                    if method.find("mock_")!=-1:
                        res=base_request.mock_request(base_request.run_main,method,url,re_data,header,mock_data)
                    else:
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
    #report_path=base_path+"/report"
    suit = unittest.TestSuite()
    discover = unittest.defaultTestLoader.discover(case_path, pattern='test*.py')
    now = datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S')
    filename = handle_ini.get_value("filename","report") + str(now)
    report_path = base_path + f"/report/{filename}.html"
    #BeautifulReport(discover).report(description='yohitrip interface test', filename=filename, report_dir=report_path)
    f=open(report_path,"wb")
    #runner=HTMLTestRunner(stream=f,title="YANXUE_erp V1.00 API Test",description="测试描述")
    runner=HTMLTestRunnerCN.HTMLTestReportCN(stream=f,
                                             title=handle_ini.get_value("title","report"),
                                             description=handle_ini.get_value("description","report"),
                                             tester=handle_ini.get_value("tester","report"))
    runner.run(discover)
    f.close()
    new_report=send_email.acquire_report_address(base_path + "/report/")
    send_email.send_email(new_report)