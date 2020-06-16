# -*- coding: utf-8 -*-
import os,sys,datetime,subprocess
from wtforms.validators import ValidationError
reload(sys)
sys.setdefaultencoding('utf-8')
def gettime():
    return "#######"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def gettimename():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
def getday():
    return datetime.datetime.now().strftime('%Y-%m-%d')
def getday1(s=0):
    t=datetime.datetime.now()+ datetime.timedelta(days=s)
    return t.strftime('%Y%m%d')
def run_cmd(scmd):
    print('Running system command: %s'%(scmd))
    proc = subprocess.Popen(scmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    s_output, s_err = proc.communicate()
    s_return = proc.returncode
    return s_return,s_output, s_err
def send_mail(filepath):
    cmd='echo " '%(gettime(),filepath)
    sreturn,s_output, s_err=run_cmd(cmd)
    return sreturn
def isInt8(field):
    if not str(field).isalnum()  or len(str(field))!=8:
        return False
    else:
        return True
