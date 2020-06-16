# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
import logging, json,os
from werkzeug.utils import secure_filename
from project.util.common import *
# from util.models import *
from project.util.excel_todb import *
from project.util.dbutil import MysqlUtil
from project.util.result import results
# from util.excel_todb import MysqlUtil
from flask import jsonify
from validator import Required, validate, Length as mail_length
from flask_login import LoginManager, login_user, login_required, logout_user

from flask_sqlalchemy import SQLAlchemy
from project.Forms import *
app = Flask(__name__)
app.secret_key = b"qweq#.??daddadaqqe"

app.config[
    "SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://video_adver_w:Ci4EWB84BnY5@10.16.193.176:8036/video_adver?charset=utf8'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_POOL_SIZE"] = 100
app.config["SQLALCHEMY_MAX_OVERFLOW"] = 20
db = SQLAlchemy(app)
reload(sys)
sys.setdefaultencoding('utf-8')
from warnings import filterwarnings
from project.models import *

filterwarnings('error', category=MySQLdb.Warning)
from flask_bootstrap import Bootstrap  # 导入

bootstrap = Bootstrap(app)  # 绑定bootstrap与该项目app的关系

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))




# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger(__name__)
currentdir = os.path.abspath(os.path.dirname(__file__))

par_dir=os.path.abspath(os.path.join(os.getcwd(), "."))
LOG_PATH = os.path.join(par_dir, 'logs')
LOG_FILE = 'tools.log'
data_dir = os.path.join(par_dir, 'data')
print "currentdir=%s"%currentdir
print "par_dir=%s"%par_dir
'''
abort(401)
redirect(url_for('login'))
'''


def config():
    print("config start")
    print LOG_PATH
    if os.path.exists(LOG_PATH):
        pass
    else:
        os.mkdir(LOG_PATH)
    # 指定logger输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    # 文件日志
    file_handler = logging.FileHandler("%s%s%s" % (LOG_PATH, os.sep, LOG_FILE))
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


@app.route('/', methods=['POST', 'GET'])
@login_required
def _index():
    return redirect(url_for('login'))


# return render_template('upload.html')
#  return "http://192.168.64.174:8091/upload \n http://192.168.64.174:8091/sendmailout?sdate=20191223&sellerid=6000"
@app.route('/deletedspinfo', methods=['GET'])
def _deletedspinfo():
    dspid = request.args.get("dspid", 0)
    buyerid = request.args.get("buyerid", 0)

    query_list = [
        DspInfo.dspid == dspid, DspInfo.buyerid == buyerid
    ]
    sc = DspInfo.query.filter(*query_list).update({'isvalid': 0})
    print("update sc=%s" % (sc))
    db.session.commit()
    result = results()
    result.set_statuscode(0)
    result.set_data("删除成功")
    return jsonify(json.loads(str(result)))


@app.route('/deletesuginfo', methods=['GET'])
def _deletesuginfo():
    sugid = request.args.get("sugid", 1)

    query_list = [
        SugInfo.id == sugid
    ]
    print sugid
    suginfo = SugInfo.query.filter(*query_list).first()
    db.session.delete(suginfo)
    db.session.commit()
    result = results()
    result.set_statuscode(0)
    result.set_data("删除成功")
    return jsonify(json.loads(str(result)))


@app.route('/getdspinfo', methods=['GET'])
def _getdspinfo():
    dspid = request.args.get("dspid", 0)
    buyerid = request.args.get("buyerid", 0)
    query_list = [
        DspInfo.dspid == dspid, DspInfo.buyerid == buyerid
    ]
    dspinfo = DspInfo.query.filter(*query_list).first()
    print(DspInfo.dobule_to_dict(dspinfo))

    return jsonify(DspInfo.dobule_to_dict(dspinfo))
@app.route('/getsellerweight', methods=['GET'])
def _getsellerweight():
    sellerid = request.args.get("sellerid", 0)
    query_list = [
        AdxSspInfoWeight.id == sellerid
    ]
    sellerid = AdxSspInfoWeight.query.filter(*query_list).first()
    print AdxSspInfoWeight.dobule_to_dict(sellerid)
    return jsonify(AdxSspInfoWeight.dobule_to_dict(sellerid))

