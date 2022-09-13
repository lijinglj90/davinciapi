# coding:utf-8
import configparser
import os
import logger as lg
from splitcfg import SplitSymbol
import chardet

SPLITSTR = SplitSymbol.SYMBOL_BETWEEN_MODELLEVEL
class IniCfg():
    def __init__(self,cfgpath:str, encodingstr="utf-8"): 
        self.__cfgpath = cfgpath
        self.__splitstr = SPLITSTR

        self.__conf = configparser.ConfigParser()
        if not os.path.isfile(cfgpath):
            self.__hasfile = False
        else:
            self.__hasfile = True
            self.__conf.read(cfgpath, encodingstr)

        get_encoding = self.get_encoding(self.__cfgpath)
        print('能不能调用出来：', get_encoding)
        if encodingstr:  # 用户指定编码格式  encoding不为空
            self.__encoding = encodingstr  # 使用用户指定编码格式
        else:  # 用户没有指定编码格式
            if get_encoding:  # 程序自动获取文件编码格式，不为空
                self.__encoding = get_encoding  # 使用程序获取的编码格式
            else:
                self.__encoding = 'utf-8'  # 给一个默认值

    @staticmethod
    def get_encoding(cfgpath):
        # 二进制方式读取，获取字节数据，检测类型
        with open(cfgpath, 'rb') as f:
            data = f.read()
            return chardet.detect(data)['encoding']

    #读取ini，根据section名和key名读取值
    @staticmethod
    def readvalue_static(cfgpath:str,key:str, default = ""):
        stinfo = "readvalue_static调用，cfgpath:%s key:%s default:%s" %(cfgpath, key, default)
        lg.myloger.info(stinfo)

        if not os.path.isfile(cfgpath):
            info = ">> 无此文件，请核对路径[%s]" % cfgpath
            lg.myloger.error(info)
            return False,info,None

        temp_list = key.split(SPLITSTR,1)
        if len(temp_list) != 2 or temp_list[0] is None or temp_list[1] is None or temp_list[0] == "" or temp_list[1] == "":
            info = ">> 配置项参数错误，请核对[%s]" % key
            lg.myloger.error(info)
            return False,info,None


        get_encoding = IniCfg.get_encoding(cfgpath)
        if get_encoding:  # 程序自动获取文件编码格式，不为空
            encoding = get_encoding  # 使用程序获取的编码格式
        else:
            # encoding = 'utf-8'  # 给一个默认值
            info = '文件获取不到编码格式，请检查'
            return False, info, None

        cfgobj = configparser.ConfigParser()
        # cfgobj.read(cfgpath, encoding="utf-8")
        cfgobj.read(cfgpath, encoding=encoding)
        if cfgobj.has_option(temp_list[0],temp_list[1]):
            return True,"",cfgobj.get(temp_list[0],temp_list[1])
        else:
            info = ">> 配置项不存在返回缺省值，请核对[%s]" % key
            lg.myloger.info(info)
            return True,info,default


    #静态读取ini，根据section名和key名读取值
    @staticmethod
    def setvalue_static(cfgpath:str, key:str, value:str):
        stinfo = "setvalue_static调用，cfgpath:%s key:%s value:%s" %(cfgpath, key, value)
        lg.myloger.info(stinfo)

        if not os.path.isfile(cfgpath):
            info = ">> 无此文件，请核对路径[%s]" % cfgpath
            lg.myloger.error(info)
            return False,info
        
        temp_list = key.split(SPLITSTR,1)
        if len(temp_list) != 2 or temp_list[0] is None or temp_list[1] is None or temp_list[0] == "" or temp_list[1] == "":
            info = ">> 配置项参数错误，请核对[%s]" % key
            lg.myloger.error(info)
            return False,info


        get_encoding = IniCfg.get_encoding(cfgpath)
        if get_encoding:  # 程序自动获取文件编码格式，不为空
            encoding = get_encoding  # 使用程序获取的编码格式
        else:
            # encoding = 'utf-8'  # 给一个默认值
            info = '文件获取不到编码格式，请检查'
            return False, info, None

        cfgobj = configparser.ConfigParser()
        # cfgobj.read(cfgpath, encoding="utf-8")
        cfgobj.read(cfgpath, encoding=encoding)
        if not cfgobj.has_section(temp_list[0]):
            cfgobj.add_section(temp_list[0])

        cfgobj.set(temp_list[0], temp_list[1], value)
        cfgobj.write(open(cfgpath, "w")) 
        return True,""

    def readvalue(self, key:str, default = ""):
        stinfo = "readvalue调用，cfgpath:%s key:%s value:%s" %(self.__cfgpath, key, default)
        lg.myloger.info(stinfo)
        if not self.__hasfile:
            info = ">> 无此文件，请核对路径[%s]" % self.__cfgpath
            lg.myloger.error(info)
            return False,info,None
        
        temp_list = key.split(self.__splitstr,1)
        if len(temp_list) != 2 or temp_list[0] is None or temp_list[1] is None or temp_list[0] == "" or temp_list[1] == "":
            info = ">> 配置项参数错误，请核对[%s]" % key
            lg.myloger.error(info)
            return False,info,None
        
        if self.__conf.has_option(temp_list[0],temp_list[1]):
            return True, "", self.__conf.get(temp_list[0],temp_list[1])
        else:
            info = ">> 配置项不存在返回缺省值，请核对[%s]" % key
            lg.myloger.info(info)
            return False,info,default

    #读取ini，根据section名和key名读取值
    def setvalue(self, key:str, value:str):
        stinfo = "setvalue_static调用，cfgpath:%s key:%s value:%s" %(self.__cfgpath, key, value)
        lg.myloger.info(stinfo)
        
        if not self.__hasfile:
            info = ">> 无此文件，请核对路径[%s]" % self.__cfgpath
            lg.myloger.error(info)
            return False,info
        
        temp_list = key.split(self.__splitstr,1)
        if len(temp_list) != 2 or temp_list[0] is None or temp_list[1] is None or temp_list[0] == "" or temp_list[1] == "" != 2:
            info = ">> 配置项参数错误，请核对[%s]" % key
            lg.myloger.error(info)
            return False,info
        
        if not self.__conf.has_section(temp_list[0]):
            self.__conf.add_section(temp_list[0])

        self.__conf.set(temp_list[0], temp_list[1], value)
        return True,""

    #写入配置文件    
    def save(self):
        self.__conf.write(open(self.__cfgpath, "w", encoding=self.__encoding))
        # self.__conf.write(open(self.__cfgpath, "w"))
