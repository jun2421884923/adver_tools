# -*- coding: utf-8 -*-
import json
dict_result={
    0:"success",
    1:"error"
}

class results(object):
    def __init__(self, statuscode=0,data=None):
        self.__errno = statuscode
        self.__data = {}
        self.__data['list']=data
        self.__msg = dict_result[self.__errno]

    def set_statuscode(self, statuscode):
        self.__errno = statuscode
        self.__msg = dict_result[self.__errno]
    def set_data(self,data):
        self.__data['list']=data

    def set_resultMsg(self, msg):
        self.__msg = msg

    def get_statuscode(self):
        return self.__errno
    def get_resultMsg(self):
        return self.__msg

    def get_data(self):
        return self.__data
    def __str__(self):
        return json.dumps({"errno":self.__errno,"data":self.__data,"msg":self.__msg})