@app.route('/getsuginfo', methods=['GET'])
def _getsuginfo():
    sugid = request.args.get("sugid", 0)
    query_list = [
        SugInfo.id == sugid
    ]
    suginfo = SugInfo.query.filter(*query_list).first()
    print(SugInfo.dobule_to_dict(suginfo))

    return jsonify(SugInfo.dobule_to_dict(suginfo))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/xiaodu/index', methods=['POST', 'GET'])
@login_required
def _xiaoduindex():
    pages = {'内部上传页面': 'upload', "对外发邮件页面": '_mail', '历史未返数dsp情况': '_show_data', '嘉明上传页面': '_jiaming_upload',
             'dsp投放情况': '_dsptoufang', 'dsp管理': '_show_dsp_page',
             'sug管理': '_show_sug_page', '历史单价查看': '_showecpm','历史广告位绑定关系':'_impid_mapping','分成媒体分成前比例':'_share_ratio','内容输出上传页面（mis数据）':'_content_upload'
             }
    return render_template('xiaoduindex.html', pages=pages)


@app.route('/add_dsp', methods=['POST', 'GET'])
@login_required
def _add_dsp():
    """
    :return:
    """
    dspid = request.args.get("dspid")
    buyerid = request.args.get("buyerid")
    dspname = request.args.get("dspname")
    isvalid = request.args.get("isvalid")
    query_list = [
        DspInfo.dspid == dspid, DspInfo.buyerid == buyerid
    ]
    has_dsp = DspInfo.query.filter(*query_list).first()
    result = results()

    if has_dsp:
        print("exist %s, %s" % (dspid, buyerid))
        sc = DspInfo.query.filter(*query_list).update({'name': dspname, 'isvalid': isvalid})
        print("update sc=%s" % (sc))
        db.session.commit()
        result.set_statuscode(0)
        result.set_data("更新成功")
        return jsonify(json.loads(str(result)))
    else:
        print("not exist %s, %s" % (dspid, buyerid))
        dspinfo = DspInfo(dspid, buyerid, dspname, isvalid)
        try:
            db.session.add(dspinfo)
        except Warning:
            print 'Warning was raised as an exception!'
        except MySQLdb.Warning, w:
            sqlWarning = "Warning:%s" % str(w)
            print(sqlWarning)
        except MySQLdb.Error, e:
            sqlError = "Error:%s" % str(e)
            print(sqlError)
        except Exception, e:
            print(e)
            result.set_statuscode(1)
            result.set_data("添加失败，请检查数据")
            return jsonify(json.loads(str(result)))
        db.session.commit()
        result.set_statuscode(0)
        result.set_data("添加成功")
        return jsonify(json.loads(str(result)))


@app.route('/add_sug', methods=['POST', 'GET'])
@login_required
def _add_sug():
    """
    :return:
    """
    sug = request.args.get("sug")
    score = request.args.get("score")
    site = request.args.get("site")
    date = request.args.get("date")
    sugid = request.args.get("sugid")

    query_list = [
        SugInfo.id == sugid
    ]
    query_list1 = [
        SugInfo.sug == sug, SugInfo.site == site
    ]
    has_dsp = SugInfo.query.filter(*query_list).first()
    has_dsp1 = SugInfo.query.filter(*query_list1).first()

    result = results()

    if has_dsp:
        print("exist id=%s" % (sugid))
        sc = SugInfo.query.filter(*query_list).update({'sug': sug, 'score': score, 'date': date})
        print("update sc=%s" % (sc))
        db.session.commit()
        result.set_statuscode(0)
        result.set_data("更新成功")
        return jsonify(json.loads(str(result)))
    elif has_dsp1 and (not has_dsp):
        print("exist sug=%s" % (sug))
        sc = SugInfo.query.filter(*query_list1).update({'score': score, 'date': date})
        print("update sc=%s" % (sc))
        db.session.commit()
        result.set_statuscode(0)
        result.set_data("更新成功")
        return jsonify(json.loads(str(result)))
    else:
        print("not exist id=%s" % (sugid))
        dspinfo = SugInfo(sug, score, site, date)
        try:
            db.session.add(dspinfo)
        except Warning:
            print 'Warning was raised as an exception!'
        except MySQLdb.Warning, w:
            sqlWarning = "Warning:%s" % str(w)
            print(sqlWarning)
        except MySQLdb.Error, e:
            sqlError = "Error:%s" % str(e)
            print(sqlError)
        except Exception, e:
            print(e)
            result.set_statuscode(1)
            result.set_data("添加失败，请检查数据")
            return jsonify(json.loads(str(result)))
        db.session.commit()
        result.set_statuscode(0)
        result.set_data("添加成功")
        return jsonify(json.loads(str(result)))

