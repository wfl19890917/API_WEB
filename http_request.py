import requests
COOKIE=None;
def http_request(method,url,data):
    if  method=='get':
        result=requests.get(url,data,cookies=COOKIE)
    else:
        result=requests.post(url,data,cookies=COOKIE)
    return result   #返回响应体
   # return result.jsresultxlsx#返回响应结果：结果是字典类型：{'status': 1, 'code': '10001', 'data': None, 'msg': '登录成功'}