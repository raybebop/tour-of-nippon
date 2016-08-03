#!/usr/bin/python
#-*-coding:utf8-*- 

import os, sys, re
import httplib
import string
import json

import lxml.html
from lxml import etree

#http://www.vvshu.com/view/popeye/index%d.shtml
_host = "www.vvshu.com"
_port = 80
_uri = "/view/popeye/index%d.shtml"

#def http_post(host, port, uri, params):
#    headers = {
#        'Content-type': 'application/x-www-form-urlencoded',
#        'Accept': 'text/plain'
#    }
#    conn = httplib.HTTPConnection(host, port)
#    conn.request("POST", uri, params, headers)
#    response = conn.getresponse()
#    return response.read()

def http_get(host, port, uri):
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    conn = httplib.HTTPConnection(host, port)
    conn.request("GET", uri, '', headers)
    response = conn.getresponse()
    return response.read()

def get_book_entry(u):
    doc = http_get(*u)
    html = etree.HTML(doc.lower().decode('gbk'))
    hrefs = html.xpath("//div[@class='vvmlt']/ul/li/a")
    return map(lambda x: x.attrib['href'], hrefs)

def get_book_info(u):
    rtv = dict()
    rtv['url'] = u
    doc = http_get(_host, _port, "/%s" % "/".join(u.split('/')[3:]))
    html = etree.HTML(doc.lower().decode('gbk'))
    title = html.xpath("//title/text()")
    pnum = html.xpath("//script[@language='javascript']/text()")
    rtv['title'] = re.sub(' ', '_', title[0].encode('utf-8').split('-')[0].strip(' '))
    try:
        rtv['pnum'] = re.findall(r'var page = (.*);', "\n".join(pnum))[0]
    except Exception,e:
        raise e
    rtv['pages'] = map(lambda x: "%s?%d" % (u, x), range(2, string.atoi(rtv['pnum'])+1))
    rtv['pages'].insert(0, u)
    return rtv

def get_book_img(u):
    img_host = "img1.vvshu.com"
    doc = http_get(_host, _port, "/%s" % "/".join(u.split('/')[3:]))
    html = etree.HTML(doc.lower().decode('gbk'))
    psrc = html.xpath("//script[@language='javascript']/text()")
    try:
        _page = re.findall(r'var page = (.*);', "\n".join(psrc))[0]
        _noo = re.findall(r'var noo = (.*);', "\n".join(psrc))[0]
        _dir = re.findall(r'var dir = (.*);', "\n".join(psrc))[0]
        _gs = re.findall(r'var gs = (.*);', "\n".join(psrc))[0]
    except Exception,e:
        raise e
    if '?' in u:
        _pn = '%03d' % string.atoi(u.split('?')[-1])
    else: 
        _pn = '%03d' % string.atoi('1')
    return "http://%s/%s%s%s" % (img_host, _dir.strip("'"), _pn, _gs.strip("'"))

def main():
    entries = map(lambda x: _uri % x, range(1,4))
    entries = map(lambda x: (_host, _port, x), entries)

    books = list()
    _books = map(lambda x: get_book_entry(x), entries)
    _books = map(lambda x: len(books) < 0 and books.append(x) or books.extend(x), _books)

    book_detail = map(lambda x: get_book_info(x), books)

    for i in book_detail:
        _temp = dict()
        _temp['imgs'] = list()
        for j in i['pages']:
            _temp['imgs'].append(get_book_img(j))
        i.update(_temp)

    #print json.dumps(book_detail)
    for j in book_detail:
        print j['url']

if __name__ == '__main__':
    main()
