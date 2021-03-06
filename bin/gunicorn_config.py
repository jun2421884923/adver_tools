# -*- coding: utf-8 -*-
import multiprocessing

currentRootPath = "/home/video/jun.chang/adver_tools"
reload = True                                   #当代码改变时自动重启服务
bind = '192.168.64.174:8091'                        #绑定ip和端口号
backlog = 512                                   #监听队列
chdir = currentRootPath                         #gunicorn要切换到的目的工作目录
timeout = 30                                    #超时
worker_class = 'sync'                           #默认的是sync模式
#workers = multiprocessing.cpu_count() * 2 + 1   #进程数
workers = 3
threads = 2                                     #指定每个进程开启的线程数
loglevel = 'info'                               #日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'    #设置gunicorn访问日志格式，错误日志无法设置
"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""

accesslog = currentRootPath + "/logs/gunicorn_access.log"      #访问日志文件
errorlog  = currentRootPath + "/logs/gunicorn_error.log"       #错误日志文件
