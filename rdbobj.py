import os
from rdbmysql import RdbMysql
from rdbdisql import RdbDSql
from rdbking import RdbKing
from rdbpsql import RdbPSql

class RdbObj():
    def __init__(self, dbtype:str = "",concectstr:str = ""):
        '''利用环境变量初始化连接参数'''
        mytype = ""
        if dbtype == "":
            mytype = os.getenv('TEST_DB1_TYPE', 'QMYSQL')
        else :
            mytype = dbtype

        if mytype == "QMYSQL":
            self.dbobj = RdbMysql()
        elif mytype == "QKSQL":
            self.dbobj = RdbKing()
        elif mytype == "QDSQL":
            self.dbobj = RdbDSql()
        elif mytype == "QPSQL":
            self.dbobj = RdbPSql()
        else:
            self.dbobj = None

        self.dbobj.setconnectpara(concectstr)
        # self.dbobj.setconnectpara(hostname, port, database, username, passwd)
        # self.dbobj.setconnectpara("10.8.8.21","3306","DAVINCI","sa","cast1234")

    def exec_sql_bycmd(self,para:str,exec_type:int = 1):
        if self.dbobj is None:
            ret = False
            info = "dbobj-数据库类型 为不支持对象"
            data = None
        else:
            ret,info,data = self.dbobj.exec_sql_bycmd(para,exec_type)
        return ret,info,data
    
    def exec_sql(self,sql:str):
        if self.dbobj is None:
            ret = False
            info = "dbobj-数据库类型 为不支持对象"
            data = None
        else:
            ret,info,data = self.dbobj.exec_sql(sql)
        return ret,info,data

    def exec_querry(self,sql:str,return_type='3'):
        if self.dbobj is None:
            ret = False
            info = "dbobj-数据库类型 为不支持对象"
            data = None
        else:
            ret,info,data = self.dbobj.exec_querry(sql,return_type)
        return ret,info,data       
    
    # def exec_sql_bycmd(self,para:str,exec_type:int = 1):
    #     if self.dbobj is None:
    #         ret = False
    #         info = "dbobj 为不支持对象"
    #         data = None
    #     else:
    #         ret,info,data = self.dbobj.exec_sql_bycmd(para,exec_type)
    #     return ret,info,data


if __name__ == '__main__':
    # aql = "SELECT VERSION()"
#     # aql = "SELECT AVERAGE FROM hdranastat5m_jm_20220414 h WHERE h.ID = (SELECT a.ID FROM analoginput a left join plant p on a.EQUIPMENTCONTAINER_ID = p.id WHERE a.TYPE = (SELECT m.ID FROM measurementtype m WHERE m.`NAME` = 'p')  AND a.EQUIPMENTCONTAINER_TABLEID = 1071) AND h.HDTIME ='2022-04-14 00:05:00'"
#     # aql = "select a.*,b.* from (SELECT AVERAGE FROM hdranastat5m_jm_20220414 h WHERE h.ID = (SELECT a.ID FROM analoginput a left join plant p on a.EQUIPMENTCONTAINER_ID = p.id WHERE a.TYPE = (SELECT m.ID FROM measurementtype m WHERE m.`NAME` = 'p')  AND a.EQUIPMENTCONTAINER_TABLEID = 1071) AND h.HDTIME ='2022-04-14 00:05:00') a,(select datatime turbinetheoryp,availableturbine,metertheoryp,availablemeter,modetheoryp,availablemode from hdrtheorypdata5m_jm_20220414 h left join plant p on h.obj_id=p.id  WHERE objtable_id = 1071  AND fcst_nodetype = 1 AND datatime = '2022-04-14 00:05:00')b"
#     # aql = "select id, PLANT_TYPE from plant where ALIASNAME = '中广核民勤风电场'"
#     # aql = "select id, PLANT_TYPE from plant where ALIASNAME = '龙头风电场'"
#     # aql = "select a.ava,b.ave,(a.ava-b.ave)*100/b.ave,substring(a.datatime,11,6)as time from (select datatime,availableturbine ava from hdrtheorypdata20220331  where datatime='2022-03-31 00:00:00')a,(select AVERAGE ave FROM hdranastat20220331 h WHERE h.ID =(SELECT a.ID FROM analoginput a WHERE a.TYPE =(SELECT m.ID FROM measurementtype m WHERE m.`NAME` = 'p') AND a.EQUIPMENTCONTAINER_ID = 115020 AND a.EQUIPMENTCONTAINER_TABLEID = 1071) AND h.HDTIME ='2022-03-31 00:00:00')b"
#     # aql = "SELECT * from wind_turbine where PLANT_ID = 115093 and ALIASNAME = '风机_1'"
#     aql = "SELECT alarmstring FROM hdralarmbase20210415 WHERE dttimestamp='2021-04-15 08:23:05'"
    aql = "SELECT p/((select cap from plantcap where id=1)/(SELECT RUN_CAPACITY from plant)) from hdrsfcstdata_llgf where record_id=(SELECT id FROM hdrsfcstrecord2022 WHERE powertype = 0 AND fcst_time = '2022-08-08 12:15:00')"
    c = RdbObj('QMYSQL','10.64.14.126@_@_@_@_').exec_querry(aql,return_type='3')
#     c = RdbObj()
#     c = RdbObj('QMYSQL').exec_querry(aql,return_type='4')
    print(c)
    print(len(c[-1]))
