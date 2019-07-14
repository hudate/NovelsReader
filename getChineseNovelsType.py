#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from NovelsWebsitesSettings import ChineseNovelsSettings as CNS


def getQiDian(url):
    typrList = []
    req = urllib.request.urlopen(url)
    soup = BeautifulSoup(req.read(), 'lxml')
    sl = soup.find(attrs={"class": "select-list"}).find_all("div")[0]
    alla = sl.find_all('a')[1:]
    for a in alla:
        typrList.append(a.get_text())
    return typrList


def setNovelsType(filename, typelist, anchor):
    typesListString = ''
    for index in range(0, len(typelist)):
        typesListString += '"' + typelist[index] + '", '

    typesListString = typesListString[:-2]

    with open(filename, 'r+', encoding='utf-8') as f:
        allLines = f.readlines()

    print(allLines)

    fileString = ''
    for line in allLines:
        if line.startswith(anchor):
            line = anchor + '[%s]\n'%typesListString
        fileString += line
    print(fileString)

    f = open(filename, mode='w')
    f.write(fileString)
    f.close()


if __name__ == '__main__':

    # 设置获取小说类型的参考网站列表
    urlList = [CNS[0]["websites"][0]["url"], CNS[0]["websites"][1]["url"]]

    # 获取从网站获取小说类型，，由于另一个网站使用ajax的原因，目前只使用起点的分类类型
    typesList = getQiDian(urlList[0]+"all/")

    # 小说类型的配置文件
    typesFileName = 'NovelsTypesSetting.py'

    # 中英文小说类型的识别字符串
    ChineseNovelsAnchor = 'ChineseNovelsTypes = '
    EnglishNovelsAnchor = 'EnglishNovelsTypes = '

    # 写入 获取到类型之后，把其写入到类型的配置文件中
    setNovelsType(typesFileName, typesList, ChineseNovelsAnchor)




