# -*- coding:utf-8 -*-
import requests,json,time,re,os,datetime

folder = os.environ["FOLDER"]
token = os.environ["TOKEN"]
sckey = os.environ["SCKEY"]
phone = os.environ["USERNAME"]
passWord = os.environ["PASSWORD"]

def allow():
    al = requests.get(folder, headers={'Authorization': token}).json()['data']['depots'][0]['name']
    print(al)
    if str(al) == '1':return True
    else:return False

def login():
    global s
    s = requests.session()
    data = {"userName": phone,"passWord": passWord,"uatoken": 'byyaohuoid34976'}
    s.post('https://yukizq.com/api/yuki/login', headers={'Content-Type': 'application/json'},data=json.dumps(data))
    print('登陆成功')

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
        requests.get('https://sc.ftqq.com/' + sckey + '.send?text=YUKI接到单了点击查看&desp=' + a['createDate'] + '\n\n' + a['pickDate'] + '\n\n' + str(a['goodprice']) + '\n\n' + a['keyWord'] + '\n\n' + a['remark'] + '\n\n![logo](' + a['picture'] + ')')
        s.post('https://yukizq.com/api/yuki/oktaskremark', headers={'Content-Type': 'application/json'},data=json.dumps({"taskId":a['taskId']}))


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
