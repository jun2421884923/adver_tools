
#coding=utf-8
import  pymysql as MySQLdb
from project.settings import  dbconfig


class MysqlUtil():
    def __init__(self,bind='self'):
        self._bind=bind
        self.conn = MySQLdb.connect(host=dbconfig[self._bind]["host"] \
                                    , user=dbconfig[self._bind]["user"] \
                                    , passwd=dbconfig[self._bind]["password"] \
                                    , db=dbconfig[self._bind]["database"] \
                                    , port=dbconfig[self._bind]["port"] \
                                    , charset='utf8' \
                                    )
    def excute(self, sql_cmd):
        results = []
        try:
            if sql_cmd:
                cur = self.conn.cursor()
                cur.execute(sql_cmd)
                results = cur.fetchall()
                cur.close()
                return True, results
        except Exception as e:
            print(e)
        return False, results
    def executemany(self,sql,data_list):
        try:
            if sql:
                cur = self.conn.cursor()
                cur.executemany(sql,data_list)
                self.conn.commit()
                cur.close()
            return True
        except Exception as e:
            print (e)
            return False
        return False
    def executeone_commit(self,sql):
        try:
            if sql:
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
                cur.close()
            return True
        except Exception as e:
            print (e)
        return False
    def executeone_notcommit(self,sql):
        try:
            if sql:
                cur = self.conn.cursor()
                cur.execute(sql)

            return True
        except Exception as e:
            print (e)
        return False
    def disconnect(self):
        if self.conn:
            self.conn.close()
    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()
























