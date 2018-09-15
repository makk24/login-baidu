#coding:utf-8
import base64
import json
import re
from urllib.parse import quote
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import execjs

import requests
import time
from requests.cookies import RequestsCookieJar

from urllib import request
from http import cookiejar

global init_time
init_time= str(int(time.time() * 1000))
agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
headers = {
    'User-Agent': agent,
    "Host": "passport.baidu.com",
    "Referer": "https://m.baidu.com/",
    'Connection': 'keep-alive'
    
}
cookie_jar = RequestsCookieJar()
cookie_jar.set("BAIDUID", "B1CCDD4B4BC886BF99364C72C8AE1C01:FG=1", domain="baidu.com")

cookies = {'name': 'FP_UID', 'value': 'a8e078358d61a058b43420dee15e9e77', 'domain': '.baidu.com','path': '/'}
def _get_runntime():
    """
    :param path: 加密js的路径,注意js中不要使用中文！估计是pyexecjs处理中文还有一些问题
    :return: 编译后的js环境，不清楚pyexecjs这个库的用法的请在github上查看相关文档
    """
    js='''
    function callback(){
        return 'bd__cbs__'+Math.floor(2147483648 * Math.random()).toString(36)
    }
    function gid(){
        return 'xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (e) {
        var t = 16 * Math.random() | 0,
        n = 'x' == e ? t : 3 & t | 8;
        return n.toString(16)
        }).toUpperCase()
    }
    '''
    phantom = execjs.get()  # 这里必须为phantomjs设置环境变量，否则可以写phantomjs的具体路径
    # with open(js_path, 'r') as f:
    #     source = f.read()
    return phantom.compile(js)
def get_gid():
    return _get_runntime().call('gid')
def get_callback():
    return _get_runntime().call('callback')
