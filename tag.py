# ! python3
# -*- coding: utf-8 -*-
# @author : xp-speit2018
# @email  : hantjscnxp@outlook.com
# @file   : tag.py
# 
# requirements:
#  requests@2.26.0
#

'''
    To use this script, convert your *.xlsx file to .csv format and set its path below as CSV_PATH.
    WARN: do not use chinese character and space in file path and name.

'''
from os import error
import sys
import requests
import time

CSV_PATH = './to_tag.csv'

TOKEN = ''
DETAIL_URL = 'https://hub.juzibot.com/api/v1/customer/detail?token=' + TOKEN
POST_URL = 'https://hub.juzibot.com/api/v1/tag/mark?token=' + TOKEN
TAG_MAP = {
    "822未参加" : "et_36bDgAAPGL7NIGqBqIc663HsM0Cdg",
    "822一阶"   : "et_36bDgAA8Ste0Ec6teFsjW_vvhoioA",
    "822二阶"   : "et_36bDgAAKcP83hmd6hFa7RxlC5-KnA"
}

mark_list = []

lineMax = 0
with open(CSV_PATH) as scv:
    for line in scv:
        lineMax += 1

with open(CSV_PATH) as scv:
    lineNum = 0
    for line in scv:
        lineNum += 1
        # print('\rexecuting line {}/{}, {}'.format(lineNum, lineMax, line))
        print('\r{}/{}, {}'.format(lineNum,lineMax, line[:-1].ljust(70)), end='')
        sys.stdout.flush()

        if lineNum%400==0:
            time.sleep(30)

        splitNum = len(line.split(','))
        # 居然有人在昵称中使用逗号…… "Fy,atto"
        if splitNum==5:
            userName, userId, tag, tagGroup, emptyStr = line.split(',')
        elif splitNum>5:
            emptyStr, userName, elseStr = line.split('"')
            emptyStr0, userId, tag, tagGroup, emptyStr = elseStr.split(',')

        if userName=='昵称':
            continue
        if userId=='0':
            userName, userId = userId, userName

        try:
            detailRes = requests.get(DETAIL_URL, {"externalUserId":userId}).json()
        except error:
            print(error)

        if detailRes["errcode"]==0:
            unionId = detailRes["data"]["unionId"]
        else:
            print("request unionId failed, userId: {}".format(userId))
            continue
            
        mark_list.append({
            "unionId" : unionId,
            "userId": userId,
            "addTadId": [TAG_MAP[tag]]
        })

print(mark_list)

postRes = requests.post(POST_URL, {"mark_list":mark_list}).json
print(postRes)
        



