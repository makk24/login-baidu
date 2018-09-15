#coding:utf-8
import requests
import time
from requests.cookies import RequestsCookieJar
from urllib import request
from http import cookiejar
from logger import Logger

log = Logger('./logs/all.log',level='info')
agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
headers = {
    'User-Agent': agent,
    'Connection': 'keep-alive'
}
def toRequest(cuid,doid,uss):
  cookies.set_cookie(cookiejar.Cookie(version=0, name='BAIDUCUID', value=cuid,
                     port=None, port_specified=None,
                     domain=".baidu.com", domain_specified=None, domain_initial_dot=None,
                     path="/", path_specified=None,
                     secure=None,
                     expires=None,
                     discard=None,
                     comment=None,
                     comment_url=None,
                     rest=None,
                     rfc2109=False,))
  cookies.set_cookie(cookiejar.Cookie(version=0, name='BDUSS', value=uss,
                     port=None, port_specified=None,
                     domain=".baidu.com", domain_specified=None, domain_initial_dot=None,
                     path="/", path_specified=None,
                     secure=None,
                     expires=None,
                     discard=None,
                     comment=None,
                     comment_url=None,
                     rest=None,
                     rfc2109=False,))
  res1=s.get('https://ext.baidu.com/api/subscribe/v1/relation/status', cookies=cookies,headers=headers);
  log.logger.info(res1.text)
  res=s.get('https://ext.baidu.com/api/subscribe/v1/relation/receive?callback=_box_jsonp120&type=media&op_type=add&third_id='+doid+'&sfrom=dusite&source=dusite_pagelist&store=uid&sid=&position=', cookies=cookies, headers=headers)
  log.logger.info('doid:'+doid+',uss:'+uss+'------'+res.text)

if __name__=='__main__':
    s = requests.session()
    cookies = cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cookies)
    opener = request.build_opener(cookie_support)
    req1 = opener.open('http://www.baidu.com')
    cookies.add_cookie_header
    filename = 'cuid.txt'
    filename1 = 'doid.txt'
    filename2 = 'uss.txt'
    file_doid = open(filename1).read().splitlines()
    file_cuid = open(filename).read().splitlines()
    file_uss = open(filename2).read().splitlines()
    for doid in file_doid:
      if doid.strip()!="":
        for uss in file_uss:
          for cuid in file_cuid:
            if cuid.strip()!="":
              toRequest(cuid.strip(),doid.strip(),uss)
              time.sleep(0.02)
    input()
