#!/usr/bin/python
# encoding: utf-8


import requests
from urllib import urlencode
import urllib
import time

base_url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'

# 深主板变量　
refer='http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-szse-main'
column = 'szse'
plate = 'szmb'
filepath='files_sz/'

# 上海主板变量
# column = 'sse'
# plate = 'shmb'
# referer='http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice-sse'

header = {
    'Host': 'www.cninfo.com.cn',
    'Origin': 'http://www.cninfo.com.cn',
    'Referer': refer,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


# 获取文件数量
def getMaxPage():
    params = {
        'pageNum': 1,
        'pageSize': 30,
        'tabName': 'fulltext',
        'searchkey': '社会责任',
        'column': column,
        'plate': plate,
        'seDate': '2010-01-01 ~ 2020-01-01'
    }

    response = requests.post(base_url, data=urlencode(params), headers=header)
    json = response.json()
    totalRecordNum = int(json.get('totalAnnouncement'))

    return totalRecordNum


# 下载文件
def download(bulletinId, announceTime, name):
    delimiter = ''
    list = ['http://www.cninfo.com.cn/new/announcement/download?bulletinId=', bulletinId, '&announceTime=',
            announceTime]
    url = delimiter.join(list).strip()
    filePath = filepath + name

    print 'download:', name ,'totalRecordNum:',  totalRecordNum
    urllib.urlretrieve(url, filePath)
    time.sleep(0.2)

# 　脚本开始的地方　
totalRecordNum = getMaxPage()
pageSize = 30
max_page = totalRecordNum / pageSize
indexAll = 0

# 循环房间　下载数据　　
for pageNum in range(1, max_page+1):

    params = {
        'pageNum': pageNum,
        'pageSize': pageSize,
        'tabName': 'fulltext',
        'searchkey': '社会责任',
        'column': column,
        'plate': plate,
        'seDate': '2010-01-01 ~ 2020-01-01'
    }

    response = requests.post(base_url, data=urlencode(params), headers=header)
    json = response.json()
    totalRecordNum = json.get('totalAnnouncement')

    for index, item in enumerate(json.get('announcements')):
        indexAll=indexAll+1
        announcementTitle = item.get('announcementTitle').encode('utf-8')
        secName = item.get('secName').encode('utf-8')
        secCode = item.get('secCode').encode('utf-8')
        announcementId = item.get('announcementId').encode('utf-8')
        adjunctUrl = item.get('adjunctUrl').encode('utf-8')

        indexTime = adjunctUrl.find('/', 1)
        timefile = adjunctUrl[indexTime + 1:indexTime + 10]
        indexNameEnd = adjunctUrl.find('.', 1)
        nameEnd = adjunctUrl[indexNameEnd:]
        name = announcementTitle + nameEnd

        delimiter = '_'
        list = [str(indexAll), secCode, secName, timefile, name]
        fileName = delimiter.join(list).strip()

        download(announcementId, timefile, fileName)
