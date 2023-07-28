# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler
import json

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]
def getdata(name):
    gitpage = requests.get("https://github.com/" + name)
    data = gitpage.text
    datadatereg = re.compile(r'data-date="(.*?)" data-level')
    # 修复页面改版后，正则匹配失效问题 1 
    # github页面改版前
    # datacountreg = re.compile(r'data-count="(.*?)" data-date')   
    # datacountreg = re.compile(r'rx="2" ry="2">(.*?) contribution')
    datacountreg = re.compile(r'<span class="sr-only">(\w*) contribution')
    datadate = datadatereg.findall(data)
    # print(len(datadate))
    datacount = datacountreg.findall(data)
    # print(len(datacount))
    # 修复页面改版后，正则匹配失效问题 2
    # github页面改版前
    # datacount = list(map(int, datacount))
    datacount = list(map(int, [0 if i == "No" else i for i in datacount]))
    contributions = sum(datacount)
    datalist = []
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    return returndata
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
