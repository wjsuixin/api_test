import sys
import requests
import json
import os
from unittest import mock
from util.handle_excel import handle_excel
from util.handle_ini import handle_ini
from util.handle_log import Logger
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
base_path=os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)
logger=Logger(logger="RunMain").getlog()

class BaseRequest:

    def get_base_url(self,index):
        """
        获取对应index下的base_url
        """
        sheet_name = handle_excel.get_sheet_names()[index]
        base_url=handle_ini.get_value(sheet_name,"BaseUrl")
        return base_url


    def send_post(self,index,url,data,header=None):
        """
        创建post方法
        """
        res=requests.post(url=self.get_base_url(index)+url,data=data,headers=header,verify=False,allow_redirects=False).text
        return res

    def send_get(self,index,url,data,header=None):
        """
        创建get方法
        """
        res=requests.get(url=self.get_base_url(index)+url,params=data,headers=header,verify=False,allow_redirects=False).text
        return res

    def send_updata_post(self,index,url,data,header=None):
        """
        创建文件上传方法
        """
        data=eval(data) # 将Excel表中取出的数据由类型str转化为dict
        res=requests.post(url=self.get_base_url(index)+url,files=data,headers=header,verify=False,allow_redirects=False).text
        return res

    def run_main(self,method,index,url,data,header):
        """
        创建执行函数
        """
        if method=="post":
            res=self.send_post(index,url,data,header)
        elif method=="updata_post":
            res=self.send_updata_post(index,url,data,header)
        else:
            res=self.send_get(index,url,data,header)
        try:
            res=json.loads(res)
            #print(type(res))
        except:
            logger.info("该返回数据是text")
        return res

    def mock_request(self,mock_method,method,url,request_data,header,mock_data):
        """
        mock接口测试
        """
        mock_method=mock.Mock(return_value=mock_data)
        if method=="mock_post":
            res=mock_method(self.run_main,"post",url,request_data,header)
        elif method=="mock_get":
            res = mock_method(self.run_main, "get", url, request_data, header)
        else:
            res=mock_method(self.run_main, "updata_post", url, request_data, header)
        try:
            res = json.loads(res)
            # print(type(res))
        except:
            logger.info("该返回数据是text")
        return res


base_request=BaseRequest()

if __name__ == '__main__':
    base_request=BaseRequest()
    """
    url="https://fat-adm-api.local.hiseas.com/admin/api/auth/login"
    data={"username":"wj@qq.com","password":"yx1234"}
    header = {"content-type": "application/json;charset=UTF-8"}
    res=requests.post(url=url,json=data,headers=header)
    print(res)
    header1={"authorization":res.json()["data"]["token"]}
    print(header1)
    url1="https://fat-adm-api.local.hiseas.com/admin/api/base/upload"
    file={"file":("python.pdf",open("D:\python.pdf","rb"),"application/pdf")}
    files={'file': ("python.pdf", open("D:\python.pdf", 'rb'), "application/pdf")}
    print(type(file))
    res1=requests.post(url=url1,files=file,headers=header1,verify=False)
    print(res1.text)
    """
    #base_request.get_base_url(1)
    url = "auth/login"
    data = {"username": "wj@qq.com", "password": "yx1234"}
    header = {"content-type": "application/json;charset=UTF-8"}
    mock_data = {"ID": 1, "name": "wujiang"}
    print(base_request.get_base_url(1))
    t1 = base_request.run_main("post",1, url,json.dumps(data), header)
    print(t1)
    t = base_request.mock_request(base_request.run_main, "post", url, json.dumps(data), header, mock_data)
    print(t)