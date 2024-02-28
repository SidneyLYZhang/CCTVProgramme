import pandas as pd
import datetime
import fnmatch
import json
import os

def getDates(place):
    res = []
    for file in os.listdir(place):
        if fnmatch.fnmatch(file, '*.json'):
            res.append(os.path.splitext(os.path.basename(file))[0])
    return res

def read_data(file):
    with open(file, "r", encoding="utf8") as f:
        data = json.load(f)
    res = pd.DataFrame()
    for i in data.keys():
        tmp = pd.DataFrame([pd.Series(i) for i in data[i]["list"]])
        tmp["频道ID"] = [i]*len(tmp)
        tmp["频道名称"] = [data[i]['channelName']]*len(tmp)
        res = pd.concat([res,tmp])
    res = res[['频道ID', '频道名称', 'title', 'startTime', 'endTime',
               'columnBackvideourl', 'column_url', 'eventId', 'eventType',
               'length', 'showTime', 'top']]
    res["startTime"] = res["startTime"].apply(datetime.datetime.fromtimestamp)
    res["endTime"] = res["endTime"].apply(datetime.datetime.fromtimestamp)
    return res

def getChannelData(chdata, data):
    if chdata in data["频道ID"].unique().tolist():
        return data[data["频道ID"] == chdata]
    elif chdata in data["频道名称"].unique().tolist():
        return data[data["频道名称"] == chdata]
    elif chdata[:2] == '新闻':
        return data[data["频道ID"] == "cctv13"]
    elif chdata[:2] == '综合':
        return data[data["频道ID"] == "cctv1"]
    elif chdata[:2] == '少儿':
        return data[data["频道ID"] == "cctvchild"]
    elif chdata[:3] == '电视剧':
        return data[data["频道ID"] == "cctv8"]
    elif chdata[:2] == '电影':
        return data[data["频道ID"] == "cctv6"]
    elif chdata[:2] == '体育':
        return data[data["频道ID"].isin(["cctv5","cctv5plus"])]
    elif chdata[:2] == '财经':
        return data[data["频道ID"] == "cctv2"]
    elif chdata[:2] == '国际':
        return data[data["频道ID"] == "cctv4"]
    elif chdata[:3] == '纪录片':
        return data[data["频道ID"] == "cctvjilu"]
    elif chdata[:2] == '军事' or chdata[:4] == '国防军事':
        return data[data["频道ID"] == "cctv7"]
    elif chdata[:2] == '农业':
        return data[data["频道ID"] == "cctv17"]
    elif chdata[:2] == '科教':
        return data[data["频道ID"] == "cctv10"]
    else:
        raise ValueError("使用了错误频道。")