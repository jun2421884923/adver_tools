# -*- coding: utf-8 -*-

from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,DateField
from wtforms.validators import DataRequired,NumberRange,Regexp
import datetime
from project.util.common import *


class LoginForm(FlaskForm):
    # 域初始化时，第一个参数是设置label属性的
    username = StringField('用户名:', validators=[DataRequired()])
    password = PasswordField('密码:  ', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)


class SugSearchForm(FlaskForm):
    keyword = StringField('sug搜索:')


class EcpmSearchForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(EcpmSearchForm, self).__init__(*args, **kwargs)
        if not self.startday.data or not self.endday:
            self.startday.data = getday1(-1)
            self.endday.data=getday1(-1)
    startday = StringField(label='开始日期:',default=getday1(-1))
    endday = StringField(label='结束日期:',default=getday1(-1))
    buyerid = StringField('客     户  id   : ')
    impid = StringField('广告位 id:')
class ImpidMappingForm(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(ImpidMappingForm, self).__init__(*args, **kwargs)
        if not self.startday.data or not self.endday:
            self.startday.data = getday1(-1)
            self.endday.data=getday1(-1)
    startday = StringField(label='开始日期:',default=getday1(-1))
    endday = StringField(label='结束日期:',default=getday1(-1))
    sellerid = StringField('媒体id: ')
    dspid    = StringField('dspid:')
    thirdid    = StringField('第三方广告位id:')
    impid    = StringField('广告位id:')
class SellerSearchForm(FlaskForm):
    sellername = StringField('媒体名:')