@app.route('/add_weight', methods=['POST', 'GET'])
@login_required
def _add_weight():
    """
    :return:
    """
    sellerid = request.args.get("sellerid")
    weight = request.args.get("weight")
    query_list=[ AdxSspInfoWeight.id == sellerid]
    result=results()
    try:
        sc = AdxSspInfoWeight.query.filter(*query_list).update({ 'weight': weight})
        print("update sc=%s" % (sc))
        db.session.commit()
        result.set_statuscode(0)
        result.set_data("更新成功")
        return jsonify(json.loads(str(result)))
    except Exception ,e:
        print e
        result.set_statuscode(1)
        result.set_data("更新失败")
        return jsonify(json.loads(str(result)))


@app.route('/redict', methods=['POST', 'GET'])
@login_required
def _select():
    print(request.args.get('pathid'))
    spath = request.args.get('pathid', None)
    print(spath)
    return redirect(url_for('%s' % (spath)))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        # user_name = request.form.get('username', None)
        # password = request.form.get('password', None)
        # remember_me = request.form.get('remember_me', False)
        print(user_name)
        print(password)
        user = User(user_name)
        print(user)
        if user.verify_password(password):
            login_user(user, remember=remember_me)
            print(user_name)
            if user_name in ['test', 'xiaodu']:
                return redirect(url_for('_xiaoduindex'))
            else:
                return redirect(url_for('_jiaming_upload'))
        else:
            flash("用户名密码不正确")
            render_template('login.html', title="login", form=form)
    return render_template('login.html', title="login", form=form)


# @app.route('/test_post/nn', methods=['GET', 'POST'])  # 路由
# def test_post():
#     print "post_test"
#     testInfo={}
#     testInfo['name'] = 'xiaoliao'
#     testInfo['age'] = '28'
#     return json.dumps(testInfo)
#
#
# @app.route('/res')
# def res():
#     print "res"
#     return "testqqqqq"
#
# @app.route('/test')
# def test():
#     users = []
#     for i in range(1, 11):
#         user = User(1, "zzm" + str(i))
#         user = User(2, "zzqweqem" + str(i))
#         users.append(user)
#     user = User(1, "hello user")
#     return render_template("test.html", content="hello flask "
#             ,user=user,users=users)
# @app.route('/a')
# def query_user():
#     id = request.args
#     print(id)
#     print(1)
#     return "res=="+request.args.get("aaa")
@app.route('/test')
def _test():
    print("test")
    print request.args
    return jsonify({"code": 0})


@app.route('/show_sug_page/1', methods=['GET', 'POST'])
@app.route('/show_sug_page/<int:page>', methods=['GET', 'POST'])
@login_required
def _show_sug_page(page=1):
    print(type(request.args))
    form = SugSearchForm()
    k = ""
    if form.is_submitted() and form.keyword.data:
        k = form.keyword.data
        print("sug=%s" % k)
        return redirect(url_for('_show_sug_page', keyword=k))
    elif request.args.get("keyword", None):
        k = request.args.get("keyword", None)
        contents = SugInfo.query.filter(SugInfo.sug.like('%' + k + '%')).order_by(SugInfo.id.desc()).paginate(page=page,
                                                                                                              per_page=6,
                                                                                                              error_out=False)

    else:
        contents = SugInfo.query.order_by(SugInfo.id.desc()).paginate(page=page, per_page=6, error_out=False)

    title = "sug列表(包含调爱奇艺接口部分)"

    labels = [u'sug', u'得分', u'来源', u'日期']
    form.keyword.data = k
    return render_template('sug_info.html', pagination=contents, labels=labels, h3=title, form=form, key=request.args)


