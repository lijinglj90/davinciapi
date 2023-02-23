"""
encoding: utf-8
@file: rdbinsql.py
@author: james
@time: 2022/10/21 10:11
@desc:
"""
from rdbbase import RdbBase
from basefunc import runcmd
from influxdb import InfluxDBClient
import sys



class RdbInSql(RdbBase):

    def __init__(self):
        super(RdbInSql, self).__init__()
        self.dbtype = "influxdb"

    def exec_sql_bycmd(self, para: str, exec_type: int = 1):
        if exec_type == 0:
            # exec_cmd = "influxdb -h %s -P %s -u %s -p \"%s\" -e \"%s\"" % (self.host, \
            #                                                             self.port, self.user, self.passwd, para)
            exec_cmd = "influx -username %s -password \"%s\" " % (self.user, self.passwd)
        else:
            # exec_cmd = "influxdb -h %s -P %s -u %s -p \"%s\" -e \"source %s\"" % (self.host, \
            #                                                                    self.port, self.user, self.passwd, para)
            exec_cmd = "influx -username %s -password \"%s\" " % (self.user, self.passwd)

            # 执行命令
        ret, info, data = runcmd(exec_cmd)
        return ret, info, data

    def exec_sql(self, sql: str):
        # 打开数据库连接,执行sql，没有返回值
        db_clinet = InfluxDBClient(host=self.host, port=int(self.port), username=self.user, password=self.passwd, database=self.database, timeout=60)

        ret = True
        info = ""
        try:
            # 执行SQL语句
            db_clinet.query(sql)
        except:
            # 输出异常信息
            err_info = sys.exc_info()
            info = "influxdb执行[%s]异常:错误号[%s],错误描述[%s]" % (sql, err_info[0], err_info[1])
            ret = False
        return ret, info, None

    def exec_querry(self, sql: str, return_type: str = '3'):
        # 打开数据库连接，执行sql，有返回值
        db_clinet = InfluxDBClient(host=self.host, port=int(self.port), username=self.user, password=self.passwd, database=self.database)
        ret = True
        info = ""
        data = []
        count = 0
        try:
            # 执行SQL语句
            results = db_clinet.query(sql)
            # 获取所有记录列表
            for measurement in results.get_points():
                count +=1
                if(count==1):
                    colnames=list(measurement.keys())
                    data.append(colnames)
                values=measurement.values()
                data.append(list(values))

        except:
            # 输出异常信息
            err_info = sys.exc_info()
            info = "influxdb执行[%s]异常:错误号[%s],错误描述[%s]" % (sql, err_info[0], err_info[1])
            ret = False


        # 根据return_type返回对应的格式
        print('@@@@@@@@@@@@@@就是想看看有没有返回值', 'results:', results, 'data:', data, 'return_type:', return_type, 'ret:', ret,
              'info:', info)
        # 两行两列：sql="SELECT AVERAGE,DTMAXVAL FROM hdranastat5m20220925 WHERE id=49 AND hdtime <= '2022-09-25 00:05:00'"
        if return_type in ['3', 3]:
            """
              # list 值 例：
              两行两列: (True, '', [['4311.416016', '2022-09-24 23:56:28'], ['4290.012695', '2022-09-25 00:00:05']])
              一行值：(True, '', ['4311.416016', '4869.40625'])
              一列值：(True, '', [['4311.416016'], ['4290.012695']])
              单个值：(True, '', ['4311.416016'])
            """
            if len(data) == 2:
                data_l1 = data[1]
            else:
                data_l1 = data[1:]
            return ret, info, data_l1
        elif return_type in ["4", 4]:
            """
            str 值 例：
            两行两列: (True, '', '4311.416016,2022-09-24 23:56:28,4290.012695,2022-09-25 00:00:05')
            一行值：(True, '', '4311.416016,4869.40625')
            一列值：(True, '', '4311.416016,4290.012695')
            单个值：(True, '', '4311.416016')
            """
            data_l4 = ''
            if len(data) == 2:
                l4 = []
                for i in data[1]:
                    l4.append(str(i))
                data_l4 = ",".join(l4)
            else:
                l4 = []
                for i in range(1, len(data)):
                    for j in data[i]:
                        l4.append(str(j))
                    data_l4 = ",".join(l4)
            return ret, info, data_l4
        elif return_type in ["5", 5]:
            """
            list-dict 例：
            两行两列: (True, '', [{'AVERAGE': '4311.416016', 'DTMAXVAL': '2022-09-24 23:56:28'}, {'AVERAGE': '4290.012695', 'DTMAXVAL': '2022-09-25 00:00:05'}])
            一行值：(True, '', [{'AVERAGE': '4311.416016', 'MAXVAL': '4869.40625'}])
            一列值：(True, '', [{'AVERAGE': '4311.416016'}, {'AVERAGE': '4290.012695'}])
            单个值：(True, '', [{'AVERAGE': '4311.416016'}])
            """
            data_l5 = []
            for i in range(1, len(data)):
                data_l5.append(dict(zip(data[0], data[i])))
            return ret, info, data_l5
        elif return_type in ["6", 6]:
            """
            两行两列: (True, '', [['AVERAGE', 'DTMAXVAL'], ['4311.416016', '2022-09-24 23:56:28'], ['4290.012695', '2022-09-25 00:00:05']])
            一行值：(True, '', [['AVERAGE', 'MAXVAL'], ['4311.416016', '4869.40625']])
            一列值：(True, '', [['AVERAGE'], ['4311.416016'], ['4290.012695']])
            单个值：(True, '', [['AVERAGE'], ['4311.416016']])
            """
            return ret, info, data
        else:
            return False, "请输入对应的返回类型", []

    def exec_querry_obj(self, tableinfo: str, filterinfo: str, querryfield: str):
        pass

    def exec_excute_obj(self, tableinfo: str, filterinfo: str, modifyfield: str, modifyvalue: str):
        pass

