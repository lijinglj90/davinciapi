from rdbbase import RdbBase
from basefunc import runcmd
#import MySQLdb
import pymysql
import sys
import datetime
from splitcfg import SplitSymbol
import base64
from Crypto.Cipher import AES
import struct


def decrypt(text):
    secret = "3.14159265358979"
    # base64_decrypted = base64.decodebytes(text.encode('utf-8'))  #把text转为utf-8编码格式的字节,再转换为二进制64位的字节
    base64_decrypted = base64.b64decode(text)  # base64编码转换为二进制文件
    mode = AES.MODE_ECB  # 表示模式是ECB模式
    cryptor = AES.new(secret.encode('utf-8'), mode)  # 创建一个aes对象
    plain_text = cryptor.decrypt(base64_decrypted)  # decrypt解密  encrypt加密
    return struct.unpack('d', plain_text[:8])[0]  # struct.unpack按照给定的格式(fmt)解析字节流string，返回的数据类型是元祖

class RdbMysql(RdbBase):

    def __init__(self):
        super(RdbMysql,self).__init__()
        self.dbtype = "mysql"

    def exec_sql_bycmd(self,para:str,exec_type:int = 1):
        if exec_type == 0:
            exec_cmd = "mysql -h %s -P %s -u %s -p \"%s\" -e \"%s\"" %(self.host,\
                self.port,self.user,self.passwd,para)
        else:
            exec_cmd = "mysql -h %s -P %s -u %s -p \"%s\" -e \"source %s\"" %(self.host,\
                self.port,self.user,self.passwd,para)
        
        #执行命令
        ret,info,data = runcmd(exec_cmd)
        return ret,info,data

    def exec_sql(self,sql:str):
        # 打开数据库连接,执行sql，没有返回值
        # db = MySQLdb.connect(host=self.host, port=int(self.port),user=self.user, passwd=self.passwd, db=self.database,charset='utf8' )
        db = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.database,charset='utf8')

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
            #输出异常信息  
            err_info = sys.exc_info()  
            info = "mysql执行[%s]异常:错误号[%s],错误描述[%s]" %(sql,err_info[0],err_info[1]) 
            
            # 发生错误时回滚
            db.rollback()
            ret = False

        # 关闭数据库连接
        db.close()
        return ret,info,None
    
    def exec_querry(self,sql:str,return_type:str='3'):
        # 打开数据库连接，执行sql，有返回值
        # db = MySQLdb.connect(host=self.host, port=int(self.port),user=self.user, passwd=self.passwd, db=self.database,charset='utf8' )
        db = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.database,charset='utf8',read_timeout=60, write_timeout=60)
        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()

        ret = True
        info = ""
        data = []
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
                        row_new = decrypt(row[i])
                        row_data.append(row_new)
                        continue
                    if isinstance(row[i], int):
                        row_new = str(row[i])
                        row_data.append(row_new)
                        continue
                    row_data.append(str(row[i]))
                data.append(row_data)
        except:
            #输出异常信息  
            err_info = sys.exc_info()  
            info = "mysql执行[%s]异常:错误号[%s],错误描述[%s]" %(sql,err_info[0],err_info[1]) 
            
            # 发生错误时回滚
            db.rollback()
            ret = False

        # 关闭数据库连接
        db.close()
        #根据return_type返回对应的格式
        # print('@@@@@@@@@@@@@@',results, data)
        #两行两列：sql="SELECT AVERAGE,DTMAXVAL FROM hdranastat5m20220925 WHERE id=49 AND hdtime <= '2022-09-25 00:05:00'"
        if return_type in ['3',3]:
            """
              # list 值 例：
              两行两列: (True, '', [['4311.416016', '2022-09-24 23:56:28'], ['4290.012695', '2022-09-25 00:00:05']])
              一行值：(True, '', ['4311.416016', '4869.40625'])
              一列值：(True, '', [['4311.416016'], ['4290.012695']])
              单个值：(True, '', ['4311.416016'])
            """
            if len(data)== 2 :
                data_l1 = data[1]
            else:
                data_l1 = data[1:]
            return ret,info,data_l1
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
            return ret,info,data_l5
        elif return_type in ["6", 6]:
            """
            两行两列: (True, '', [['AVERAGE', 'DTMAXVAL'], ['4311.416016', '2022-09-24 23:56:28'], ['4290.012695', '2022-09-25 00:00:05']])
            一行值：(True, '', [['AVERAGE', 'MAXVAL'], ['4311.416016', '4869.40625']])
            一列值：(True, '', [['AVERAGE'], ['4311.416016'], ['4290.012695']])
            单个值：(True, '', [['AVERAGE'], ['4311.416016']])
            """
            return ret,info,data
        else:
            return False, "请输入对应的返回类型", []


    def exec_querry_obj(self,tableinfo:str,filterinfo:str,querryfield:str):
        pass

    def exec_excute_obj(self,tableinfo:str,filterinfo:str,modifyfield:str,modifyvalue:str):
        pass