@app.route('/showecpm/1',methods=['GET','POST'])
@app.route('/showecpm/<int:page>',methods=['GET','POST'])
@login_required
def _showecpm(page=1):
    form=EcpmSearchForm()
    print form.data
    if  form.is_submitted() :
        print "POST"

        if not isInt8(form.startday.data) or not isInt8(form.startday.data):
            flash("开始或者结束日期必须为8位数字")
            form.startday.data=form.endday.data=getday1(-1)
        key=form.data
        return redirect(url_for('_showecpm',**key))
    else:
        print request.args
        startday = request.args.get("startday",getday1(-1))

        endday = request.args.get("endday",getday1(-1))
        buyerid = request.args.get("buyerid", None)
        impid = request.args.get("impid", None)
        if not isInt8(startday) or not isInt8(endday):
            flash("开始或者结束日期必须为8位数字")
            startday = endday= getday1(-1)
        form.startday.data =startday
        form.buyerid.data =buyerid
        form.endday.data =endday
        form.impid.data =impid

        # query = db.session().query(AdxRecentEcpm, AdxSspAdposition).filter(AdxRecentEcpm.day >=20200519).filter(AdxRecentEcpm.impid == AdxSspAdposition.id)
        # print query
        # print query.first()
        query_list = [
            AdxRecentEcpm.day >= startday,AdxRecentEcpm.day <= endday
        ]
        sub_sql = AdxRecentEcpm
        if startday and endday:
            sub_sql=sub_sql.query.filter(*query_list )
        else:
            sub_sql = sub_sql.query.filter(AdxRecentEcpm.day == getday1(-1))
        # SELECT dep.dname FROM dep, emp WHERE dep.id = emp.dep_id
        if buyerid:
            sub_sql=sub_sql.filter(AdxRecentEcpm.buyerid==buyerid)
        if impid:
            sub_sql = sub_sql.filter(AdxRecentEcpm.impid == impid)
        sub_sql.as_scalar()  # as_scalar的功能就是把上面的sub_sql加上了括号
        query=sub_sql.outerjoin(AdxSspAdposition, AdxSspAdposition.id==AdxRecentEcpm.impid).outerjoin(AdverSspBuyerInfo, AdverSspBuyerInfo.id==AdxRecentEcpm.buyerid).outerjoin(AdxDspInfo, AdxDspInfo.id==AdxRecentEcpm.buyerid).add_columns(AdxRecentEcpm.day, AdxRecentEcpm.buyerid, AdxRecentEcpm.third_position_id,AdxRecentEcpm.impid,AdxRecentEcpm.third_ecpm, AdxSspAdposition.name.label("impidname"), AdverSspBuyerInfo.name.label("buyername"),AdxDspInfo.name.label("dspname")).order_by(AdxRecentEcpm.day.desc())
        print query
        contents = query.paginate(page=page,per_page=6,error_out=False)


    title = "sdk和dsp历史单价"

    labels = [u'日期', u'客户id',u'客户名', u'第三方广告位', u'impid',u'广告位名字',u'ecpm']
    return render_template('showecpm.html',pagination=contents,labels=labels,h3=title,form=form,key=request.args)



@app.route('/share_ratio/1',methods=['GET','POST'])
@app.route('/share_ratio/<int:page>',methods=['GET','POST'])
@login_required
def _share_ratio(page=1):
    form=SellerSearchForm()
    print form.data
    if  form.is_submitted() :
        print "POST"
        key=form.data
        return redirect(url_for('_share_ratio',**key))
    else:
        print request.args
        sellername = request.args.get("sellername",None)
        form.sellername.data =sellername



        if sellername:
            sub_sql = AdxSspInfoWeight.query.filter(AdxSspInfoWeight.name.like('%' + sellername + '%'))
        else:
            sub_sql = AdxSspInfoWeight.query
        query=sub_sql.order_by(AdxSspInfoWeight.update_time.desc())
        print query
        contents = query.paginate(page=page,per_page=6,error_out=False)


    title = '媒体分成前收入比例'

    labels = [u'媒体id',  u'媒体名',u'比例',u'更新时间',u'操作']
    return render_template('shareratio.html',pagination=contents,labels=labels,h3=title,form=form,key=request.args)

