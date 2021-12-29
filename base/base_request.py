import requests
import json
import os
from util.handle_excel import handle_excel
from util.handle_ini import handle_ini
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
base_path=os.path.dirname(os.path.dirname(__file__))

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
