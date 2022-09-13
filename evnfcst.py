from evnbase import EnvBase 
import os
from inicfg import IniCfg

class EnvFcst(EnvBase):
	''' 业务系统环境变量和基础参数配置接口基类'''
	
	def __init__(self):
		#调用父类构造
		super(EnvFcst, self).__init__()
		
		#获取DAVINCI环境变量
		temp = os.getenv('DAVINCI')
		if temp is None or temp == "":
			return
		
		self.dict_env["DAVINCI"] = temp
		
		#获取工程目录名和工程路径，key为"PROJECTNAME"和"PROJECTPATH"
		path = temp + "/etc/system.cfg"
		
		_,_,value = IniCfg.readvalue_static(path,"project@@name")
		if (not value is None) and value != "":
			self.dict_env["PROJECTNAME"] = value
			self.dict_env["PROJECTPATH"] = temp + "/usr/" + value
		else:
			return
		
		'''获取数据库连接信息:
			DB数量key为"DB_NUM"
			DB1的key分别为"DB1_HOST"、"DB1_PORT"、"DB1_NAME"、"DB1_USER"和"DB1_PASSWD"和"DB1_TYPE"
			DB2的key分别为"DB1_HOST"、"DB2_PORT"、"DB2_NAME"、"DB2_USER"和"DB2_PASSWD"
		'''
		path = self.dict_env["PROJECTPATH"] + "/hdr/hdrpara.cfg"
		iniobj = IniCfg(path)
		_,_,value = iniobj.readvalue("dbconfig@@database1_type")
		if (not value is None) and value != "":
			self.dict_env["DB1_TYPE"] = value
			self.dict_env["DB1_HOST"] = iniobj.readvalue("dbconfig@@hd_db1_ip_1")
			self.dict_env["DB1_NAME"] = iniobj.readvalue("dbconfig@@hd_db1_name_1")
			self.dict_env["DB1_USER"] = iniobj.readvalue("dbconfig@@hd_db1_user")
			self.dict_env["DB1_PASSWD"] = iniobj.readvalue("dbconfig@@hd_db1_passwd")
			if value == "QMYSQL":
				self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1",3306)
			elif value == "QPSQL":
				self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1",5432)
			elif value == "QDMOCI":
				self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1",5236)
			else:
				pass