@app.route('/impid_mapping/1',methods=['GET','POST'])
@app.route('/impid_mapping/<int:page>',methods=['GET','POST'])
@login_required
def _impid_mapping(page=1):
    form=ImpidMappingForm()
    print form.data
    if  form.is_submitted() :
        print "POST"

        if not isInt8(form.startday.data) or not isInt8(form.startday.data):
            flash("开始或者结束日期必须为8位数字")
            form.startday.data=form.endday.data=getday1(-1)
        key=form.data
        return redirect(url_for('_impid_mapping',**key))
    else:
        print request.args
        startday = request.args.get("startday",getday1(-1))

        endday = request.args.get("endday",getday1(-1))
        dspid = request.args.get("dspid", None)
        sellerid = request.args.get("sellerid", None)
        thirdid = request.args.get("thirdid", None)
        impid = request.args.get("impid", None)
        if not isInt8(startday) or not isInt8(endday):
            flash("开始或者结束日期必须为8位数字")
            startday = endday= getday1(-1)
        form.startday.data =startday
        form.dspid.data =dspid
        form.endday.data =endday
        form.impid.data =impid
        form.sellerid.data =sellerid
        form.thirdid.data =thirdid

        query_list = [
            AdxDspPositionHistory.day >= startday,AdxDspPositionHistory.day <= endday
        ]
        sub_sql = AdxDspPositionHistory
        if startday and endday:
            sub_sql=sub_sql.query.filter(*query_list )
        else:
            sub_sql = sub_sql.query.filter(AdxDspPositionHistory.day == getday1(-1))
        # SELECT dep.dname FROM dep, emp WHERE dep.id = emp.dep_id
        if dspid:
            sub_sql=sub_sql.filter(AdxDspPositionHistory.dspid == dspid)
        if impid:
            sub_sql = sub_sql.filter(AdxDspPositionHistory.impid == impid)
        if sellerid:
            sub_sql = sub_sql.filter(AdxDspPositionHistory.sellerid == sellerid)
        if thirdid:
            sub_sql = sub_sql.filter(AdxDspPositionHistory.thirdid == thirdid)
        sub_sql.as_scalar()  # as_scalar的功能就是把上面的sub_sql加上了括号
        query=sub_sql.outerjoin(AdxSspAdposition, AdxSspAdposition.id==AdxDspPositionHistory.impid).outerjoin(AdxSspInfo, AdxSspInfo.id==AdxDspPositionHistory.sellerid).outerjoin(AdxDspInfo, AdxDspInfo.id==AdxDspPositionHistory.dspid).add_columns(AdxDspPositionHistory.day, AdxDspPositionHistory.dspid, AdxDspPositionHistory.thirdid,AdxDspPositionHistory.impid,AdxDspPositionHistory.sellerid, AdxSspAdposition.name.label("impidname"), AdxSspInfo.name.label("sellername"),AdxDspInfo.name.label("dspname")).order_by(AdxDspPositionHistory.day.desc())
        print query
        contents = query.paginate(page=page,per_page=6,error_out=False)


    title = "历史广告位绑定"

    labels = [u'日期', u'dspid',u'dsp名', u'媒体id', u'媒体名',u'第三方广告位id',u'广告位id',u'广告位名']
    return render_template('impidmapping.html',pagination=contents,labels=labels,h3=title,form=form,key=request.args)
@app.route('/show_dsp_page/1', methods=['GET', 'POST'])
@app.route('/show_dsp_page/<int:page>', methods=['GET', 'POST'])
@login_required
def _show_dsp_page(page=1):
    title = "dsp列表"
    contents = DspInfo.query.order_by(DspInfo.dspid.asc()).paginate(page=page, per_page=6, error_out=False)
    print(type(contents))
    print(contents)
    labels = [u'dspid', u'buyerid', u'dsp名字', u'是否有效']

    return render_template('dsp_info.html', pagination=contents, labels=labels, h3=title)


