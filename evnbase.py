import os

class EnvBase:
	''' 业务系统环境变量和基础参数配置接口基类'''
	
	def __init__(self):
		#初始化配置参数字典，交由子类实现
		self.__dict_env={}

	def get_attr(self,keyword):
		'''参数获取接口
		通过传入关键词获取参数值
		
		Args：
			keyword：参数名，为英文字符串，如环境变量名等，由业务初始化
		
		Returns：
			一个字符串，如该关键字不存在，则返回空串
		
		'''
		
		if(keyword == ""):
			print("关键词为空")
			assert False
		
		return self.__dict_env.get(keyword,"")   #获取传入环境变量的参数值
	
	def setenv(self):
		print('@@@@@@@@@@@setenv方法的dict_env值',self.dict_env)
		# print('@@@@@@@@@@@__dict_env', self.__dict_env)
		for keyword,value in self.dict_env.items():
			mykey = "TEST_" + keyword
			os.environ[mykey] = value   #设置环境变量   其中key和value均为string类型
		os.environ["TEST_BASE"] = "/home/sprixin/autotest"  #设置环境变量

	def getenv(self,keyword):
		if (keyword == ""):
			print("关键词为空")
			assert False
		value = os.getenv(keyword)
		return value # 获取传入环境变量的参数值
