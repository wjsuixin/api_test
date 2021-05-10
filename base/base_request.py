import requests
import json
import os
from util.handle_excel import handle_excel
from util.handle_ini import handle_ini
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
base_path=os.path.dirname(os.path.dirname(__file__))
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
            print("这个是text")
        return res

base_request=BaseRequest()

if __name__ == '__main__':
    base_request=BaseRequest()
    print(base_request.get_base_url(2))