@app.route('/mail')
@login_required
def _mail():
    print "mail"
    return render_template('sendmail.html')


# @app.route('/flashDemo')
# def flash_demo():
#     flash("hello world flash")
#     return render_template("flash.html")
# @app.route('/index/<int:id>',methods=['GET','POST'])
# def index(id):

#     print('id=',id)
#     return  render_template('index.html',surl=surl,id=id)

@app.route('/sendmailout', methods=['POST', 'GET'])
@login_required
def _sendmailout():
    """
    http://192.168.64.174:8091/sendmailout?sdate=20191223&sellerid=6000
    :return:
    """
    rules = {
        "sdate": [Required, mail_length(8, 8)],
        "sellerid": [Required]
    }
    valid, errors = validate(rules, request.args)
    result = results()
    logger.info(str(request.args) + ":" + str(valid) + str(errors))
    # 参数校验
    if not valid:
        result.set_statuscode(1)
        result.set_data(str(errors))
        return jsonify(json.loads(str(result)))
    sdate = request.args.get("sdate")
    sellerid = request.args.get("sellerid")
    cmd = """    ssh  video@bjb-s02-dcc060-adver-report00.bj  "cd /home/video/xiaodu/jun.chang/report/sellerid_imp_click && sh run_api.sh '%s' '%s' "  """ % (
    sdate, sellerid)
    logger.info(cmd)
    s_return, s_output, s_err = run_cmd(cmd)
    logger.info(str(s_return) + "###" + str(s_output) + "###" + str(s_err))
    if s_return != 0:
        result.set_statuscode(1)
        result.set_data(str(s_output) + "############" + str(s_err))
        return jsonify(json.loads(str(result)))
    else:
        result.set_data("sdate=" + sdate + "    sellerid=" + sellerid)
    return jsonify(json.loads(str(result)))


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    # flash('test  '+gettime())
    if request.method == 'POST':
        print "post"
        logger.info("upload get ")
        f = request.files['file']
        print f.filename, type(f)
        if not f.filename:
            flash("上传文件不能为空！！")
            return redirect(url_for('upload'))
        upload_path = os.path.join(data_dir, secure_filename(f.filename))
        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        f.save(upload_path)
        conn_mysql_adver = MysqlUtil("self")
        l_list = read_excel(upload_path, conn_mysql_adver)
        if len(l_list) == 0:
            print  "请检查excel数据"
            logger.info("请检查excel数据=%s " % (str(f.filename)))
            flash("请检查excel数据")
        else:
            flag = write_db(l_list, conn_mysql_adver)
            conn_mysql_adver.disconnect()
            if flag:
                flash('自建库上传成功%s行！  ' % (str(len(l_list))) + gettime())
                print str(f.filename) + "上传成功！" + gettime()
                logger.info(str(f.filename) + "上传成功！")
            else:
                flash('自建库上传失败，请检查前三列是否有重复！  ' + gettime())
                logger.error(str(f.filename) + '广告库上传失败，请检查前三列是否有重复！  ')

        return redirect(url_for('upload'))
    print "get"
    logger.info("upload get ")
    return render_template('upload.html')


@app.route('/jiaming/upload', methods=['POST', 'GET'])
@login_required
def _jiaming_upload():
    # flash('test  '+gettime())
    dspid = 1136
    if request.method == 'POST':
        print "post"
        logger.info("upload post ")
        f = request.files['file']
        print f.filename, type(f)
        if not f.filename:
            flash("上传文件不能为空！！")
            return redirect(url_for('_jiaming_upload'))
        upload_path = os.path.join( data_dir, secure_filename(f.filename))
        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        if os.path.exists(upload_path):
            print(upload_path + "  exist")
            os.rename(upload_path, upload_path + gettimename())
        f.save(upload_path)
        conn_mysql_adver = MysqlUtil("self")
        l_list = read_jiaming(upload_path, conn_mysql_adver)
        print(l_list)
        if len(l_list) == 0:
            print  "请检查excel数据"
            logger.info("请检查excel数据=%s " % (str(f.filename)))
            flash("请检查excel数据")
        else:
            [i.append(0) for i in l_list]
            print(l_list)
            flag = write_db(l_list, conn_mysql_adver)
            conn_mysql_adver.disconnect()

            if flag:
                flash('上传成功%s行！  ' % (str(len(l_list))) + gettime())
                print str(f.filename) + "上传成功！" + gettime()
                logger.info(str(f.filename) + "上传成功！")
                sreturn = send_mail(upload_path)
                if sreturn == 0:
                    logger.info("%s发邮件成功！" % (upload_path))
                else:
                    logger.info("%s发邮件失败！" % (upload_path))
            else:
                flash('上传失败，请检查数据！  ' + gettime())
                logger.error(str(f.filename) + '广告库上传失败，请检查前三列是否有重复！  ')

        return redirect(url_for('_jiaming_upload'))
    print "jaiming  get"
    logger.info("jaiming upload get ")
    return render_template('upload.html', dspid=dspid)


