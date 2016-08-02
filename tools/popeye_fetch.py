#!/usr/bin/python
#-*-coding:utf8-*- 

import os, sys, re
import httplib
import string

import lxml.html
from lxml import etree

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

def get_book_entry(doc):
    html = etree.HTML(doc.lower().decode('gbk'))
    hrefs = html.xpath("//div[@class='vvmlt']/ul/li/a")
    #for i in hrefs:
    #    print i.attrib
    return map(lambda x: x.attrib['href'], hrefs)

def get_book_info(doc):
    rtv = dict()
    html = etree.HTML(doc.lower().decode('gbk'))
    title = html.xpath("//title/text()")
    pnum = html.xpath("//script[@language='javascript']/text()")
    rtv['title'] = re.sub(' ', '_', title[0].encode('utf-8').split('-')[0].strip(' '))
    for i in pnum:
        if re.search(r'var page', i):
            rtv['pnum'] = re.findall(r'var page = (.*);', i)[0]
            break
    return rtv

def main():
    #http://www.vvshu.com/view/popeye/index%d.shtml
    _host = "www.vvshu.com"
    _port = 80
    _uri = "/view/popeye/index%d.shtml"

    entries = map(lambda x: _uri % x, range(1,4))
    entries = map(lambda x: (_host, _port, x), entries)

    books = list()
    for i in entries:
        doc = http_get(*i)
        #for i in get_book_entry(doc):
        #    print i
        #sys.exit()
        books.extend(get_book_entry(doc))

    book_detail = list()
    for i in books:
        _info = dict()
        _info['url'] = i
        doc = http_get(_host, _port, "/%s" % "/".join(i.split('/')[3:]))
        info = dict(get_book_info(doc), **_info)
        print info
        book_pages = list()
        book_pages.append(i)
        for j in range(2,string.atoi(info['pnum'])+1):
            print j
        sys.exit()


if __name__ == '__main__':
    main()
