# -*- coding: utf-8 -*-
from flask import Flask,render_template,request,flash,redirect,url_for
import logging,os,sys,json
from werkzeug.utils import secure_filename
from util.common import *
from util.excel_todb import *
from util.dbutil import  MysqlUtil
from util.result import results
# from util.excel_todb import MysqlUtil
from flask import jsonify
from validator import Required, Not, Truthy, Blank, Range,f Equals, In, validate,Length,InstanceOf
# from wtforms.validators import
from flask_wtf import FlaskForm
reload(sys)

sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.secret_key = b"qweq#.??daddadaqqe"

        self.user_name = user_name
# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger(__name__)
currentdir = os.path.abspath(os.path.dirname(__file__))

LOG_PATH = os.path.join(currentdir,'logs')
LOG_FILE = 'tools.log'
data_dir=os.path.join(currentdir,'data')
'''
abort(401)
redirect(url_for('login'))
'''

def config():
    print("config start")
    if os.path.exists(LOG_PATH):
        pass
    else:
        os.mkdir(LOG_PATH)
    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    # 文件日志
    file_handler = logging.FileHandler("%s%s%s" % (LOG_PATH,os.sep, LOG_FILE))
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值
    # 为logger添加的日志处理器，可以自定义日志处理器让其输出到其他地方
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    app.logger.addHandler(file_handler)
    # 指定日志的最低输出级别，默认为WARN级别
    logger.setLevel(logging.DEBUG)
config()
@app.route('/',methods=['POST', 'GET'])
def hello_world():
    print "hello"
   # return render_template('upload.html')
    return "http://192.168.64.174:8091/upload \n http://192.168.64.174:8091/sendmailout?sdate=20191223&sellerid=6000"

@app.errorhandler(404)
def not_fond(e):
    return render_template("404.html")
if __name__ == '__main__':
    currentdir = os.path.abspath(os.path.dirname(__file__))
    data_dir=os.path.join(currentdir,'data')
    app.run(port=8092,debug=True)