@app.route('/content_upload', methods=['POST', 'GET'])
@login_required
def _content_upload():
    # flash('test  '+gettime())
    if request.method == 'POST':
        print "post"
        logger.info("upload get ")
        f = request.files['file']
        print f.filename, type(f)
        if not f.filename:
            flash("上传文件不能为空！！")
            return redirect(url_for('_content_upload'))
        upload_path = os.path.join(data_dir, secure_filename(f.filename))
        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        f.save(upload_path)
        conn_mysql_adver = MysqlUtil("self_adver_report")
        l_list = read_content(upload_path, conn_mysql_adver)
        if len(l_list) == 0:
            print  "请检查excel数据"
            logger.info("请检查excel数据=%s " % (str(f.filename)))
            flash("请检查excel数据")
        else:
            flag = write_self_media_report(l_list, conn_mysql_adver)
            conn_mysql_adver.disconnect()
            if flag:
                flash('自建库上传成功%s行！  ' % (str(len(l_list))) + gettime())
                print str(f.filename) + "上传成功！" + gettime()
                logger.info(str(f.filename) + "上传成功！")
            else:
                flash('自建库上传失败，请检查数据！  ' + gettime())
                logger.error(str(f.filename) + '自建库上传失败，请检查数据！  ')

        return redirect(url_for('_content_upload'))
    print "get"
    logger.info("upload get ")
    return render_template('upload.html')

@app.route('/xiaodu/showdsp', methods=['POST', 'GET'])
@login_required
def _show_data():
    conn_mysql_adver = MysqlUtil("self")
    days_ago8 = getday1(-8)
    title = "最近8天未返数dsp情况"
    # get annual sales rank
    contentsql = """

select q.day,q.b,q.imp  from
(

select
        day,b ,sum(imp) as imp
        from (select day, b,sellerid,
impid,imp,click  from hour_adver_report  where
        day >= %s    and locate('adx',b)>0
				union all 
select a.day,cast(if( b.dspid =0,a.b ,concat('adx_',b.dspid) ) AS CHAR(100) CHARACTER SET utf8)as b,a.sellerid,
impid,imp,click
from 
(select *  from hour_adver_report  where
        day >= %s  and locate('adx',b)=0			 )a left join adver_ssp_buyer_info  b on  a.b= b.id ) hour_report
           inner join 	(select concat('adx_',dspid) as dspid from dsp_info where isvalid=1 and dspid!=1138  )w on  hour_report.b=w.dspid

           where
        day >= %s    
        group
        by  day,
        b
	union all

select
        day,hour_report.b ,sum(imp) as imp
        from (select day, b,sellerid,
impid,imp,click  from hour_adver_report  where
        day >= %s     and locate('adx',b)>0
				union all 
select a.day,cast(if( b.dspid =0,a.b ,concat('adx_',b.dspid) ) AS CHAR(100) CHARACTER SET utf8)as b,a.sellerid,
impid,imp,click
from 
(select *  from hour_adver_report  where
        day >= %s  and locate('adx',b)=0			 )a left join adver_ssp_buyer_info  b on  a.b= b.id 
				) hour_report 
	inner join (select concat('adx_',dspid) as b,impid  from adx_dsp_position where dspid=1138 and sellerid>6000 )adp on hour_report.b=adp.b and hour_report.impid=adp.impid  and  hour_report.b='adx_1138'
		where
        day >= %s 
        group
        by  day,
        hour_report.b

				)q left join

	(			select day,concat('adx_',buyerid) as b,count(*)  as sc from 
	day_adver_third_report where day>=%s    group by day,concat('adx_',buyerid)
	)w  on q.b=w.b and q.day=w.day
	where	 w.sc  is null
	""" % (days_ago8, days_ago8, days_ago8, days_ago8, days_ago8, days_ago8, days_ago8)
    _, content = conn_mysql_adver.excute(contentsql)

    labels = [u'日期', u'dspid', u'当日曝光']
    return render_template('showdata.html', labels=labels, content=content, h3=title)


