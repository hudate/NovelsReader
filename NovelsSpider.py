#!/usr/bin/env python
# -*- coding -*-

import urllib
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from time import *
from NovelsReader.getModules import getModules


class Browser(object):
    def __init__(self, browser, mode=0):
        self.__browserName = browser
        self.__browser = None
        self.__mode = mode
        self.setDrive()

    def setDrive(self):
        if self.__browserName.lower() == 'firefox':
            self.__browser = webdriver.Firefox()  
        elif  self.__browserName.lower() == 'chrome':
            self.__browser = webdriver.Chrome()
        else:
            self.__browser = 'r'

        # set browser inti headless mode
        if self.__mode:
            setOptions = Options()
            setOptions.add_argument('--headless')


    def get(self, url, headers = None, data = None):
        if self.__browser == 'r':
            if headers:
                req = urllib.request.Request(url, headers = headers,data = data)
            else:
                req = urllib.request.Request(url)
            res = urllib.request.urlopen(req)
            res = res.read().decode('gbk')
        else:
            self.__browser.get(url)
            res = self.__browser.page_source
        return res

    def close(self):
        if self.__browser != 'r':
            self.__browser.close()

    def title(self, soup):
        titleE = soup.find_all("title")[0]
        pageTitle = titleE.get_text()
        novelTitle = soup.find_all('h1')[0].get_text()
        return pageTitle, novelTitle

    def content(self, soup):
        content = ''
        pdiv = soup.find(id = 'onearcxsbd')
        allP = pdiv.find_next('p')
        content = allP.get_text().replace('\n　　', '')
        return content

def writeNovelToFile(filename, novelInfo):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write('\n\n' + novelInfo[0][1] + '\n')
        f.write(novelInfo[1] +'\n')

def getNovelInfo(url, browser):
    browser = Browser(browser)
    res = browser.get(url)
    browser.close()
    soup = BeautifulSoup(res, 'lxml')
    title = browser.title(soup)
    novel = browser.content(soup)
    return title, novel

def getEveryUrl(bigUrl, biginnum, filename, browser, novelname):
    num = biginnum
    errTimes = 0
    while 1:
        try:
            url = bigUrl + str(num) + '.html'
            print(url)
            novelInfo = getNovelInfo(url, browser)
            if novelname not in novelInfo[0][0]:
                break
            print(novelInfo[0][0])
            writeNovelToFile(filename, novelInfo)
            num += 1
        except:
            print('网络错误，重新请求中...')
            errTimes += 1
            if errTimes == 2:
                num += 1
                errTimes = 0
            sleep(2)

if __name__ == '__main__':
    print('欢迎使用小说阅读下载器。')
    # some necessary moudles
    modulesList = ['bs4', 'selenuim']
    
    # install modules if necessary 
    getModules(modulesList)
    
    # get novel type
    novelTyep = input('请输入您的选项：')
    novelname = '摇花放鹰传'
    bigUrl = 'http://www.xyyuedu.com/wuxiaxiaoshuo/wolongsheng/yaohuafangyingchuan/'

    # 设置浏览器，若为Firefox 或者 Chrome则使用selenium
    browser = 'r'
    biginnum = 242620
    filename = '摇花放鹰传.txt'
    getEveryUrl(bigUrl, biginnum, filename, browser, novelname)

