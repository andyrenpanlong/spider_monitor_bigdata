# -*- coding: utf-8 -*-
from pymongo import MongoClient
from .settings import MONGODB_SETTINGS
import json
import pandas as pd
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

mongo_client = MongoClient(MONGODB_SETTINGS["host"], MONGODB_SETTINGS["port"])


# 为数据自动添加索引
def add_index(result):
    lists = []
    if len(result) > 0:
        keys = result[0].keys()
        for i in range(0, len(result), 1):
            dataobj = {}
            for j in keys:
                if j != "_id":
                    dataobj[j] = result[i][j]
                    dataobj["index"] = (i + 1)
            lists.append(dataobj)
    return lists


# 获取店铺信息
def get_shop_message(search):
    db = mongo_client.seventeen_zwd
    db_name = "shop_message"
    search_key = {}
    if search:
        if search.isdigit():
            search_key['game_id'] = {
                '$regex': '.*' + search + '.*'
            }
        else:
            search_key['game_name'] = {
                '$regex': '.*' + search + '.*'
            }
    result = list(db[db_name].find(search_key).limit(10))
    return add_index(result)


# 获取数据库信息
def get_db_message(dbname, tablename, search, page, page_size=10):
    db = mongo_client[dbname]
    db_name = tablename
    search_key = {}
    next_page = 0
    if int(page) > 1:
        next_page = int(int(page) - 1) * int(page_size)
    if not search:
        result = list(db[db_name].find(search_key, {"_id": 0}).skip(next_page).limit(int(page_size)))
    else:
        keys = {"_id": 0}
        for i in search.split(","):
            keys[str(i)] = ""
        result = list(db[db_name].find(search_key, keys).skip(next_page).limit(int(page_size)))
    return result


# 获取数据库表总数目
def get_db_num(dbname, tablename):
    db = mongo_client[dbname]
    db_name = tablename
    result = db[db_name].find().count()
    return result


# 代发信息列表
def get_daifa_list(search):
    db = mongo_client.seventeen_zwd
    db_name = "daifa_list"
    search_key = {}
    if search:
        if search.isdigit():
            search_key['game_id'] = {
                '$regex': '.*' + search + '.*'
            }
        else:
            search_key['game_name'] = {
                '$regex': '.*' + search + '.*'
            }
    result = list(db[db_name].find(search_key).limit(5))
    return add_index(result)


# 出租信息列表
def get_chuzu_list(search):
    db = mongo_client.seventeen_zwd
    db_name = "chuzu_message"
    search_key = {}
    if search:
        if search.isdigit():
            search_key['game_id'] = {
                '$regex': '.*' + search + '.*'
            }
        else:
            search_key['game_name'] = {
                '$regex': '.*' + search + '.*'
            }
    result = list(db[db_name].find(search_key).limit(5))
    return add_index(result)


# 获取词云
def get_word_clouds():
    db = mongo_client.seventeen_zwd
    db_name = "station_message"
    result = []
    data = list(db[db_name].find({}))
    for i in data:
        arr = i["product_type"].split(" ")
        for k in arr:
            result.append(k)
    return list(set(result))


# 获取统计信息
def get_tongji():
    db = mongo_client.seventeen_zwd
    db_name = "chuzu_message_2"
    result = {}
    Size = []
    data = list(db[db_name].find({}))
    for i in data:
        Size.append(i["size"])
    d = {
        'Size': pd.Series(Size)
    }
    df = pd.DataFrame(d)
    df = df.groupby("Size").size()

    tongji_result = json.loads(df.to_json())
    results = []
    for i in tongji_result:
        obj = {}
        key = i
        value = tongji_result[i]
        obj["key"] = key
        obj["value"] = int(value)
        obj["precent"] = obj["value"] * 100 / int(len(Size))
        results.append(obj)
    result["tongji_result"] = results
    result["count"] = len(Size)
    return result


# 根据日期统计
def date_tongji():
    db = mongo_client.seventeen_zwd
    db_name = "chuzu_message_2"
    result = {}
    Time = []
    data = list(db[db_name].find({}))
    for i in data:
        Time.append(i["time"])
    d = {
        'Time': pd.Series(Time)
    }
    df = pd.DataFrame(d)
    df = df.groupby("Time").size()
    results = {}
    col = df.iloc[:]
    num = []
    time = []
    arrs = col.values
    for j in arrs:
        num.append(int(j))
    for k in col.keys():
        time.append(k)
    results["time"] = time
    results["num"] = num
    result["date_result"] = results
    return result


# 根据时间统计
def time_tongji():
    db = mongo_client.seventeen_zwd
    db_name = "chuzu_message_2"
    result = {}
    Size = []
    data = list(db[db_name].find({}))
    for i in data:
        Size.append(i["size"])
    d = {
        'Size': pd.Series(Size)
    }
    df = pd.DataFrame(d)
    df = df.groupby("Size").size()
    tongji_result = json.loads(df.to_json())
    results = []
    for i in tongji_result:
        obj = {}
        key = i
        value = tongji_result[i]
        obj["key"] = key
        obj["value"] = int(value)
        obj["precent"] = obj["value"] * 100 / int(len(Size))
        results.append(obj)
    result["tongji_result"] = results
    result["count"] = len(Size)
    return result


# 价格分布信息统计
def get_jiage_tongji():
    db = mongo_client.soubu
    db_name = "product_list"
    result = {}
    Price = []
    data = list(db[db_name].find({}))
    for i in data:
        Price.append(float(i["price"]))
    d = {
        'Price': pd.Series(Price)
    }
    df = pd.DataFrame(d)
    df = df.groupby("Price").size()
    col = df.iloc[:]
    num = []
    time = []
    arrs = col.values
    for j in arrs:
        time.append(int(j))
    for k in col.keys():
        num.append(k)
    results = {}
    results["time"] = num
    results["num"] = time
    result["date_result"] = results
    return result

# 聊天问题入库
def noanswer_question(question):
    db = mongo_client.chatbot
    db_name = "noanswer"
    data = {
        "question": question
    }
    if len(list(db[db_name].find({"question": question}))) < 1:
        db[db_name].insert(data)


# 聊天接口
def chat_with_me(question):
    db = mongo_client.chatbot
    db_name = "dsj"
    data = list(db[db_name].find({"question": {"$regex": question}}, {"_id": 0}))
    if len(data) == 0:
        noanswer_question(question)
        data = [
            {
                "question": question,
                "answer": "对不起，已经交给工程师龙爸爸在处理了，或者您也可以教教小龙呢！"
             }
        ]
    dafu = {}
    dafu["content"] = data
    return dafu

# 密码验证
def check_name_pass(username, password):
    print("8888888888", username, password)
    return True
    # client = MongoClient('127.0.0.1', 27017)
    # db = client.local
    # result = list(db.userName.find({"en_name": username}))
    # if (len(result) > 0) and result[0]["password"] == password:
    #     return True
    # else:
    #     return False
