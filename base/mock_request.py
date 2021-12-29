# -*- coding: utf-8 -*-
# author： wujiang
# datetime： 2021/11/2 16:09
from unittest import mock
import requests,json
class MockRequest():

    def mock_request(self,mock_method,method,url,request_data,header,mock_data):
        mock_method=mock.Mock(return_value=mock_data)
        res=mock_method(method,url,request_data,header)
        return res

    def request_main(self,method,url,request_data,header):
        if method=="post":
            res=requests.post(url=url,data=request_data,headers=header)
        else:
            res = requests.get(url=url,params=request_data,headers=header)
        return res.text

if __name__ == '__main__':
    mock_r=MockRequest()
    url = "https://fat-adm-api.local.hiseas.com/admin/api/auth/login"
    data = {"username": "wj@qq.com", "password": "yx1234"}
    header = {"content-type": "application/json;charset=UTF-8"}
    mock_data = {"ID": 1, "name": "wujiang"}
    t1=mock_r.request_main("post",url,json.dumps(data),header)
    print(t1)
    t=mock_r.mock_request(mock_r.request_main,"post",url,json.dumps(data),header,mock_data)
    print(t)