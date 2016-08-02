#!/usr/bin/python
#-*-coding:utf8-*- 

import os, sys, re
import httplib

import lxml.html
from lxml import etree
from BeautifulSoup import BeautifulSoup

def http_get(host, port, uri):
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    conn = httplib.HTTPConnection(host, port)
    conn.request("GET", uri, '', headers)
    response = conn.getresponse()
    return response.read()

def http_post(host, port, uri, params):
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    conn = httplib.HTTPConnection(host, port)
    conn.request("POST", uri, params, headers)
    response = conn.getresponse()
    return response.read()

def main():
    ###"http://www.vvshu.com/view/popeye/index%d.shtml"
    _host = "www.vvshu.com"
    _port = 80
    _uri = "/view/popeye/index%d.shtml"

    entries = map(lambda x: _uri % x, range(1,4))
    entries = map(lambda x: (_host, _port, x), entries)

    for i in entries:
        doc = http_get(*i)
        #html = lxml.html.fromstring(doc)
        page = etree.HTML(doc.lower().decode('gbk'))
        hrefs = page.xpath(u"//a")
        hrefs = page.xpath("//div[@class='vvmlt']/ul/li/a")
        #print hrefs
        for href in hrefs:
            print href.attrib
        sys.exit()

if __name__ == '__main__':
    main()
