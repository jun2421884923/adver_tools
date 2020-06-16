# -*- coding: utf8 -*-
import sys,pandas as pd,re
import pymysql as MySQLdb
from flask import flash
from flask import current_app
from project.util.common import *
import traceback
from warnings import filterwarnings
filterwarnings('error', category = MySQLdb.Warning)
sys.path.append('/home/video/jun.chang/MyFlask')
#sys.path.append('..')
#from Myflask import logger
#import logging
#logger = logging.getLogger(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')
def check_number(x):
    flag=False
    try:
        tmp=int(x)
        return True
    except:
        print str(x)+':conv int fail'
    return flag

def check_decimal(x):
    flag=False
    try:
        tmp=float(x)
        return True
    except:
        print str(x)+':conv float fail'
    return flag
def check_day(x):
    flag=False
    try:
        if str(x).isdigit() and len(str(x))==8:
            return True
    except:
        print str(x)+':day len!=8 or is not int'
    return flag
def  getall_buyerid(conn_mysql):
    buyid_sql = """ select id from adx_dsp_info
 union all 
 select id from adver_ssp_buyer_info"""
    flag,res = conn_mysql.excute(buyid_sql)
    if flag:
        return [ i[0] for i in res]
    else:
        return []
def get_allthirdid(conn_mysql,startdate,enddate):
    thirdid_sql = """ select thirdid  from adx_dsp_position_history where day>=%s and day<= %s  group by thirdid
"""%(startdate,enddate)
    flag, res = conn_mysql.excute(thirdid_sql)
    if flag:
        return [i[0] for i in res]
    else:
        return []
def check_buyerid(buyerid,allbuyid_list):
    if check_number(buyerid):
        if buyerid in allbuyid_list:
            return True
        else:
            current_app.logger.error("%s buyerid不在库里"%(str(buyerid)))
            return False
    return False
