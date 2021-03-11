# -*- coding:utf-8 -*-
import requests,datetime,re,json,pytz,os
from bs4 import BeautifulSoup

folder = os.environ["FOLDER"]
token = os.environ["PUSH"]
phone = os.environ["USERNAME"]
pwd = os.environ["PASSWORD"]
url = 'http://yycangming.club/home/s_task/'
#--------------以下为代码区，请勿修改！------------#
def allow():
    al = requests.get(folder, headers={'User-Agent': 'yaohuoid34976'}).text
    if re.search(r'<title>\d+</title>', al).group()[7:10] == '000':
        print('云函数接单开关已关闭')
        return False
    else:return re.search(r'<title>\d+</title>', al).group()[7:10]

def login(a):
    tb={}
    s.headers={'User-Agent': 'Android','Content-Type': 'application/x-www-form-urlencoded'}
    s.post(url[:-7]+'dologin.do',data='role=worker&phone='+phone+'&pwd='+pwd)
    m6 = s.get(url[:-7] + 'worker/initAcount.do').text
    l = BeautifulSoup(m6, 'html.parser')
    for i in l.ul:
        if 'id' in str(i):tb[i.a.get_text()]=0
    for n,i in enumerate(list(tb)):
        if a[n] =='0':del tb[i]
    m7=s.get(url+'init_task.do?pro=3').text
    l7 = BeautifulSoup(m7, 'html.parser')
    for i in l7.find_all('li'):
        if re.search(r'\d+-\d+-\d+', str(i)).group()==datetime.datetime.now(pytz.timezone('PRC')).strftime('%Y-%m-%d'):tb[re.search(r'买号：\S+', i.find_all('p')[4].get_text()).group()[3:]] += 1
    for key in tb:
        try:
            if tb[key] == 3:print(key+'今日已做满3单，请将该位对应数字置0')
            else:tbl.append(key)
        except:pass
    if tbl:
        print(tbl,'接单中...')
        return True
    else:
        print('对应位置已接满，请全部置零或将未接满位置置1')
        return

def check(soup):
    l = BeautifulSoup(soup, 'html.parser').find_all('li')
    for i in l:
        bh=re.search(r'TAS\d+', i.find('div', class_="ui-block-a").get_text()).group()
        print('接单次数',c)
        if receive(bh):
            if inf():return
            else:return True

def receive(taskid):
    for i in tbl:
        m3 = s.post(url + 'doUserTask.do', data=('waigua=12321&xiaohao='+i+'&taskNo=' + taskid).encode('utf-8')).json()
        print(m3)
        if m3['errorCode']=='0000':return True
    return

def inf():
    m4=s.get(url+'init_task.do?pro=2').text
    l = BeautifulSoup(m4, 'html.parser')
    try:
        id = l.find('div', class_="link").div.attrs['id']
        m5=s.get(url+'excuteTask.do?id='+id).text
        bj=l.find_all('i')[0].get_text()
        yj = l.find_all('i')[1].get_text()
        li = BeautifulSoup(m5,'html.parser')
        img = li.find('div', class_="info").img.attrs['src']
        name = li.find('p', class_='bAcount').get_text()
        key = li.find('p', id='copy_key').get_text()
        print(name, key, bj, yj)
        requests.post('http://pushplus.hxtrip.com/send', data=json.dumps({"token": token, "title": '(无穷) '+bj+'/'+yj,"content": {'<a href="http://qr61.cn/ogpvAF/qtDE2Ly">Copyright © 2021 初音ミク</a>':'All rights reserved','商品主图': '<img src="' + img + '" alt="商品主图" width="100%"/>','店铺名': name,'关键词': key,'注意': '店铺名仅供平台核对任务，若使用店铺名搜索下单导致的商家返款异常后果自负'},"template": "json"}),headers={'Content-Type': 'application/json'})
        return
    except:return True

def main_handler(event, context):
    global c, s,tbl
    break_loop = False
    s = requests.session()
    n=allow()
    if n:
        c = 0
        tbl = []
        if login(n):
            if inf():
                while not break_loop:
                    m1 = s.get(url + 'renwu_list3.do').text
                    if check(m1):
                        break_loop = True
                        print(c)
                    c = c + 1

if __name__ == '__main__':
    main_handler("", "")