if __name__=='__main__':
    name = input('请输入用户名:\n')
    pre_password = input('请输入密码:\n')
    
    s = requests.session()
    #使用urlencode方法转换标准格式
    #logingpostdata = parse.urlencode(Login_Data).encode('utf-8')
    #声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    cookie_support = request.HTTPCookieProcessor(cookie)
    #通过CookieHandler创建opener
    opener = request.build_opener(cookie_support)
    #创建Request对象
    req1 = opener.open('http://m.baidu.com')# request.Request(url=login_url, data=logingpostdata, headers=head)
    for item in cookie:
        cookies[item.name]=item.value
        print('Name = %s' % item.name)
        print('Value = %s' % item.value)
    #面向对象地址
    date_url = 'https://ext.baidu.com/api/subscribe/v1/relation/receive?callback=_box_jsonp120&type=media&op_type=add&third_id=1595896505607270&sfrom=dusite&source=dusite_pagelist&store=uid_cuid&sid=&position='
    #面向对象
    req2 =  request.Request(date_url, data={}, headers=headers)
    print(req2)

    # 访问登录页面的初始页面，然后这次访问会话带上 cookies
    s.get("https://www.baidu.com/v2/?login", headers=headers, cookies=cookie,verify=False)
    
    ###########获取gid#############################3
    gid =get_gid()
    ###########获取callback#############################3
    callback1 =get_callback()
    ###########获取token#############################3
    tokenUrl="https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt=%d&class=login&gid=%s&loginversion=v4&logintype=dialogLogin&traceid=&callback=%s"%(time.time()*1000,gid,callback1)

    token_response = s.get(tokenUrl, cookies=cookie, headers=headers,verify=False)
    pattern = re.compile(r'"token"\s*:\s*"(\w+)"')
    match = pattern.search(token_response.text)
    if match:
        token = match.group(1)

    else:
        raise Exception
    ###########获取callback#############################3
    callback2 =get_callback()
    ###########获取rsakey和pubkey#############################3
    rsaUrl = "https://passport.baidu.com/v2/getpublickey?token=%s&" \
             "tpl=mn&apiver=v3&tt=%d&class=login&loginversion=v4&logintype=dialogLogin&traceid=&gid=%s&callback=%s"%(token,time.time()*1000,gid,callback2)
    rsaResponse = s.get(rsaUrl)
    pattern = re.compile("\"key\"\s*:\s*'(\w+)'")
    match = pattern.search(rsaResponse.text)
    if match:
        key = match.group(1)
        print( key)

    else:
        raise Exception
    pattern = re.compile("\"pubkey\":'(.+?)'")
    match = pattern.search(rsaResponse.text)
    if match:
        pubkey = match.group(1)
        print( pubkey)

    else:
        raise Exception
    ################加密password########################3
    pre_password = bytes(pre_password, encoding = "utf8") 
    pubkey = pubkey.replace('\\n','\n').replace('\\','')
    rsakey = RSA.importKey(pubkey)
    cipher = PKCS1_v1_5.new(rsakey)
    password = base64.b64encode(cipher.encrypt(pre_password))
    print( password)
    ###########获取callback#############################3
    callback3 = get_callback()
    login_time = str(int(time.time() * 1000))
    data={
        'apiver':'v3',
        'charset':'utf-8',
        'countrycode':'',
        'crypttype':12,
        'detect':1,
        'foreignusername':'',
        'idc':'',
        'isPhone':'',
        'logLoginType':'pc_loginDialog',
        'loginmerge':True,
        'logintype':'dialogLogin',
        'mem_pass':'on',
        'quick_user':0,
        'safeflg':0,
        'staticpage':'https://www.baidu.com/cache/user/html/v3Jump.html',
        'subpro':'',
        'tpl':'mn',
        'u':'https://www.baidu.com/',
        'username':name,
        'callback':'parent.'+callback3,
        'gid':gid,
        'password':password,
        'ppui_logintime':str(int(login_time) - int(init_time)),
        'rsakey':key,
        'token':token,
        'tt':'%d'%(time.time()*1000),


    }
    ###########第一次post#############################3
    post1_response = s.post('https://passport.baidu.com/v2/api/?login', cookies=cookie,data=data)
    pattern = re.compile("codeString=(\w+)&")
    match = pattern.search(post1_response.text)
    if match:
    ###########获取codeString#############################3
        codeString = match.group(1)
        print( codeString)

    else:
        raise Exception
    data['codestring']= codeString
    #############获取验证码###################################
    verifyFail = True
    while verifyFail:
        genimage_param = ''
        if len(genimage_param)==0:
            genimage_param = codeString

        verifycodeUrl="https://passport.baidu.com/cgi-bin/genimage?%s"%genimage_param
        verifycode = s.get(verifycodeUrl)
        #############下载验证码###################################
        with open('verifycode.png','wb') as codeWriter:
            codeWriter.write(verifycode.content)
            codeWriter.close()
        #############输入验证码###################################
        verifycode = input("Enter your input verifycode: ");
        callback4 = get_callback()
        #############检验验证码###################################
        checkVerifycodeUrl='https://passport.baidu.com/v2/?' \
                        'checkvcode&token=%s' \
                        '&tpl=mn&subpro=&apiver=v3&tt=%d' \
                        '&verifycode=%s&codestring=%s' \
                        '&callback=%s'%(token,time.time()*1000,quote(verifycode),codeString,callback4)
        print( checkVerifycodeUrl)
        state = s.get(checkVerifycodeUrl)
        print( state.text)
        if state.text.find(u'验证码错误')!=-1:
            print( '验证码输入错误...已经自动更换...')
            callback5 = ctxt.locals.callback()
            changeVerifyCodeUrl = "https://passport.baidu.com/v2/?reggetcodestr" \
                                  "&token=%s" \
                                  "&tpl=mn&subpro=&apiver=v3" \
                                  "&tt=%d&fr=login&" \
                                  "vcodetype=de94eTRcVz1GvhJFsiK5G+ni2k2Z78PYRxUaRJLEmxdJO5ftPhviQ3/JiT9vezbFtwCyqdkNWSP29oeOvYE0SYPocOGL+iTafSv8pw" \
                                  "&callback=%s"%(token,time.time()*1000,callback5)
            print( changeVerifyCodeUrl)
            verifyString = s.get(changeVerifyCodeUrl)
            pattern = re.compile('"verifyStr"\s*:\s*"(\w+)"')
            match = pattern.search(verifyString.text)
            if match:
            ###########获取verifyString#############################3
                verifyString = match.group(1)
                genimage_param = verifyString
                print( verifyString)

            else:
                verifyFail = False
                raise Exception

        else:
            verifyFail = False
    data['verifycode']= verifycode
    ###########第二次post#############################3
    data['ppui_logintime']=81755
    ####################################################
    # 特地说明，大家会发现第二次的post出去的密码是改变的，为什么我这里没有变化呢？
    #是因为RSA加密，加密密钥和密码原文即使不变，每次加密后的密码都是改变的，RSA有随机因子的关系
    #所以我这里不需要在对密码原文进行第二次加密了，直接使用上次加密后的密码即可，是没有问题的。
    # ####################################################################################
    # password = base64.b64encode(cipher.encrypt(pre_password))
    # print( password
    # data['password']=password
    post2_response = s.post('https://passport.baidu.com/v2/api/?login', cookies=cookie,data=data,headers=headers)
    print(post2_response.cookies.get_dict())
    if post2_response.text.find('err_no=0')!=-1:
      res1=s.get('https://ext.baidu.com/api/subscribe/v1/relation/status', cookies=cookie,headers=headers);
      print((res1.text))
      res=s.get('https://ext.baidu.com/api/subscribe/v1/relation/receive?callback=_box_jsonp120&type=media&op_type=add&third_id=1595896505607270&sfrom=dusite&source=dusite_pagelist&store=uid_cuid&sid=&position=', cookies=cookie, headers=headers)
      print((res.text))
      print( '登录成功')
    else:
      print( '登录失败')
