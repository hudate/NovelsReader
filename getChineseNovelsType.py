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

if __name__ == '__main__':
    urlList = [CNS[0]["websites"][0]["url"], CNS[0]["websites"][1]["url"]]
    typeList = getQiDian(urlList[0]+"all/")
    print(typeList)



