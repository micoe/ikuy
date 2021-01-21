# -*- coding:utf-8 -*-
import requests,datetime,json,time,os

folder = os.environ["FOLDER"]
token = os.environ["TOKEN"]
push = os.environ["PUSH"]
phone = os.environ["USERNAME"]
passWord = os.environ["PASSWORD"]


def allow():
    al = requests.get(folder, headers={'Authorization': token}).json()['data']['depots'][0]['name']
    if str(al) == '1':return True
    else:return False

def login():
    try:
        l=s.post('https://www.yukizq.com/api/yuki/login',data={"userName": phone,"passWord": passWord,"uatoken": 'yaohuoid34976'})
        print('登陆成功')
    except:
        print('登陆失败')
        exit()

def status():
    global st
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
    if '未' in st.text:
        a = s.post('https://www.yukizq.com/api/yuki/query_task_1').json()['data']['data']
        requests.post('http://pushplus.hxtrip.com/send', data=json.dumps({"token": token, "title": 'YUKI接到单了，点击查看详情',"content": {'接单时间': t(a['createDate']),'开始时间': t(a['pickDate']),'接单账号': a['tbCode'],'商品主图': '<img src="' + a['picture'] + '" alt="商品主图" width="100%"/>','关键词': a['keyWord'],'价格': str(a['goodprice']),'任务说明': a['remark']},"template": "json"}),headers={'Content-Type': 'application/json'})
        s.post('https://www.yukizq.com/api/yuki/oktaskremark', headers={'Content-Type': 'application/json'},data=json.dumps({"taskId":a['taskId']}))
    elif '评' in st.text:
        a = s.post('https://www.yukizq.com/api/yuki/query_reviews_list').json()['data']['list']
        for i in a:
            if i['states'] == 2:
                requests.post('http://pushplus.hxtrip.com/send', data=json.dumps({"token": push, "title": 'YUKI有待评价任务，请先完成评价任务',"content": {'评价账号': i['tbCode'],'店铺名': i['shopName'],'订单号': i['businessNumber'],'评价入口': '任务-评价任务'},"template": "json"}),headers={'Content-Type': 'application/json'})

def t(t):
    ti=datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(hours=8)
    return str(ti)

def main_handler(event, context):
    global break_loop,s
    s = requests.session()
    break_loop = False
    if allow():
        login()
        while status():
            receive()
            while query():
                time.sleep(3)
        send()

if __name__ == '__main__':
    main_handler("", "")
