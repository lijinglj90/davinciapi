from evnbase import EnvBase 
import os
from inicfg import IniCfg

class EnvFcst(EnvBase):
	''' 业务系统环境变量和基础参数配置接口基类'''
	
	def __init__(self):
		#重写父类构造
		# super(EnvFcst, self).__init__()
		super().__init__()
		self.dict_env = {}
		
		#获取DAVINCI环境变量
		temp = os.getenv('DAVINCI')
		print('@@@@@@',temp)
		if temp is None or temp == "":
			return
		
		self.dict_env["DAVINCI"] = temp

		
		#获取工程目录名和工程路径，key为"PROJECTNAME"和"PROJECTPATH"
		path = temp + "/etc/system.ini"

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
		path = self.dict_env["PROJECTPATH"] + "/hdr/hdrpara.ini"
		iniobj = IniCfg(path)
		_,_,value = iniobj.readvalue("dbconfig@@database1_type")
		if (not value is None) and value != "":
			self.dict_env["DB1_TYPE"] = value
			_,_,self.dict_env["DB1_HOST"] = iniobj.readvalue("dbconfig@@hd_db1_ip_1")
			_,_,self.dict_env["DB1_NAME"] = iniobj.readvalue("dbconfig@@hd_db1_name_1")
			_,_,self.dict_env["DB1_USER"] = iniobj.readvalue("dbconfig@@hd_db1_user")
			_,_,self.dict_env["DB1_PASSWD"] = iniobj.readvalue("dbconfig@@hd_db1_passwd")
			_,_,self.dict_env["DB1_DATABASE"] = iniobj.readvalue("dbconfig@@hd_db1_name_1")
			_,_,hd_db1_name_1 = iniobj.readvalue("dbconfig@@hd_db1_name_1")
			self.dict_env["DB1_DATABASE"] = hd_db1_name_1.split('@')[1]
			if value == "QMYSQL":  #mysql
				_,_,self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1","3306")
			elif value == "QPSQL":  #瀚高
				_,_,self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1","5432")
			elif value in ["QDSQL","QDMOCI"]:  #达梦
				_,_,self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1","5236")
			elif value in ["QKSQL","QKINGBASE"]:   #金仓
				_,_,self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1","54321")
			elif value == "QINSQL":   #influxdb
				_,_,self.dict_env["DB1_PORT"] = iniobj.readvalue("dbconfig@@hd_db1_PORT1","8086")
			else:
				pass
		print(self.dict_env)
