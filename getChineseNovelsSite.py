import os
import urllib, urllib.request
from bs4 import BeautifulSoup

url = 'http://www.hao123.com/book'
res = urllib.request.urlopen(url)
res = res.read().decode()
h = BeautifulSoup(res, 'lxml')
bd = h.find(attrs={"id": "bd"})
cfs = bd.find_all(attrs={"class": "mod-content clearfix"})

for cf in cfs:
    adict = {}
    title = cf.find(attrs={'class': "content-title"}).get_text().split(" ")[0]
    alla = cf.find_all("a")
    print(title)
    for a in alla:
        adict["name"] = a.get_text()
        adict["url"] = a["href"]
        print("\t%s"%adict)















