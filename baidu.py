#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- rsa (必须)
Info
- author : "xchaoinfo"
- email  : "xchaoinfo@qq.com"
- date   : "2016.2.17"

'''
import requests
import math
import random
import rsa
# import binascii
# import os
import base64
import time
import re

"""
1. 百度的模拟登录，请确保你的账号能在浏览器下登录不需要验证码
 百度的三次登录错误后，才会出现验证码，但是还有一种情况是百度的账号异常

2. 这是一个初级的版本的，以后会对代码整理完善，并且统一代码风格

几个重要的参数

-- gid：js 代码构造 不需要 http 请求

-- token：需要 https://passport.baidu.com/v2/api/? 加上参数
但是不能使用 requests 的 params 参数 因为顺序不同的话，访问出问题

-- pubkey 和 rsakey
需要 http 请求获得
还有 RSA 的加密 以及 加密后的 base64 字符串化

-- callback 的 参数是动态变化的

post login 时候 还有 ppui_logintime 时间间隔参数

我是通过随机访问了一个贴吧的链接 查查是否有我的用户名 来判断是否登录成功的
if there are still questions you encounter, feel free to contact by email

"""


# gid 在同一个登录的 session 相同
def get_gid():
    gid = "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    gid = list(gid)
    for xy in range(len(gid)):
        if gid[xy] in "xy":
            r = int(random.random()*16)
            if gid[xy] == "x":
                gid[xy] = hex(r).replace("0x", '').upper()
            else:
                gid[xy] = hex(r & 3 | 8).replace("0x", '').upper()
        else:
            pass
    return ''.join(gid)


# 每次都不同
def get_callback():
    loopabc = '0123456789abcdefghijklmnopqrstuvwxyz'
    prefix = "bd__cbs__"
    n = math.floor(random.random() * 2147483648)
    a = []
    while n != 0:
        a.append(loopabc[n % 36])
        n = n // 36
    a.reverse()
    callback = prefix + ''.join(a)
    return callback


# 密码加密
def get_password(password_input, pubkey):
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode("utf-8"))
    password_input = password_input.encode("utf-8")
    psword = rsa.encrypt(password_input, pub)
    psword = base64.b64encode(psword)
    return psword.decode("utf-8")


# 构造 Request headers

agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
headers = {
    'User-Agent': agent,
    "Host": "passport.baidu.com",
    "Referer": "https://www.baidu.com/"
    
}
gid = get_gid()
session = requests.session()
# 访问登录页面的初始页面，然后这次访问会话带上 cookies
session.get("https://www.baidu.com/v2/?login", headers=headers,verify=False)


# 同一个登录下 token 是唯一的
def get_token():
    # 此处必须是自己构造 url 不能采用 params 的参数， params 参数的顺序是变化的
    token_callback = get_callback()
    global init_time
    init_time = str(int(time.time() * 1000))
    token_url = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt="
    token_url = token_url + init_time + "&class=login&loginversion=v4&logintype=dialogLogin&traceid=&gid="
    token_url = token_url + gid + "&callback="
    token_url = token_url + token_callback
    # token_params = {
    #     "getapi": "",
    #     "tpl": "pp",
    #     "apiver": "v3",
    #     "tt": str(int(time.time() * 1000)),
    #     "class": "login",
    #     "gid": gid,
    #     "logintype": "dialogLogin",
    #     "callback": get_callback()
    # }
    token_html = session.get(token_url, headers=headers,verify=False)
    token_content_all = token_html.text.replace(token_callback, "")
    token_content_all = eval(token_content_all)
    # print(token_content_all)
    return token_content_all['data']['token']

token = (get_token())


def get_publickey(token):
    publickey_callback = get_callback()
    publickey_url = "https://passport.baidu.com/v2/getpublickey?token="
    publickey_url = publickey_url + token + "&tpl=mn&apiver=v3&tt="
    publickey_url = publickey_url + str(int(time.time() * 1000)) + "&class=login&loginversion=v4&traceid=&&gid="
    publickey_url = publickey_url + gid + "&callback="
    publickey_url = publickey_url + publickey_callback
    # print(publickey_url)

    headers["Referer"] = "https://passport.baidu.com/v2/?login"
    publickey_html = session.get(publickey_url, headers=headers,verify=False)
    publickey_content_all = eval(publickey_html.text.replace(publickey_callback, ""))

    return publickey_content_all['pubkey'], publickey_content_all['key']


# print(get_publickey(token))

pubkey, key = get_publickey(token)

# 随机停顿 几秒 模拟真实的浏览情况
time.sleep(random.randint(2, 5))


def login(username, password, key):
    login_url = "https://passport.baidu.com/v2/api/?login"
    login_time = str(int(time.time() * 1000))
    login_callback = get_callback()
    # "https://passport.baidu.com/static/passpc-account/html/v3Jump.html",
    # {
    #     "staticpage": 'https://www.baidu.com/cache/user/html/v3Jump.html',
    #     "charset": "UTF-8",
    #     "token": token,
    #     "tpl": "mn",
    #     "subpro": "",
    #     "apiver": "v3",
    #     "tt": login_time,
    #     "codestring": "",
    #     "safeflg": "0",
    #     "u": "https://www.baidu.com/",
    #     "isPhone": False,
    #     "detect": "1",
    #     "gid": gid,
    #     "quick_user": "0",
    #     "logintype": "dialogLogin",
    #     "logLoginType": "pc_loginDialog",
    #     "idc": "",
    #     "loginmerge": "true",
    #     "splogin":"rate",
    #     "username": username,
    #     "password": password,
    #     "verifycode": "",
    #     "mem_pass": "on",
    #     "rsakey": key,
    #     "crypttype": "12",
    #     "ppui_logintime": str(int(login_time) - int(init_time)),
    #     "countrycode": "",
    #     "callback": login_callback,
    #     "loginversion":"v4",
    #     "dv":"tk0.271275940479766441536134169152@wwv0iy2D5y0kqUOncSKnlGN9QU8DCySkPi0kqU6ot8surhD6lSJtBEpyogpulgIpByO~lbLmg-2yoT2pgiBHgg0tshDCOHEJuSpuhDJte-2tlSPntyPiOjPXEU2D2z2D7eByJU2m-JEJT4JCtBpulEJuhS2DhSpih7PiBiKirC0koyBD2uSkMT0kqU6ot8surhD6lSJtBEpyogpulgIpByO~lbLmg-2yMgBig_ov0PoB15z0k2-2Hgb2yCQ04gu8DMU215T0kJbByqU6ot8surhD6lSJtBEpyogpulyO9rYNpse8koQ0kCz0kM~2DqU6ot8surhD6lSJtBEpyogpuluP~6bDXtYLpgzB1EU2DCg0kogByEQ04g~8kqU2DEg0ko~2DET0tshDCOHEJuSpuhDJte-2tlSPntyPiOjPXseyppN~pxLgQ1Khxvi2Hgb0kIQEvqOnUg015i2D5iBDCz2kEi8DP~B1Ez2DJyB1oyBko~8Dou2M__iveN4szP42Z0bliOiPaIXtcL4JaI~lY0b-uKXs3LX3aL9E_Bvq2mgg0kozBkqUByJu0kozBkqU8Dqg0kozBkqU2DEz2mgQB1q_"
    # }
    login_postdata ={
        "staticpage": "https://www.baidu.com/cache/user/html/v3Jump.html",
        "charset":"UTF-8",
        "token": token,
        "tpl": "mn",
        "subpro": "",
        "apiver": "v3",
        "tt": login_time,
        "codestring": "",
        "safeflg": 0,
        "u": "https://www.baidu.com/",
        "isPhone": "false",
        "detect": 1,
        "gid": gid,
        "quick_user": 0,
        "logintype": "dialogLogin",
        "logLoginType": "pc_loginDialog",
        "idc": "",
        "loginmerge": "true",
        "splogin": "rate",
        "username": username,
        "password": password,
        "mem_pass": "on",
        "rsakey": key,
        "crypttype": 12,
        "ppui_logintime": str(int(login_time) - int(init_time)),
        "countrycode": "",
        "fp_uid": "",
        "fp_info": "",
        "loginversion": "v4",
        "dv":       "tk0.0285814030560667121536138483535@rrs0MCptN~4kqQ52o7Fwnht5vR9oBDE-2lEwvlCEB-AyvaImlap-9~RkNQpmz9D9ir91oBEwvD9whRpthR      EghV8gBgOgn14k6i7tIJB-NQpmz9D9ir91oBEwvD9whRpthREghV8gBgOgn14kpg7t5JptNg4kqQ52o7Fwnht5vR9oBDE-2lEwvlCEB-AyvaImlep-NgRk    NQpmz9D9ir91oBEwvD9whRpthREghV8gBgOgn14k9ap-GJus0srBTpi4k6iBHlzptNi4oFht1AHD9wREwht9oJzpovR8g5WOKGe5gnV8rhG8blyBkDQpTN        l4k1gBk8Q52o7Fwnht5vR9oBDE-2lEwv-AKnZMEFJCTTMyTw--iTOhwsjpHla4kC~BsvAuQl4Tqa7k9~ptDlp-qwBTqyBT8zpT2wp-Czp-Ne7kpwp-9_js      0wTMrFe8rpj4avgAg8dC3oUIr9dCyvZ4azLArFl8-LX4gAgAaiWCKG1AHiTOyeXxsvpmll4k2epTpQBkDz4k2eBkqQ7tql4k2eBkqQptDepml~BTq_",
        "traceid": "F41F8301",
        "callback": login_callback
    }
    headers["Referer"] = "https://www.baidu.com/"
    headers["Origin"] = "https://www.baidu.com/"
    headers["Host"] = "passport.baidu.com"
    login_html = session.post(login_url, data=login_postdata, headers=headers)

    print(login_html.cookies)
    #re_html=r"accounts = \\'(?<acc>.*?)\\'[\s\S]*?href \+= "(?<num>.*?)"\+accounts;"
    matchObj = re.search( r'accounts = \'(.*?)\'[\s\S]*?href \+= "(.*?)"\+accounts;', login_html.text)
    url='https://www.baidu.com/cache/user/html/v3Jump.html?'+matchObj.group(2).replace('\\','')+matchObj.group(1)
    res1=session.get(url,data={}, headers={})
    print(res1)
    # res=session.get('https://ext.baidu.com/api/subscribe/v1/relation/receive?callback=_box_jsonp595&type=media&op_type=add&third_id=1570704156259187&sfrom=dusite&source=dusite_pagelist&store=uid_cuid&sid=&position=',data={}, headers=headers)
    # print((res.text))
    # html_index = session.get('https://tieba.baidu.com/p/5858634895?pid=121706425446&cid=0&red_tag=2953177019#121706425446')
    # with open("tieba.html", 'wb') as f:
    #     f.write(html_index.content)
    #     f.close()

try:
    input = raw_input
except:
    pass


if __name__ == "__main__":
    username = input("请输入你的手机号或者邮箱\n >:")
    secret = input("请输入你的密码\n >:")
    login(username, get_password(secret, pubkey), key)
