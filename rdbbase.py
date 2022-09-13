#coding:utf-8
from abc import ABCMeta,abstractmethod
import os
from splitcfg import SplitSymbol
class RdbBase(metaclass=ABCMeta):
    '''关系数据库访问接口
        提供执行sql脚本和sql脚本文件的接口
    '''
    def __init__(self):
        '''利用环境变量初始化连接参数'''
        hostname = os.getenv('TEST_DB1_HOST', 'localhost')
        self.host = hostname
        
        port = os.getenv('TEST_DB1_PORT', '3306')
        self.port = port
        
        username = os.getenv('TEST_DB1_USER', 'sa')
        self.user = username

        database = os.getenv('TEST_DB1_DATABASE', 'DAVINCI')
        self.database = database
        
        passwd = os.getenv('TEST_DB1_PASSWD', 'cast1234')
        self.passwd = passwd

        dbtype = os.getenv('TEST_DB1_TYPE', 'QMYSQL')
        self.dbtype = dbtype

        # print('系统默认',self.host, self.port, self.database, self.user, self.passwd)

    # def setconnectpara(self,hostname='',port='',database='',username='',passwd=''):
    def setconnectpara(self,concectstr=''):
        data = concectstr.split(SplitSymbol.SYMBOL_BETWEEN_ELEMENTS_IN_CONDITION)
        print(data)
        if len(data) == 5:
            if data[0] not in ['', '_']:
                self.host = data[0]
            if data[1] not in ['', '_']:
                self.port = data[1]
            if data[2] not in ['', '_']:
                self.database = data[2]
            if data[3] not in ['', '_']:
                self.user = data[3]
            if data[4] not in ['', '_']:
                self.passwd = data[4]
            print('用户传参', self.host, self.port, self.database, self.user, self.passwd)
        else:
            print('使用系统默认', self.host, self.port, self.database, self.user, self.passwd)
            pass


    @abstractmethod
    def exec_sql_bycmd(self,para:str,exec_type:int = 1):
        pass

    @abstractmethod
    def exec_sql(self,sql:str):
        pass

    @abstractmethod
    def exec_querry(self,sql:str,return_type:int):
        pass

    @abstractmethod
    def exec_querry_obj(self, tableinfo: str, filterinfo: str, querryfield: str):
        pass

    # @abstractmethod
    # def exec_querry_obj(self, tableinfo: str, filterinfo: str, modifyfield: str, modifyvalue: str):
    #     pass