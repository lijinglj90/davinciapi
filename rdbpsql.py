from rdbbase import RdbBase
from basefunc import runcmd
'''
    PG数据库操作实现：
    提供通过psql客服端和PG数据库python驱动psycopg2接口访问两种方式实现对PG数据库的访问
    1）psql：需按照psql客服端工具，通过其实现调用
    2）psycopg2：按照方法为“pip install psycopg2" 
'''

import psycopg2
class RdbPSql(RdbBase):

    def __init__(self):
        super(RdbPSql,self).init__()
        self.dbtype = "QPGSQL"

    def exec_sql_bycmd(self,para:str,exec_type:int = 1):
        if exec_type == 0:
            exec_cmd = "psql -h%s -p%s -d%s -U%s -W%s -c\'%s\'" %(self.host,self.port,\
                self.database,self.user,self.passwd,para)
        else:
            exec_cmd = "psql -h%s -p%s -d%s -U%s -W%s -f%s" %(self.host,self.port,\
                self.database,self.user,self.passwd,para)
        
        #执行命令
        ret,info,data = runcmd(exec_cmd)
        return ret,info,data
    
    def exec_sql(self,sql:str):
        # 打开数据库连接
        db = psycopg2.connect(host=self.host, port=int(self.port),user=self.user, passwd=self.passwd, db=self.database,charset='utf8' )

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
    
    def exec_querry(self,sql:str):
        # 打开数据库连接
        db = psycopg2.connect(host=self.host, port=int(self.port),user=self.user, passwd=self.passwd, db=self.database,charset='utf8' )

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
                    row_data.append(row[i])
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
        return ret,info,data

    def exec_querry_obj(self,tableinfo:str,filterinfo:str,querryfield:str):
        pass

    def exec_excute_obj(self,tableinfo:str,filterinfo:str,modifyfield:str,modifyvalue:str):
        pass