#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import urllib, urllib.request
from bs4 import BeautifulSoup

class WriteInfosToSettingFile(object):

    def __init__(self, infos, anchorstring, destpath='.', filename='novelsSetting.py', ):
        self.destpath = destpath
        self.filename = filename
        self.infos = infos
        self.anchorstring = anchorstring
        if self.destpath == ".":
            self.fname = os.path.join(os.getcwd(), self.filename)
        else:
            self.fname = os.path.join(os.getcwd(), self.destpath, self.filename)


    def writeInfos(self):
        print("写入文件：%s" % self.fname)

        fileString = ''
        if os.path.exists(self.fname):
            with open(self.fname, 'r', encoding='utf-8') as f:
                allLine = f.readlines()

            for line in allLine:
                if line.startswith(self.anchorstring):
                    line = self.anchorstring + ' = %s\n' % self.infos
                fileString += line
        else:
            print('没有文件，即将新建文件：%s'%self.filename)
            fileString = self.anchorstring + ' = %s\n' % self.infos

        print('fileString is :', fileString)
        f = open(self.fname, mode='w', encoding='utf-8')
        f.write(fileString)
        f.close()

class GetChineseNovelsWebSites(object):

    def __init__(self, url='http://www.hao123.com/book', anchorstring = "ChineseNovelsWebsitesSettings"):
        '''
            此url只针对中文小说，获取的路径来自hao123.com。如想修改，可传入url，或者直接在此赋值。
            anchorstrinig是用于区分配置文件中的关键配置信息字段，详见README.md。
        '''
        self.url = url
        webSitesInfosString = self.startGetWebsites()
        self.anchorstring = anchorstring
        writefile = WriteInfosToSettingFile(webSitesInfosString, self.anchorstring)
        writefile.writeInfos()


    def startGetWebsites(self):
        res = urllib.request.urlopen(self.url)
        res = res.read().decode()
        h = BeautifulSoup(res, 'lxml')
        bd = h.find(attrs={"id": "bd"})
        cfs = bd.find_all(attrs={"class": "mod-content clearfix"})

        novelsTypeWebSites = []
        for cf in cfs:
            adict = {}
            websites = []
            title = cf.find(attrs={'class': "content-title"}).get_text().split(" ")[0]
            alla = cf.find_all("a")
            print("获取到的小说类型：%s"%title)
            adict['bigType'] = title
            for a in alla:
                websiteDict = {}
                websiteDict["name"] = a.get_text()
                websiteDict["url"] = a["href"]
                websites.append(websiteDict)
            adict['websites'] = websites
            novelsTypeWebSites.append(adict)

        return str(novelsTypeWebSites)

class GetEnglishNovelsWebSites(WriteInfosToSettingFile):
    def __init__(self,url=None, anchorstring="EnglishNovelsWebsitesSettings"):
        self.url = url
        webSitesInfosString = self.startGetWebsites()
        self.anchorstring = anchorstring
        writefile = WriteInfosToSettingFile(webSitesInfosString, self.anchorstring)
        writefile.writeInfos()


    def startGetWebsites(self):
        if self.url:
            self.sendMegToAuthor(self.url)
            print("传入了url, 该url已反馈给软件作者,请等待更新!")

        novelsTypeWebSites = [{"name": "英文小说网", "url": "http://novel.tingroom.com/"},
                              {"name": "爱思英语", "url": "https://www.24en.com/novel/"},
                              {"name": "小e英语", "url": "http://www.en8848.com.cn/soft/"}]

        return str(novelsTypeWebSites)


    def sendMegToAuthor(self):
        data = {"url":self.url}
        req = urllib.request.Request(url="www.ifconfig.site/novels/", data=data, method="post")
        if req == "200":
            print("反馈成功!")
        else:
            print("反馈失败!")
        return

class GetChineseNovelsTypes(WriteInfosToSettingFile):

    def __init__(self, url=['https://www.qidian.com/all', 'https://www.qidian.com/mm/all'], anchorstring="ChineseNovelsTypesSettings", sex="男"):
        '''
            此url只针对中文小说，获取的路径来自hao123.com。如想修改，可传入url，或者直接在此赋值。
            anchorstrinig是用于区分配置文件中的关键配置信息字段，详见README.md。
        '''
        if "男" in sex:
            self.url = url[0]

        if "女" in sex:
            self.url = url[1]

        TypesInfosString = self.startGetBoyTypes()

        self.anchorstring = anchorstring
        writefile = WriteInfosToSettingFile(TypesInfosString, self.anchorstring)
        writefile.writeInfos()

    def startGetBoyTypes(self):
        protocol_name = "https:"
        res = urllib.request.urlopen(self.url)
        res = res.read().decode()
        h = BeautifulSoup(res, 'lxml')
        bd = h.find(attrs={"type": "tag"})
        alla = bd.find_all('a')

        novelsTypes = []
        for a in alla[1:]:
            adict = {}
            title = a.get_text()
            href = a["href"]
            # print("获取到的小说类型：%s" % title)
            if protocol_name not in href:
                href = protocol_name + href
            adict[title] = href
            novelsTypes.append(adict)
        return str(novelsTypes)

class GetEnglishNovelsTypes(WriteInfosToSettingFile):

    def __init__(self, urls=None, anchorstring="EnglishNovelsTypesSettings"):
        from novelsSetting import EnglishNovelsWebsitesSettings as enws
        self.urlsDict = enws
        TypesInfosString = self.getTypes()
        self.anchorstring = anchorstring
        # writefile = WriteInfosToSettingFile(TypesInfosString, self.anchorstring)
        # writefile.writeInfos()

    def getTypes(self):
        for eweb in self.urlsDict:
            print('eweb is :', eweb)
            print('eweb["url"] is :', eweb["url"])
            soup = self.getSoup(eweb["url"], eweb["headers"])
            # if eweb["name"] == "英文小说网":
            #     types = self.getTingRoomTypes(eweb["url"])
            # if eweb["name"] == "爱思英语":
            #     types = self.get24EnTypes()
            # if eweb["name"] == "小e英语":
            #     types = self.getEn8848Types()
            # print('soup is :',soup)
            novelsTypes = []
            if eweb["name"] == "英文小说网":
                ul = soup.find(attrs={"class": "uul"})
                alla = ul.find_all("a")
            if eweb["name"] == "爱思英语":
                ul = soup.find(attrs={"class": "main_link"})
                alla = ul.find_all("a")[1:]
            if eweb["name"] == "小e英语":
                ul = soup.find(attrs={"class": "has-sub-active"})
                alla = ul.find_all("a")[1:]

            for a in alla:
                adict = {}
                title = a.get_text()
                href = a["href"]
                if not(href.startswith("https://www.") or href.startswith("http://www.")):
                    href = eweb["url"] + '/' + a['href']
                adict[title] = href
                novelsTypes.append(adict)
            print(novelsTypes)
        return novelsTypes

    def getSoup(self, url, headers):
        req = urllib.request.Request(url=url, headers=headers)
        reqText = urllib.request.urlopen(req).read().decode()
        # print(reqText)

        soup = BeautifulSoup(reqText, 'lxml')
        return soup

    # # def getTingRoomTypes(self, url):
    #     soup = self.getSoup(url)
    #
    # def get24EnTypes(self, url):
    #     soup = self.getSoup(url)
    #
    #
    # def getEn8848Types(self, url):
    #     soup = self.getSoup(url)







if __name__ == '__main__':
    # gcnw = GetChineseNovelsWebSites()
    # genw = GetEnglishNovelsWebSites()
    # gcnt = GetChineseNovelsTypes()
    gent = GetEnglishNovelsTypes()