# -*- coding: utf-8 -*-

from project import db
from sqlalchemy.orm import relationship
from sqlalchemy import PrimaryKeyConstraint,ForeignKey



from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'dsp_users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    password = db.Column(db.String(30))
    __table_args__ = {'schema': 'adver_report'}

    def __init__(self, username):

        self.username = username
        self.id = self.get_id()

    def get_id(self):
        """get user id from profile file, if not exist, it will
        generate a uuid for the user.
        """
        if self.username is not None:
            try:
                us = User.query.filter(User.username == self.username).first()
                if us:
                    return us.id
                else:
                    return 0
            except IOError:
                pass
            except ValueError:
                pass
        return 0

    @staticmethod
    def get(user_id):
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not user_id:
            return None
        try:
            return User.query.filter(User.id == user_id).first()
        except Exception, e:
            print(e)
            return None
        return None

    @staticmethod
    def query_by_username(username):
        return User.query.filter(User.username == str(username)).first()

    @property
    def pwd(self):
        raise AttributeError(u'密码不可读')

    @pwd.setter
    def pwd(self, pwd):
        self.password = pwd

    def verify_password(self, pwd):
        if self.query_by_username(self.username):
            return User.query.filter(User.username == self.username).first().password == pwd
        else:
            return False

    def __repr__(self):
        return '<User:%s,password:%s,id:%s>' % (self.username, self.password, self.id)


class DspInfo(db.Model):
    __tablename__ = 'dsp_info'
    __table_args__ = (
        PrimaryKeyConstraint('dspid', 'buyerid'),
        {'schema': 'video_adver'}
    )
    dspid = db.Column(db.Integer)
    buyerid = db.Column(db.Integer)
    name = db.Column(db.String(200), default='')
    isvalid = db.Column(db.Integer, default=1)

    def __init__(self, dspid, buyerid, name, isvalid):
        self.dspid = dspid
        self.buyerid = buyerid
        self.name = name
        self.isvalid = isvalid

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    # 配合todict一起使用
    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v

    def __repr__(self):
        return '{"dspid":"%s","buyerid":"%s","name":"%s","isvalid":"%s"}' % (
        self.dspid, self.buyerid, self.name, self.isvalid)


class SugInfo(db.Model):
    __tablename__ = 'app_wise_sug_score'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {'schema': 'video_adver'}
    )
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sug = db.Column(db.String(1000))
    score = db.Column(db.String(50))
    site = db.Column(db.String(50))
    date = db.Column(db.Integer)

    def __init__(self, sug, score, site, date):
        self.sug = sug
        self.score = score
        self.site = site
        self.date = date

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    # 配合todict一起使用
    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v

    def __repr__(self):
        return '{"sug":"%s","score":"%s","site":"%s","date":"%s"}' % \
               (self.sug, self.score, self.site, self.date)


class AdxRecentEcpm(db.Model):
    __tablename__ = 'adx_recent_ecpm'
    __table_args__ = (
        PrimaryKeyConstraint('day', 'buyerid','third_position_id','impid'),
        {'schema': 'video_adver'}
    )
    day = db.Column(db.Integer)
    buyerid = db.Column(db.String(100))
    third_position_id = db.Column(db.String(100))
    impid = db.Column(db.Integer)
    third_ecpm=db.Column(db.DECIMAL)
    stype = db.Column(db.Integer)

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    # 配合todict一起使用
    def to_json(all_vendors):
        v = [ven.dobule_to_dict() for ven in all_vendors]
        return v
class AdxSspAdposition(db.Model):
    __tablename__ = 'adx_ssp_adposition'
    __table_args__ = (
        {'schema': 'video_adver'}
    )
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))

class AdverSspBuyerInfo(db.Model):
    __tablename__ = 'adver_ssp_buyer_info'
    __table_args__ = (
        {'schema': 'video_adver'}
    )
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))
class AdxDspInfo(db.Model):
    __tablename__ = 'adx_dsp_info'
    __table_args__ = (
        {'schema': 'video_adver'}
    )
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))
class AdxDspPositionHistory(db.Model):
    __tablename__ = 'adx_dsp_position_history'
    __table_args__ = (
        {'schema': 'video_adver'}
    )
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    day = db.Column(db.Integer)
    sellerid = db.Column(db.Integer)
    dspid = db.Column(db.Integer)
    thirdid = db.Column(db.String(100))
    impid = db.Column(db.Integer)
class AdxSspInfo(db.Model):
    __tablename__ = 'adx_ssp_info'
    __table_args__ = (
        {'schema': 'video_adver'}
    )
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))
class AdxSspInfoWeight(db.Model):
    __tablename__ = 'adx_ssp_info_weight'
    __table_args__ = (
        {'schema': 'video_adver'}
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    weight=db.Column(db.DECIMAL)
    update_time=db.Column(db.DateTime)

    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result




