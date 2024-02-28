
## 必要package
import requests as rq
import json
import time
import os
import random
import pendulum as pdm
from typing import List

## 频道代码列表
CHANNELS = [
    "cctv1","cctv2","cctv3","cctv4","cctv5","cctv6","cctv7","cctv8",
    "cctv10","cctv11","cctv12","cctv13","cctv15","cctv16","cctv17",
    "cctvjilu","cctv5plus","cctvchild","cctveurope","cctvamerica"
]

## 核心爬取函数
def getURL(url:str):
    '''爬取CCTV.com的api数据'''
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://tv.cctv.com/",
        "Sec-Ch-Ua":'"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform":'"Windows"',
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailers"
    }
    text = rq.get(url=url,headers=header).text
    text = json.loads(text[9:-2])
    st = random.randint(5,9)
    print("please waiting {} seconds ...".format(st))
    time.sleep(st)
    return text['data']

def getTheDays(oridate = None, sformat = "YYYYMMDD"):
    if oridate :
        odate = pdm.from_format(oridate, sformat)
    else:
        odate = pdm.today()
    res = odate.end_of("week")
    res = [res.subtract(days=x) for x in range(0,28)]
    return [i.format(sformat) for i in res]

def gettingData(thedate:str, thechannels:List[str]):
    urls = "https://api.cntv.cn/epg/getEpgInfoByChannelNew?c={}&serviceId=tvcctv&d={}&t=jsonp&cb=setItem1"
    if os.path.exists("./{}.json".format(thedate)):
        return "Exists"
    else:
        URLL = [urls.format(x,thedate) for x in thechannels]
        res = dict()
        for i in URLL:
            tmp = getURL(i)
            res = dict(**res, **tmp)
        return res
    
if __name__ == "__main__":
    ### 爬取数据并保存
    for dx in getTheDays():
        data = gettingData(dx, CHANNELS)
        if isinstance(data, dict):
            with open("./data/{}.json".format(dx), "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)