@app.route('/xiaodu/dsptoufang', methods=['POST', 'GET'])
@login_required
def _dsptoufang():
    days_ago8 = request.args.get("sdate", getday1(-1))

    conn_mysql_adver = MysqlUtil("self")

    title = "dsp投放情况"
    # get annual sales rank
    contentsql = """
select q.day,q.b,q.sellerid,asi.name,q.imp,if(w.sc is null,0,1) as isreturn  from
(

select
        day,b ,sellerid,sum(imp) as imp
        from (select day, b,sellerid,
impid,imp,click  from hour_adver_report  where
        day = '%s'    and locate('adx',b)>0
				union all 
select a.day,cast(if( b.dspid =0,a.b ,concat('adx_',b.dspid) ) AS CHAR(100) CHARACTER SET utf8)as b,a.sellerid,
impid,imp,click
from 
(select *  from hour_adver_report  where
        day  = '%s'   and locate('adx',b)=0			 )a left join adver_ssp_buyer_info  b on  a.b= b.id ) hour_report
          inner join 	(select concat('adx_',dspid) as dspid from dsp_info where isvalid=1 and dspid!=1138  )w on  hour_report.b=w.dspid

           where
        day  = '%s'     
        group
        by  day,
        b,sellerid
	union all

select
        day,hour_report.b ,sellerid,sum(imp) as imp
        from (select day, b,sellerid,
impid,imp,click  from hour_adver_report  where
        day  = '%s'      and locate('adx',b)>0
				union all 
select a.day,cast(if( b.dspid =0,a.b ,concat('adx_',b.dspid) ) AS CHAR(100) CHARACTER SET utf8)as b,a.sellerid,
impid,imp,click
from 
(select *  from hour_adver_report  where
        day  = '%s'   and locate('adx',b)=0			 )a left join adver_ssp_buyer_info  b on  a.b= b.id 
				) hour_report 
	inner join (select concat('adx_',dspid) as b,impid  from adx_dsp_position where dspid=1138 and sellerid>6000 )adp on hour_report.b=adp.b and hour_report.impid=adp.impid  and  hour_report.b='adx_1138'
		where
        day  = '%s'
        group
        by  day,
        hour_report.b,sellerid

				)q left join

	(			select day,concat('adx_',buyerid) as b,count(*)  as sc from 
	day_adver_third_report where day = '%s'     group by day,concat('adx_',buyerid)
	)w  on q.b=w.b and q.day=w.day
	left join adx_ssp_info asi on q.sellerid=asi.id

	""" % (days_ago8, days_ago8, days_ago8, days_ago8, days_ago8, days_ago8, days_ago8)
    _, content = conn_mysql_adver.excute(contentsql)

    labels = [u'日期', u'dspid', u'媒体id', u'媒体名', u'曝光', u'dsp是否返数']

    return render_template('showdata.html', labels=labels, content=content, h3=title, sday=1)


import pandas as pd

df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
                   'B': [5, 6, 7, 8, 9],
                   'C': ['a', 'b', 'c--', 'd', 'e']})


@app.route('/test', methods=("POST", "GET"))
def html_table():
    print(df.to_html())
    return render_template('simple.html', tables=[df.to_html(classes='data')], titles=df.columns.values)


@app.errorhandler(404)
def not_fond(e):
    return render_template("404.html")


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))



