import os
from rdbmysql import RdbMysql
from rdbdisql import RdbDSql
from rdbking import RdbKing
from rdbpsql import RdbPSql
from rdbinsql import RdbInSql
import evnobj as eo

class RdbObj():
    def __init__(self, dbtype:str = "",concectstr:str = "",baseevn:str = ""):
        '''设置基本环境变量'''
        print('用户传入的数据类型为：', dbtype)
        print('@@@@RdbObj()的baseevn值', baseevn)
        if len(baseevn) > 0:
            eo.setevn(baseevn)

        '''利用环境变量初始化连接参数'''
        mytype = ""
        # if dbtype == "":
        if dbtype in ["","_","ALL","all"]:
            mytype = os.getenv('TEST_DB1_TYPE', 'QMYSQL')
            print('环境变量获取的数据类型为：', mytype)
        else :
            mytype = dbtype


        if mytype == "QMYSQL":   #mysql数据库QMYSQL
            self.dbobj = RdbMysql()
        elif mytype in ["QKSQL","QKINGBASE"]:   #金仓数据库QKSQL
            self.dbobj = RdbKing()
        elif mytype in ["QDSQL","QDMOCI"]:   #达梦数据库QDMOCI
            self.dbobj = RdbDSql()
        elif mytype == "QPSQL":   #瀚高数据库QPSQL
            self.dbobj = RdbPSql()
        elif mytype == "QINSQL":
            self.dbobj = RdbInSql()  #influxdb数据库
        else:
            self.dbobj = None

        self.dbobj.setconnectpara(concectstr)
        # self.dbobj.setconnectpara(hostname, port, database, username, passwd)
        # self.dbobj.setconnectpara("10.8.8.21","3306","DAVINCI","sa","cast1234")
        self.mytype = mytype
        # print('最后使用的数据类型为：', self.mytype)

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
#     aql = "SELECT p/((select cap from plantcap where id=1)/(SELECT RUN_CAPACITY from plant)) from hdrsfcstdata_llgf where record_id=(SELECT id FROM hdrsfcstrecord2022 WHERE powertype = 0 AND fcst_time = '2022-08-08 12:15:00')"
#     c = RdbObj('QMYSQL','10.64.14.126@_@_@_@_').exec_querry(aql,return_type='3')
#     c = RdbObj()
#     c = RdbObj('QMYSQL').exec_querry(aql,return_type='4')
    #SELECT windpower 日风功率密度 FROM fdayform WHERE DATATIME = '2022-09-25 00:00:00'~QMYSQL~10.64.14.70@_@davinci@_@_~3
    # aql = "select left(datatime,4),LIRRAVG,LIRRAMAX,LIRRADIATION ,GRIDPMAXTIME,GRIDPMAX, ACCUMPOWER/10,THEORYSUMP/10,LABLEHOUR,LSUMSUNLIGHT,FANAVGWIND,AVGTEMPERATURE,AVGMODULETEMPERATURE, ACCDIRECTR,ACCFIFFRAD,ifnull(INCLINEIRR,'nan') from fyearform where objtable_id = 1071 and obj_id = 115020 and datatime='2022-01-01 00:00:00' order by datatime"
    # aql = "SELECT AVERAGE,DTMAXVAL FROM hdranastat5m20220925 WHERE id=49 AND hdtime <= '2022-09-25 00:05:00'"
    # aql = "SELECT AVERAGE FROM hdranastat5m20220925 WHERE id=49 AND hdtime <= '2022-09-25 00:00:00'"

    # c = RdbObj('QMYSQL', '10.64.14.69@_@DAVINCI@_@').exec_querry(aql, return_type='3')
    # print(c)

    # qq = "select * from testing"
    # c = RdbObj('QMYSQL', '10.8.8.200@8086@test@admin@123456').exec_querry(qq, return_type='3')
    # print(c)
    # print(len(c[-1]))

    qq = "select * from davinci_main_databak.hdr_analoginput20220829"
    c = RdbObj('QDSQL', '10.8.8.201@5236@_@SYSDBA@SYSDBA').exec_querry(qq, return_type='3')
    print(c)
    # print(len(c[-1]))

