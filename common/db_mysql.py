#encoding=utf-8
import time
import pymysql
class MySQL:
    def __init__(self,host,user,pwd,db,charset='utf-8'):
        self.host=host
        self.user=user
        self.pwd=pwd
        self.db=db
    def GetConnect(self):
        self.connect=pymysql.connect(self.host,self.user,self.pwd,self.db,charset='utf-8')
        cur=self.connect.cursor()
    def ExecSql(self,sql):
        cur=self.GetConnect()
        cur.execute(sql)
        self.connect.commit()
        self.connect.close()
    def ExecQuery(self,sql):
        cur=self.GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.connect.close()
        return resList  