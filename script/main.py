#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import m3u8
import sys
from bs4 import BeautifulSoup

res=""
with open('../sctvmulticast.html') as f:
   res=f.read()
#res = requests.get("http://epg.51zmt.top:8000/sctvmulticast.html")


def isIn(items, v):
    for item in items:
        if item in v:
            return True

def filterCategory(v):
    listCCTV=["CCTV", "CETV", "CGTN"]
    listSC=[ "卫视"]
    listTV=["SCTV", "四川", "CDTV", "熊猫", "峨眉", "成都"]

    if isIn(listCCTV, v):
        return "央视"
    elif isIn(listSC, v):
        return "卫视"
    elif isIn(listTV, v):
        return "四川"
    else:
        return "其他"

def findIcon(m, id):
    for v in m:
        if v["name"] == id:
            return v["icon"]

    return ""


def loadIcon():
    #res = requests.get("http://epg.51zmt.top:8000/sctvmulticast.html")
    res=""
    m=[]
    with open('../index.html') as f:
        res=f.read()

    soup = BeautifulSoup(res, 'lxml')

    for tr in soup.find_all('tr'):
        td = tr.find_all('td')
        if len(td) < 4:
            continue

        href = ""
        for a in td[0].find_all('a', href=True): 
            if a["href"] == "#":
                continue
            href = a["href"]

        if href != "":
            m.append({"id": td[3].string, "name": td[2].string, "icon": href})

    return m

mIcons = loadIcon()
#sys.exit(0)


soup = BeautifulSoup(res, 'lxml')
m=[]
for tr in soup.find_all(name='tr'):
    td = tr.find_all(name='td')
    if td[0].string == "序号":
        continue

    m.append({"id": td[0].string, "name": td[1].string, "address": td[2].string})


listUnused=["单音轨", "画中画", "热门", "直播室", "爱", "92"]
for c in m[:]:
    if isIn(listUnused, c["name"]):
        m.remove(c)
    else:
        c["name"]=c["name"].replace('高清', '').replace(' ', '').replace('-', '')



for c in m:
    c["tag"] = filterCategory(c["name"])
    c["icon"] = findIcon(mIcons, c["name"])
        

file=open("../m3u8/chengdu.m3u8", "w")
file.write("#EXTM3U name=\"成都电信IPTV\" url-tvg=\"http://epg.51zmt.top:8000/e.xml,https://epg.112114.xyz/pp.xml\"\n")

for c in m:
#    if c["icon"] == "":
#        print(c)

    line = '#EXTINF:-1 tvg-logo=' + c["icon"] + ' tvg-id=' + c["id"] + ' tvg-name=' + c["name"] + ' group-title=' + c["tag"] + ', ' + c["name"] + '\n'
    file.write(line)
    line = 'http://192.168.20.33:4000/rtp/' + c["address"] + "\n"
    file.write(line)

file.close()




#res = requests.get("https://raw.githubusercontent.com/iptv-org/iptv/master/streams/hk.m3u")

