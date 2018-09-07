# -*- coding: UTF-8 -*-
from urllib import request
from http import cookiejar

if __name__ == '__main__':
  #登陆地址
    login_url = 'http://www.jobbole.com/wp-admin/admin-ajax.php'    
    #User-Agent信息                   
    user_agent = r'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'
    #Headers信息
    head = {'User-Agnet': user_agent, 'Connection': 'keep-alive'}
    #登陆Form_Data信息
    Login_Data = {}
    Login_Data['action'] = 'user_login'
    Login_Data['redirect_url'] = 'http://www.jobbole.com/'
    Login_Data['remember_me'] = '0'         #是否一个月内自动登陆
    Login_Data['user_login'] = '********'       #改成你自己的用户名
    Login_Data['user_pass'] = '********'        #改成你自己的密码
    #使用urlencode方法转换标准格式
    logingpostdata = parse.urlencode(Login_Data).encode('utf-8')
    #声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    cookie_support = request.HTTPCookieProcessor(cookie)
    #通过CookieHandler创建opener
    opener = request.build_opener(cookie_support)
    #创建Request对象
    req1 = request.Request(url=login_url, data=logingpostdata, headers=head)

    #面向对象地址
    date_url = 'http://date.jobbole.com/wp-admin/admin-ajax.php'
    #面向对象
    Date_Data = {}
    Date_Data['action'] = 'get_date_contact'
    Date_Data['postId'] = '4128'
    #使用urlencode方法转换标准格式
    datepostdata = parse.urlencode(Date_Data).encode('utf-8')
    req2 = request.Request(url=date_url, data=datepostdata, headers=head)




    # #设置保存cookie的文件，同级目录下的cookie.txt
    # filename = 'cookie.txt'
    # #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    # cookie = cookiejar.MozillaCookieJar(filename)
    # #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    # handler=request.HTTPCookieProcessor(cookie)
    # #通过CookieHandler创建opener
    # opener = request.build_opener(handler)
    # #此处的open方法打开网页
    # response = opener.open('http://www.baidu.com')
    # #保存cookie到文件
    # cookie.save(ignore_discard=True, ignore_expires=True)
    # #打印cookie信息
    # for item in cookie:
    #     print('Name = %s' % item.name)
    #     print('Value = %s' % item.value)