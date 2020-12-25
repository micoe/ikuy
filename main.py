# -*- coding:utf-8 -*-
import requests,datetime,json,time,os

folder = os.environ["FOLDER"]
token = os.environ["TOKEN"]
push = os.environ["PUSH"]
sckey = os.environ["SCKEY"]
phone = os.environ["USERNAME"]
passWord = os.environ["PASSWORD"]

def allow():
    al = requests.get(folder, headers={'Authorization': token}).json()['data']['depots'][0]['name']
    if str(al) == '1':return True
    else:return False

def login():
    global s
    s = requests.session()
    data = {"userName": phone,"passWord": passWord,"uatoken": 'byyaohuoid34976'}
    l=s.post('https://yukizq.com/api/yuki/login', headers={'Content-Type': 'application/json;charset=utf-8'},data=data)
    print(l.json()['data']['tbCode']+'登陆成功')

def status():
    st = s.post('https://www.yukizq.com/api/yuki/is_task')
    stu=st.json()['data']
    print(stu['message'])
    return stu['status']

def receive():
    re = s.post('https://www.yukizq.com/api/yuki/receive_task', data='{"isyp":"true","ismsg":"false","isretry":"false"}')
    print(re.json()['data']['message'])

def query():
    qu = s.post('https://www.yukizq.com/api/yuki/query_receive_task')
    print(qu.json()['data']['message'])
    if 'istask' in qu.text:return True
    else:return False

def send():
    q = s.post('https://www.yukizq.com/api/yuki/query_task_1')
    a = q.json()['data']['data']
    if a:
        requests.post('http://pushplus.hxtrip.com/send', data=json.dumps({"token": push, "title": 'YUKI接到单了，点击查看详情',"content": {'接单时间': t(a['createDate']),'开始时间': t(a['pickDate']),'商品主图': '<img src="' + a['picture'] + '" alt="商品主图" width="100%"/>','搜索关键词': a['keyWord'],'价格': str(a['goodprice']),'任务说明': a['remark']},"template": "json"}),headers={'Content-Type': 'application/json'})
        s.post('https://yukizq.com/api/yuki/oktaskremark', headers={'Content-Type': 'application/json'},data=json.dumps({"taskId":a['taskId']}))

def t(t):
    ti=datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8)
    return str(ti)

def main_handler(event, context):
    print(datetime.datetime.now())
    if allow():
        login()
        while status():
            receive()
            while query():
                time.sleep(3)
        print(datetime.datetime.now())
        send()

if __name__ == '__main__':
    main_handler("", "")