def read_excel(sfile,conn_mysql):
    current_app.logger.info("start read excel %s"%(sfile))
    try:
        df = pd.read_excel(sfile,header=0)
    except:
        flash("请检查是否excel类型！")
        return []
    if df.shape[1]!=10:
        flash("请检查excel列数是否为10")
        return []
    df.columns=['day','buyer_id','third_position_id','position_name','third_imp','third_click','third_ecpm','third_income','third_request','bid']
    #空值校验
    if [ k for k,v in list(df.isnull().sum(axis=0).items()) if v>0]:
        flash( ','.join([ str(k)+'空值数='+str(v) for k,v in list(df.isnull().sum(axis=0).items()) if v>0])+gettime())
        return []

    df['check']=df['day'].apply(check_day)
    if [ str(k+2)  for k ,v in list(df['check'].items()) if v ==False]:
        flash( 'day异常的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        flash("day的格式例如20190101       修改成8位数字！")
        current_app.logger.info("day格式异常= %s " % (str(sfile)))
        return []
    #buyerid校验
    allbuyid_list=getall_buyerid(conn_mysql)
    current_app.logger.info("buyerid个数为"+str(len(allbuyid_list)))
    df['check']=df['buyer_id'].apply(check_buyerid,args=(allbuyid_list,))
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'buyer_id异常(没有这个buyerid或者不为数字)的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []
    #third_position_id 校验
    days=df['day'].drop_duplicates().values.tolist()
    days.sort()
    days=map(str,days)
    print days

    allthirtid=get_allthirdid(conn_mysql,days[0],days[-1])
    df['check']=df.apply(lambda x:check_posid(x['third_position_id'],allthirtid,int(x['buyer_id'])),axis=1 )
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'third_position_id异常(不能包含中文或者没有该广告位id)的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []

    df['check']=df['third_imp'].apply(check_number)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'third_imp异常的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []
    df['check']=df['third_click'].apply(check_number)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'third_click异常的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []
    df['check']=df['third_ecpm'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'third_ecpm异常的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []
    df['check']=df['third_income'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'third_income异常的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []
    df['check']=df['third_request'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'third_request异常的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []
    df['check']=df['bid'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash( 'bid异常的行='+','.join([ str(k+2)  for k ,v in list(df['check'].items()) if v ==False])+gettime())
        return []
    df.drop(['check'],axis=1,inplace=True)
    print df.head(5)
    # print df.to_numpy().tolist()
    return  df.values.tolist()
def write_db(l_list,conn_mysql):
    print("list=%s"%(l_list))
    day_sellid=list(set([ str(i[0])+"="+str(i[1]) for i in l_list]))
    print day_sellid
    for i in day_sellid:
        del_sql="delete from day_adver_third_report  where day='%s' and buyerid='%s'   "%(i.split('=')[0],i.split('=')[1])
        res=conn_mysql.executeone_notcommit(del_sql)
        if not res:
            print del_sql+"   exec fail!!!!!!"
            flash(del_sql+"   exec fail!!!!!!")
            return False
    sql="insert into day_adver_third_report (day,buyerid,third_position_id,third_position,third_imp,third_click,third_ecpm,third_income,third_request,bid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #flag=conn_mysql.executemany(sql,l_list)
    #print(flag)
    try:
        flag=conn_mysql.executemany(sql,l_list)
        if  flag:
            print "continue  commit"
            conn_mysql.commit()
        else:
            print "executemany  fail ,rollback"
            conn_mysql.rollback()
    except MySQLdb.Error as err:
        print "MySQLdb.Error"
        print err
    except MySQLdb.Warning as war:
        print "MySQLdb.war"
        print war
    except Exception,e:
        print "Exception"
        conn_mysql.rollback()
        traceback.print_exc()
        print e
        flash(e.message)
    else:
        print "else"
    finally:
        print "finally"
        # conn_mysql.rollback()
    return flag
def write_self_media_report(l_list,conn_mysql):
    l_list=[  [day,seller,imp,round(ecpm,2),round(cost,4)] for day,seller,imp,ecpm,cost in l_list]

    print("list=%s"%(l_list))
    day_sellid=list(set([ str(i[0])+"="+str(i[1]) for i in l_list]))
    print day_sellid
    for i in day_sellid:
        del_sql="delete from media_day_adver_report  where day_time='%s' and seller='%s'   "%(i.split('=')[0],i.split('=')[1])
        res=conn_mysql.executeone_notcommit(del_sql)
        if not res:
            print del_sql+"   exec fail!!!!!!"
            flash(del_sql+"   exec fail!!!!!!")
            conn_mysql.rollback()
            return False
    sql="replace into media_day_adver_report (day_time,seller,imp,ecpm,income) values('%s',%s,%s,%s,%s)"
    #flag=conn_mysql.executemany(sql,l_list)
    #print(flag)
    try:
        flag=conn_mysql.executemany(sql,l_list)
        if  flag:
            print "continue  commit"
            conn_mysql.commit()
        else:
            print "executemany  fail ,rollback"
            conn_mysql.rollback()
    except MySQLdb.Error as err:
        print "MySQLdb.Error"
        print err
    except MySQLdb.Warning as war:
        print "MySQLdb.war"
        print war
    except Exception,e:
        print "Exception"
        conn_mysql.rollback()
        traceback.print_exc()
        print e
        flash(e.message)
    else:
        print "else"
    finally:
        print "finally"
        # conn_mysql.rollback()
    return flag
def check_posid(pos,allthirtid,buyer_id):
    if len(str(pos).strip())==0:
        return False
    line = str(pos).decode('utf-8', 'ignore')
    p2 = re.compile(ur'.*?[\u4e00-\u9fa5]+.*')
    if p2.search(line) or( buyer_id >1000 and buyer_id<2000 and str(pos) not in allthirtid):
        return False
    else:
        return True
#内容输出上传
def read_content(sfile,conn_mysql):
    current_app.logger.info("start read_content excel %s" % (sfile))
    try:
        print(sfile)
        df = pd.read_excel(sfile, header=0)
        # if str(sfile).split('.')[1] not in ('xls','xlsx'):
        #     raise Exception("excelERR")
    except Exception, e:
        print(e)
        flash("请检查是否excel类型！")
        return []
    if df.shape[1] != 5:
        flash("请检查excel列数是否为5")
        return []
    df.columns = ['day', 'seller', 'imp', 'ecpm', 'cost']
    # 空值校验
    if [k for k, v in list(df.isnull().sum(axis=0).items()) if v > 0]:
        flash(
            ','.join([str(k) + '空值数=' + str(v) for k, v in list(df.isnull().sum(axis=0).items()) if v > 0]) + gettime())
        return []
    df['check'] = df['day'].apply(check_day)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('day异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        flash("day的格式例如20190101       修改成8位数字！")
        current_app.logger.info("day格式异常= %s " % (str(sfile)))
        return []
    df['check'] = df['imp'].apply(check_number)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('imp异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    df['check'] = df['ecpm'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash(
            'ecpm异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    df['check'] = df['cost'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash(
            'cost异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    df.drop(['check'], axis=1, inplace=True)
    print df.head(5)
    return df.values.tolist()
def read_jiaming(sfile,conn_mysql):
    """
    嘉明的数据校验
    :param sfile:
    :return:
    """
    current_app.logger.info("start read excel %s" % (sfile))
    try:
        print(sfile)
        df = pd.read_excel(sfile, header=0)
        # if str(sfile).split('.')[1] not in ('xls','xlsx'):
        #     raise Exception("excelERR")
    except Exception, e:
        print(e)
        flash("请检查是否excel类型！")
        return []
    if df.shape[1] != 9:
        flash("请检查excel列数是否为9")
        return []
    df.columns = ['day', 'buyer_id', 'third_position_id', 'position_name', 'third_imp', 'third_click', 'third_ecpm',
                  'third_income', 'request']
    # 空值校验
    if [k for k, v in list(df.isnull().sum(axis=0).items()) if v > 0]:
        flash(
            ','.join([str(k) + '空值数=' + str(v) for k, v in list(df.isnull().sum(axis=0).items()) if v > 0]) + gettime())
        return []

    df['check'] = df['day'].apply(check_day)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('day异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        flash("day的格式例如20190101       修改成8位数字！")
        current_app.logger.info("day格式异常= %s " % (str(sfile)))
        return []
    # buyerid校验
    allbuyid_list = getall_buyerid(conn_mysql)
    current_app.logger.info("buyerid个数为" + str(len(allbuyid_list)))
    df['check'] = df['buyer_id'].apply(check_buyerid, args=(allbuyid_list,))
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('buyer_id异常(没有这个dspid或者不为数字)的行=' + ','.join(
            [str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []

    days = df['day'].drop_duplicates().values.tolist()
    days.sort()
    days = map(str, days)
    print days

    allthirtid = get_allthirdid(conn_mysql, days[0], days[-1])
    df['check'] = df.apply(lambda x: check_posid(x['third_position_id'], allthirtid, int(x['buyer_id'])), axis=1)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('third_position_id异常的行=' + ','.join(
            [str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []

    df['check'] = df['third_imp'].apply(check_number)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('third_imp异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    df['check'] = df['third_click'].apply(check_number)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash(
            'third_click异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    df['check'] = df['third_ecpm'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash(
            'third_ecpm异常的行=' + ','.join([str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    df['check'] = df['third_income'].apply(check_decimal)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('third_income异常的行=' + ','.join(
            [str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    df['check'] = df['request'].apply(check_number)
    if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
        flash('request异常的行=' + ','.join(
            [str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
        return []
    # df['check'] = df.apply(lambda row: check_ecpm(row),axis=1 )

    # df['check'] = df.apply(lambda row:  True if row['third_imp']*row['third_ecpm']/1000==row['third_income'] else False,axis=1 )
    # df['check']=df.apply(check_ecpm,args=(df,))
    # print('check list='+ str(list(df['check'].items())))
    # if [str(k + 2) for k, v in list(df['check'].items()) if v == False]:
    #     flash('ecpm*imp/1000!=income的行=' + ','.join(
    #         [str(k + 2) for k, v in list(df['check'].items()) if v == False]) + gettime())
    #     return []

    #前三列重复校验
    check_repeat=zip(df['day'].values,df['buyer_id'].values,df['third_position_id'].values)
    if len(check_repeat) !=len(list(set(check_repeat))):
        flash('前三列有重复！ 重复数=%s'%(len(check_repeat)-len(list(set(check_repeat))) ))
        return []

    df.drop(['check'], axis=1, inplace=True)
    print df.head(5)
    # print df.to_numpy().tolist()
    return df.values.tolist()
def check_ecpm(df,*args):
    print(args)
    print(df,type(df))
    if df['third_imp']*df['third_ecpm']/1000==df['third_income']:
        return True
    else:
        return False
if __name__ == '__main__':
    sfile='D:\\data\\adverthirdupload.xlsx'
    l_list=read_excel(sfile)
    if len(l_list)==0:
        print  "请检查excel数据"
    else:
        write_db(l_list)
