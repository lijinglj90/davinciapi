from rdbbase import RdbBase
from basefunc import runcmd
import sys
import datetime
import dmPython
'''
    P达梦数据库操作实现：
    提供通过psql客服端和PG数据库python驱动dmPython接口访问两种方式实现对PG数据库的访问
    1）psql：需按照psql客服端工具，通过其实现调用
    2）dmPython：按照方法为“https://docs.qq.com/doc/DY3R0ekVXUWlNZ3Fl”
'''

#达梦
class RdbDSql(RdbBase):

    def __init__(self):
        super(RdbDSql,self).__init__()
        # self.dbtype = "QDISQL"
        self.dbtype = "QDMOCI"

    def exec_sql_bycmd(self,para:str,exec_type:int = 1):
        if exec_type == 0:
            exec_cmd = "disql %s/%s@%s:%s -E %s" %(self.user,self.passwd,\
                self.host,self.port,para)
        else:
            exec_cmd = "disql %s/%s@%s:%s  \'%s\'" %(self.user,self.passwd,\
                self.host,self.port,para)

        #执行命令
        ret,info,data = runcmd(exec_cmd)
        return ret,info,data

    def exec_sql(self, sql: str):
        # 打开数据库连接,执行sql，没有返回值
        print('执行的是达梦数据库exec_sql', self.host, self.port, self.database, self.user, self.passwd)
        db = dmPython.connect(server=self.host, port=int(self.port), user=self.user, password=self.passwd)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        ret = True
        info = ""
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 输出异常信息
            err_info = sys.exc_info()
            info = "达梦执行[%s]异常:错误号[%s],错误描述[%s]" % (sql, err_info[0], err_info[1])

            # 发生错误时回滚
            db.rollback()
            ret = False

        # 关闭数据库连接
        db.close()
        return ret, info, None

    def exec_querry(self, sql: str,return_type:str='3'):
        # 打开数据库连接，执行sql，有返回值
        print('执行的是达梦数据库', self.host, self.port, self.database, self.user, self.passwd)
        db = dmPython.connect(server=self.host, port=int(self.port), user=self.user, password=self.passwd)
        # db = dmPython.connect(user='SYSDBA', password='SYSDBA', server='10.8.8.26', port=5236)

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        ret = True
        info = ""
        data = []
        results = []
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            fields = cursor.description
            colnames = []
            for col in range(len(fields)):
                colnames.append(fields[col][0])
            data.append(colnames)

            for row in results:
                row_data = []
                for i in range(len(fields)):
                    if isinstance(row[i], datetime.datetime):
                        row_new = row[i].strftime("%Y-%m-%d %H:%M:%S")
                        row_data.append(row_new)
                        continue
                    if isinstance(row[i], bytes):
                        # print(row[i])
                        # row_new = decrypt(row[i])
                        row_new = str(row[i])
                        row_data.append(row_new)
                        continue
                    if isinstance(row[i], int):
                        row_new = str(row[i])
                        row_data.append(row_new)
                        continue
                    row_data.append(str(row[i]))
                data.append(row_data)
        except:
            # 输出异常信息
            err_info = sys.exc_info()
            info = "达梦执行[%s]异常:错误号[%s],错误描述[%s]" % (sql, err_info[0], err_info[1])

            # 发生错误时回滚
            db.rollback()
            ret = False

        # 关闭数据库连接
        db.close()

        # 根据return_type返回对应的格式
        # print('@@@@@@@@@@@@@@',results, data)
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

    def exec_querry_obj(self,tableinfo:str,filterinfo:str,querryfield:str):
        pass

    def exec_excute_obj(self,tableinfo:str,filterinfo:str,modifyfield:str,modifyvalue:str):
        pass