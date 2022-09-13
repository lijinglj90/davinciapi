from rdbbase import RdbBase
from basefunc import runcmd
#mport ksycopg2

class RdbKing(RdbBase):

    def __init__(self):
        super(RdbKing,self).__init__()
        self.dbtype = "QKQSL"

    def exec_sql_bycmd(self,para:str,exec_type:int = 1):
        if exec_type == 0:
            exec_cmd = "ksql -h %s -p %s -d %s -U %s -W %s -c \'%s\'" %(self.host,self.port,\
                self.database,self.user,self.passwd,para)
        else:
            exec_cmd = "ksql -h %s -p %s -d %s -U %s -W %s -f %s" %(self.host,self.port,\
                self.database,self.user,self.passwd,para)
        
        #执行命令
        ret,info,data = runcmd(exec_cmd)
        return ret,info,data
    
    def exec_sql(self,sql:str):
        pass

    def exec_querry(self,sql:str):
        pass