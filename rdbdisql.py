from rdbbase import RdbBase
from basefunc import runcmd
class RdbDSql(RdbBase):

    def __init__(self):
        super(RdbDSql,self).init__()
        self.dbtype = "QDISQL"

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
    
    def exec_sql(self,sql:str):
        pass

    def exec_querry(self,sql:str):
        pass