# coding:utf-8
'''
操作步骤执行接口：
- 类CmdType定义已实现的操作功能类型
- 类StepExecResult定义操作步骤返回通用格式
- 类StepObj实现各种功能接口调用
调用方法：
- 创建一个操作步骤对象
- 调用该对象的exec接口并获取返回值
'''
from rdbobj import RdbObj
from rtdbcfg import RtdbCfg
from webuicfg import WebCfg
from xmlcfg import XmlCfg
from csvcfg import CsvCfg
from jsoncfg import JsonCfg
from inicfg import IniCfg
import os
from enum import Enum
import basefunc as bs
from pandascfg import PandasCfg
from wpdcfg import WpdCfg
import copy
import shutil
import time

import sys
# from pluginmanager import PluginManager
# from pluginmanager import __ALLMODEL__

class CmdType():
    '''
    步骤类型编号定义
    -当增加步骤功能时，需在此注册获取指定的编号，该编号在整个框架中唯一
    '''
    # 配置操作类型
    set_para_ini = "1001"
    get_para_ini = "1002"
    set_para_csv = "1011"
    get_para_csv = "1012"
    set_para_json = "1021"
    get_para_json = "1022"
    set_para_xml = "1031"
    get_para_xml = "1032"
    set_para_pandas = '1041'
    get_para_pandas = '1042'
    set_para_wpd = "1051"
    get_para_wpd = "1052"


    #实时库操作类
    set_para_rtdb = "1101"
    get_para_rtdb = "1102"
    del_para_rtdb = "1103"


    #数据比较类型
    cmp_file_eq = "2001"
    cmp_data_eq = "2010"
    cmp_data_gr = "2011"
    cmp_data_ge = "2012"
    cmp_data_ne = "2013"
    cmp_data_ManyToOne = "2014"

    #执行命令类型
    exec_cmd = "3001"

    #web测试功能
    web_driver_create = "4001"
    web_driver_quet = "4002"
    web_element_action = "4003"

    #关系库操作
    rdb_read = "5001"
    rdb_write = "5002"

    #杂项操作类型
    file_exists = "9001"
    file_del = "9004"
    dir_file_del = "9005"
    isinfo_file = "9006"
    wait_to_time = "9002"
    wait_timespan = "9003"
    wait_sql = "9007"
    log_file = "9008"

    #在此增加新的函数定义

class StepExecResult():
    '''
    步骤执行结果结构体：
    :成员说明：
    -status 执行结果状态，执行成功为True，反之为False
    -errordesc 错误信息输出，当status为False时为错误信息，反之为空
    -returndatas 步骤返回数据列表。执行成功时有效，其具体内容有具体功能定义，如功能无返回信息则为None
    '''
    def __init__(self,status:bool,errordesc:str,returndatas:list) :
        self.status = status
        self.errordesc=errordesc
        self.returndatas=returndatas

class StepObj():
    '''
    步骤操作实现类：
    -汇聚所有步骤功能实现，通过exec调用具体的功能接口
    -增加功能时需在本类增加对应接口，相当于功能注册
    '''
    def __init__(self,cmdtype:str,paras:list) :
        self.__cmdtype = cmdtype    #功能类型
        self.__paras=paras      #参数列表

    '''INI文件访问接口'''
    from inicfg import IniCfg 
    def __get_para_ini__(self,paras:list):
        try:
            if len(paras) < 2:
                return StepExecResult(False,"参数个数错误",[])
            else:
                default = ""
                if len(paras) > 2:
                    default = paras[2]

                status,info,value = IniCfg.readvalue_static(paras[0],paras[1],default)

                ls = []
                if not status is None:
                    ls.append(value)
                print(ls, type(ls))

                return StepExecResult(status,info,ls)
        except Exception as e:
            return StepExecResult(False, e, [])

    def __set_para_ini__(self,paras:list):
        try:
            if len(paras) < 3:
                return StepExecResult(False,"参数个数错误",[])
            status,info= IniCfg.setvalue_static(paras[0],paras[1],paras[2])
            return StepExecResult(status, info, [])
        except Exception as e:
            return StepExecResult(False, e, [])


    
    '''json文件访问接口'''
    from jsoncfg import JsonCfg 
    def __get_para_json__(self,paras:list):
        if len(paras) < 4:
            return StepExecResult(False,"参数个数错误",[])
        else:
            try:
                default=""
                if len(paras) > 4:
                    default = paras[4]
                jc = JsonCfg(paras[0])
                status,info,value = jc.readvalue(paras[1],paras[2],paras[3],default)

                ls = []
                if not status is None:
                    ls.append(value)

                return StepExecResult(status,info,ls)
            except Exception as e:
                return StepExecResult(False, e, [])

    def __set_para_json__(self,paras:list):
        if len(paras) < 5:
            return StepExecResult(False,"参数个数错误",[])
        try:
            jc = JsonCfg(paras[0])
            status,info= jc.setvalue(paras[1],paras[2],paras[3],paras[4])
            if status is True:
                jc.save()

            return StepExecResult(status,info,[])
        except Exception as e:
            return StepExecResult(False, e, [])

    '''xml文件访问接口'''
    from xmlcfg import XmlCfg 
    def __get_para_xml__(self,paras:list):
        if len(paras) < 4:
            return StepExecResult(False,"参数个数错误",[])
        else:
            try:
                default=""
                if len(paras) > 4:
                    default = paras[4]
                xc = XmlCfg(paras[0])
                status,info,value = xc.readvalue(paras[1],paras[2],paras[3],default)

                ls = []
                if not status is None:
                    ls.append(value)
                print(status,info,value)
                print(ls,type(ls))
                return StepExecResult(status,info,ls)
            except Exception as e:
                return StepExecResult(False, e, [])

    def __set_para_xml__(self,paras:list):
        if len(paras) < 5:
            return StepExecResult(False,"参数个数错误",[])
        try:
            # xc = JsonCfg(paras[0])
            xc = XmlCfg(paras[0])
            status,info= xc.setvalue(paras[1],paras[2],paras[3],paras[4])
            if status is True:
                xc.save()
            print("__set_para_xml调用xc.setvalue返回:status,info", status,info)
            return StepExecResult(status,info,[])
        except Exception as e:
            print("__set_para_xml__",str(e))
            return StepExecResult(False, e, [])

    '''Csv文件访问接口'''
    from csvcfg import CsvCfg 
    def __get_para_csv__(self,paras:list):
        try:
            if len(paras) < 4 or len(paras) > 4:
                return StepExecResult(False,"参数个数错误",[])
            else:
                default=""
                if paras[3] not in ["", '']:
                    default = paras[3]
                cc = CsvCfg(paras[0])
                status, info, value = cc.readvalue(paras[1], paras[2], default)

                ls = []
                if not status is None:
                    ls.append(value)

                return StepExecResult(status,info,ls)
        except Exception as e:
            return StepExecResult(False, e, [])

    def __set_para_csv__(self,paras:list):
        print(paras)
        try:
            if len(paras) < 4 or len(paras) > 4:
                return StepExecResult(False,"参数个数错误",[])
            cc = CsvCfg(paras[0])
            status,info= cc.setvalue(paras[1],paras[2],paras[3])

            return StepExecResult(status,info,[])
        except Exception as e:
            return StepExecResult(False, e, [])

    '''文件访问接口,支持(txt、csv、excel(xls/xlsx/xlsm)、json、剪切板、数据库、html、hdf、parquet、pickled文件、sas、stata)'''
    #目前仅支持txt、csv、excel(xls/xlsx/xlsm)的读写，后期根据需要补充
    from pandascfg import PandasCfg
    def __get_para_pandas__(self, paras: list):
        print(paras,len(paras))
        if len(paras)<3:
            info = '传入参数个数不符合要求'
            return False,info,''
        elif len(paras)==3:
            paras.append('3')
            paras.append('')
        elif len(paras)==4:
            paras.append('')

        if '#*#' in paras[0]:
            dir,filename = os.path.split(paras[0])
            name = filename.split('#*#')[0]
            fuzzy_find_list = bs.fuzzy_find(dir, name)
            if len(fuzzy_find_list) == 1:
                pc = PandasCfg(fuzzy_find_list[0])
            else:
                info = f'模糊匹配到多个文件，请手动检，查询结果为：{fuzzy_find_list}'
                return StepExecResult(False, info, '')
        else:
            pc = PandasCfg(paras[0])

        status, info, value = pc.readvalue(fields=paras[1], fltstr=paras[2], return_type=paras[3], sheetname=paras[4])
        # print('@@@@@@',status, info, value)
        ls = []
        if not status is None:
            ls.append(value)
        return StepExecResult(status, info, ls)


    def __set_para_pandas__(self, paras: list):
        print(paras)
        if len(paras) < 5:
            return StepExecResult(False, "参数个数错误", [])
        cc = CsvCfg(paras[0], paras[1])
        status, info = cc.setvalue(paras[2], paras[3], paras[4])

        return StepExecResult(status, info, [])

    '''wpd文件访问接口'''
    from xmlcfg import XmlCfg
    def __get_para_wpd__(self, paras: list):
        if len(paras) < 3:
            return StepExecResult(False, "参数个数错误", [])
        else:
            try:
                wx = WpdCfg(paras[0])
                status, info, value = wx.readvalue_wpd(paras[1], paras[2])
                ls = []
                if not status is None:
                    ls.append(value)
                return StepExecResult(status, info, ls)
            except Exception as e:
                return StepExecResult(False, e, [])

    def __set_para_wpd__(self, paras: list):
        return StepExecResult(False, '待开发功能哦', [])
    
    '''实时库访问接口'''
    from rtdbcfg import RtdbCfg 
    def __get_para_rtdb__(self,paras:list):
        try:
            if len(paras) < 6:
                return StepExecResult(False,"参数个数错误",[])
            else:
                ip:str = paras[0]
                if len(ip) <= 0:
                    ip = "localhost"
                port:str = paras[1]
                if len(port) <= 0:
                    port = "8081"

                rc = RtdbCfg(ip,port)
                tableid = int(paras[2])
                print('__get_para_rtdb__:::', paras, tableid, paras[3], paras[4], paras[5])
                status,info,data = rc.readvalue(tableid,paras[3],paras[4],paras[5])
                if status:
                    ls = []
                    if len(data) > 1:
                        ls.append(data)
                    else:
                        ls = data
                    print('Ture:', 'status:', status, 'info:', info, 'data:', data, 'ls:', ls)
                    return StepExecResult(status, info, ls)
                else:
                    print('Flase:', 'status:', status, 'info:', info)
                    return StepExecResult(status, info, '')
        except Exception as e:
            return StepExecResult(False, e, '')

    def __set_para_rtdb__(self,paras:list):
        if len(paras) < 7:
            return StepExecResult(False, "参数个数错误", [])
        else:
            ip: str = paras[0]
            if len(ip) <= 0:
                ip = "localhost"
            port: str = paras[1]
            if len(port) <= 0:
                port = "8081"

            rc = RtdbCfg(ip, port)
            tableid = int(paras[2])
            print('__set_para_rtdb__:::',paras, tableid, paras[3], paras[4], paras[5], paras[6])
            status, info = rc.setvalue(tableid, paras[3], paras[4], paras[5], paras[6])

        return StepExecResult(status, info, [])

    def __del_para_rtdb__(self,paras:list):
        if len(paras) != 4:
            return StepExecResult(False, "参数个数错误", [])
        else:
            ip: str = paras[0]
            if len(ip) <= 0:
                ip = "localhost"
            port: str = paras[1]
            if len(port) <= 0:
                port = "8081"

            rc = RtdbCfg(ip, port)
            tableid = int(paras[2])

            print('__del_para_rtdb__:::',paras, tableid, paras[3])
            status, info = rc.delvalue(tableid, paras[3])

        return StepExecResult(status, info, [])


    '''数据比较接口'''
    def __cmp_data_eq__(self,paras:list):
        # print('输入的对比数据为：',paras)
        if len(paras) < 3:
            return StepExecResult(False,"参数个数错误",[])
        can2 = copy.deepcopy(paras[2])
        status = bs.cmp_eq(paras[0],paras[1],paras[2])
        info = ""
        if status is False:
            info = "判==失败：参数1为[%s],参数2为[%s]" %(paras[1],can2)
        
        return StepExecResult(status,info,[])

    def __cmp_data_gr__(self,paras:list):
        if len(paras) < 3:
            return StepExecResult(False,"参数个数错误",[])
        status = bs.cmp_gr(paras[0],paras[1],paras[2])
        
        info = ""
        if status is False:
            info = "判>失败：参数1为[%s],参数2为[%s]" %(paras[1],paras[2])
        
        return StepExecResult(status,info,[])

    def __cmp_data_ge__(self,paras:list):
        if len(paras) < 3:
            return StepExecResult(False,"参数个数错误",[])
        status = bs.cmp_ge(paras[0],paras[1],paras[2])
        
        info = ""
        if status is False:
            info = "判>=失败：参数1为[%s],参数2为[%s]" %(paras[1],paras[2])
        
        return StepExecResult(status,info,[])

    def __cmp_data_ne__(self,paras:list):
        if len(paras) < 3:
            return StepExecResult(False,"参数个数错误",[])
        status = bs.cmp_ne(paras[0],paras[1],paras[2])
        
        info = ""
        if status is False:
            info = "判!=失败：参数1为[%s],参数2为[%s]" %(paras[1],paras[2])
        
        return StepExecResult(status,info,[])

    def __cmp_data_ManyToOne__(self, paras: list):
        # print('输入的对比数据为：',paras)
        if len(paras) < 3:
            return StepExecResult(False, "参数个数错误", [])
        can2 = copy.deepcopy(paras[2])
        status = bs.cmp_eq_ManyToOne(paras[0], paras[1], paras[2])
        info = ""
        if status is False:
            info = "判==失败：参数1为[%s],参数2为[%s]" % (paras[1], can2)

        return StepExecResult(status, info, [])

    def __cmp_file_eq__(self,paras:list):
        try:
            if len(paras) < 2:
                return StepExecResult(False,"参数个数错误",[])
            elif len(paras) == 2:
                l = ['', '', '']
                paras.extend(l)
            elif len(paras) == 3:
                l = ['', '']
                paras.extend(l)
            elif len(paras) == 4:
                paras.append('')
            status,info = bs.cmp_file(paras[0],paras[1],paras[2],paras[3],paras[4])

            return StepExecResult(status,info,[])
        except Exception as e:
            info = str(e)
            return StepExecResult(False, info, [])

    '''执行命令接口'''
    def __exec_cmd__(self,paras:list):
        print('输入的命令为：',paras)
        try:
            if len(paras) < 1:
                return StepExecResult(False,"参数个数错误",[])
            status,info = bs.runcmd(paras[0])

            return StepExecResult(status,info,[])
        except Exception as e:
            return StepExecResult(False, e, [])

    '''等待接口：等待到指定时刻'''
    def __wait_to_time__(self,paras:list):
        try:
            para_count = len(paras)
            if para_count < 1:
                return StepExecResult(False,"参数个数错误",[])
            elif para_count == 1:
                bs.waitto(paras[0])
            else:
                if paras[1] == "True":
                    bs.waitto(paras[0], True)
                else:
                    bs.waitto(paras[0])
            return StepExecResult(True,"",[])
        except Exception as e:
            return StepExecResult(False, e, [])

    '''等待接口：等待指定时间长度'''
    def __wait_timespan__(self,paras:list):
        try:
            para_count = len(paras)
            if para_count < 1:
                return StepExecResult(False,"参数个数错误",[])
            else:
                bs.waitspan(paras[0])

            return StepExecResult(True,"",[])
        except Exception as e:
            info = '检查输入的参数是否是数字,报错信息：'+ str(e)
            return StepExecResult(False, info, [])

    '''等待接口：等待指定sql语句获取到数据'''
    def __wait_sql__(self,paras:list):
        obj = None
        print("__wait_sql__输入参数", paras)
        print(len(paras))
        try:
            if len(paras) == 4:
                if paras[2] in ['_', '']:
                    obj = RdbObj(paras[1])
                else:
                    obj = RdbObj(paras[1], paras[2])
                if paras[3] == '' or paras[3] == '_':
                    paras[3] = 3
                status, info, data = obj.exec_querry(paras[0], paras[3])
            # print(status, 'info:',info, 'data:', data)
            else:
                return StepExecResult(False, "参数个数错误", [])

            if status:
                t = 0
                while not data:
                    time.sleep(15)
                    t += 15
                    print(f'已经等待{t}秒，最长等待时间7200秒，目前没有数据再等一会')
                    # print(Vnum)
                    status1, info1, data1 = obj.exec_querry(paras[0], paras[3])
                    if data1:
                        # print(data1)
                        time.sleep(2)
                        break
                    if t >= 7200:
                        break
                return StepExecResult(True, "", [])
            else:
                return StepExecResult(status, info, data)
        except Exception as e:
            info = str(e)
            return StepExecResult(False, info, [])

    '''文件存在检查接口'''
    def __file_exixts__(self,paras:list):
        try:
            # print('stepobj::',paras)
            para_count = len(paras)
            if para_count < 1 or para_count > 2:
                return StepExecResult(False,"参数个数错误",[])
            elif para_count == 1:
                paras.append('')

            status = bs.hasfile(paras[0],paras[1])
            print(status)
            if status:
                return StepExecResult(status,"",[])
            else:
                info = '请检查文件路径' + str(paras[0])
                return StepExecResult(status, info, [])
        except Exception as e:
            info = '请检查文件路径' + str(e)
            return StepExecResult(False, info, [])

    '''文件删除接口'''
    def __file_del__(self,paras:list):
        try:
            # print('stepobj::',paras)
            para_count = len(paras)
            if para_count < 1:
                return StepExecResult(False,"参数个数错误",[])
            elif para_count == 1:
                paras.append('')

            status = bs.hasfile(paras[0], paras[1])
            # print(status)

            if paras[1] not in ['']:
                paras[0] = paras[0].encode(encoding=paras[1])


            if status:
                try:
                    os.remove(paras[0])
                    print('文件存在，且被删除')
                except Exception as e:
                    # print('删除文件异常')
                    info = '删除文件异常，在linux环境下不能删除root用户创建的文件'
                    return StepExecResult(False, info, [])
            else:
                print('文件不存在，不需要操作')

            return StepExecResult(True,"",[])

        except Exception as e:
            return StepExecResult(False, e, [])

    '''保留文件夹文仅清空文件夹'''
    def __dir_file_del__(self, paras: list):
        try:
            para_count = len(paras)
            if para_count < 1:
                return StepExecResult(False, "参数个数错误", [])
            status1 = os.path.isdir(paras[0])   #判断paras[0]是否是个文件夹
            status2 = os.path.exists(paras[0])  #判断paras[0]是否存在
            if status1:
                if status2:
                    try:
                        shutil.rmtree(paras[0])   #递归删除整个文件夹下所有文件，包括此文件夹
                        os.makedirs(paras[0])   #path不存在的情况下，在该path下递归创建新文件夹
                        print('删除完毕')
                    except Exception as e:
                        print(e)
                        return StepExecResult(False, e, [])
                else:
                    print('文件夹不存在，不需要操作')

                return StepExecResult(True, "", [])
            else:
                return StepExecResult(False, '输入的地址不是一个文件夹路径，请检查', [])
        except Exception as e:
            return StepExecResult(False, e, [])

    '''日志文件结果返回'''
    def __isinfo_file__(self, paras: list):
        print("__log_file__输入参数", paras)
        print(len(paras))
        try:
            if len(paras) in [3, 4]:
                status1 = os.path.exists(paras[0])
                if paras[1] in ['', '_']:
                    print('请传入需要检索的关键字')
                    return StepExecResult(False, "请传入需要检索的关键字", [])
                elif paras[2] in ['', '_']:
                    print('匹配类型未传入默认为：1')
                    return StepExecResult(False, "请传入匹配类型1", [])
                elif len(paras) == 3:  #右侧数据为1，左侧数据为2，整行数据为3
                    paras.append('')
                if status1:
                    status, info, data = bs.isinfofile(paras[0], paras[1], paras[2],paras[3])
                    print(status, 'info:', info, 'data:', data)
                    ls = []
                    ls.append(data)
                    return StepExecResult(status, info, ls)
                else:
                    print('文件不存在，请检查')
                    return StepExecResult(False, "文件不存在，请检查", [])
            else:
                print('参数个数错误')
                return StepExecResult(False, "参数个数错误", [])
        except Exception as e:
            info = str(e)
            print('info:', info)
            return StepExecResult(False, info, [])

    from webuicfg import WebCfg
    def __web_driver_quit__(self,paras:list):
        try:
            para_count = len(paras)
            if para_count < 1:
                return StepExecResult(False,"参数个数错误",[])
            wc = WebCfg()
            status,info,data = wc.quitdriver(paras[0])

            return StepExecResult(status,info,[])

        except Exception as e:
            info = '关闭驱动失败'
            return StepExecResult(False, info, [])
    
    from webuicfg import WebCfg
    def __web_element_action__(self,paras:list):
        try:
            para_count = len(paras)
            driver = None
            driver_type = "chrome"
            if para_count < 3:
                return StepExecResult(False,"参数个数错误",[])
            if para_count > 3:
                driver = paras[3]
            if para_count > 4:
                driver_type = paras[4]

            ls = []
            wc = WebCfg()
            status,info,data = wc.element_action(paras[0],paras[1],paras[2],driver,driver_type)

            ls.append(data)
            return StepExecResult(status,info,ls)
        except Exception as e:
            info = str(e).split('\n')[0]  + '，请检查测试链接及操作步骤'
            return StepExecResult(False, info, [])

    def __web_driver_create__(self,paras:list):   #创建驱动
        try:
            para_count = len(paras)
            driver_type = "chrome"
            if para_count > 0:
                driver_type = paras[0]
            wc = WebCfg()
            status,info,driver = wc.createdriver(driver_type)   #创建一个浏览器驱动，并最大化窗口
            ls = []
            ls.append(driver)
            return StepExecResult(status,info,ls)
        except Exception as e:
            info = '目前仅支持Chrome驱动,报错信息：'+str(e)
            return StepExecResult(False, info, [])

    def __rdb_querry__(self, paras: list):
        obj = None
        print("__rdb_querry__输入参数",paras)
        print(len(paras))
        try:
            if len(paras) == 4:
                if paras[2] in ['_', '']:
                    obj = RdbObj(paras[1])
                else:
                    obj = RdbObj(paras[1], paras[2])
                if paras[3] == '' or paras[3] == '_':
                    paras[3] = 3
                status, info, data = obj.exec_querry(paras[0], paras[3])
            # print(status, 'info:',info, 'data:', data)
            elif len(paras) > 0 and len(paras) < 4 and paras[0] != '':
                if len(paras) == 1:
                    obj = RdbObj()
                elif len(paras) == 2:
                    obj = RdbObj(paras[1])
                elif len(paras) == 3:
                    if paras[2] in ['_', '']:
                        obj = RdbObj(paras[1])
                    else:
                        obj = RdbObj(paras[1],paras[2])
                status, info, data = obj.exec_querry(paras[0])
            else:
                return StepExecResult(False, "参数个数错误", [])
        except Exception as e:
            info = str(e)
            return StepExecResult(False, info, [])

        ls = []
        ls.append(data)
        # print(data)
        # print('ls:',ls)
        return StepExecResult(status, info,ls)

    def __rdb_excute__(self, paras: list):
        try:
            obj = None
            if len(paras) < 1:
                return StepExecResult(False, "参数个数错误", [])
            elif len(paras) == 1:
                obj = RdbObj()
            elif len(paras) == 2:
                obj = RdbObj(paras[1])
            else:
                if paras[2] == '_':
                    obj = RdbObj(paras[1])
                else:
                    obj = RdbObj(paras[1], paras[2])

            status, info, _ = obj.exec_sql(paras[0])

            return StepExecResult(status, info, [])

        except Exception as e:
            return StepExecResult(False, e, [])

    def myexec(self):
        '''单条测试用例步骤执行接口'''
        #当增加函数时在此增加调用操作

        if self.__cmdtype == CmdType.get_para_ini:
            return self.__get_para_ini__(self.__paras)
        elif self.__cmdtype == CmdType.set_para_ini:
            return self.__set_para_ini__(self.__paras)
        elif self.__cmdtype == CmdType.get_para_json:
            return self.__get_para_json__(self.__paras) 
        elif self.__cmdtype == CmdType.set_para_json:
            return self.__set_para_json__(self.__paras)
        elif self.__cmdtype == CmdType.get_para_csv:
            return self.__get_para_csv__(self.__paras) 
        elif self.__cmdtype == CmdType.set_para_csv:
            return self.__set_para_csv__(self.__paras)
        elif self.__cmdtype == CmdType.get_para_xml:
            return self.__get_para_xml__(self.__paras) 
        elif self.__cmdtype == CmdType.set_para_xml:
            return self.__set_para_xml__(self.__paras)
        elif self.__cmdtype == CmdType.set_para_rtdb:   #1011
            return self.__set_para_rtdb__(self.__paras)
        elif self.__cmdtype == CmdType.get_para_rtdb:   #1012
            return self.__get_para_rtdb__(self.__paras)
        elif self.__cmdtype == CmdType.del_para_rtdb:   #1103
            return self.__del_para_rtdb__(self.__paras)
        elif self.__cmdtype == CmdType.get_para_pandas:
            return self.__get_para_pandas__(self.__paras)
        elif self.__cmdtype == CmdType.set_para_pandas:   #1041
            return self.__set_para_pandas__(self.__paras)
        elif self.__cmdtype == CmdType.get_para_wpd:
            return self.__get_para_wpd__(self.__paras)
        elif self.__cmdtype == CmdType.set_para_wpd:
            return self.__set_para_wpd__(self.__paras)
        elif self.__cmdtype == CmdType.cmp_data_eq:
            return self.__cmp_data_eq__(self.__paras)
        elif self.__cmdtype == CmdType.cmp_data_ge:
            return self.__cmp_data_ge__(self.__paras) 
        elif self.__cmdtype == CmdType.cmp_file_eq:
            return self.__cmp_file_eq__(self.__paras)
        elif self.__cmdtype == CmdType.cmp_data_gr:
            return self.__cmp_data_gr__(self.__paras) 
        elif self.__cmdtype == CmdType.cmp_data_ne:
            return self.__cmp_data_ne__(self.__paras)
        elif self.__cmdtype == CmdType.cmp_data_ManyToOne:
            return self.__cmp_data_ManyToOne__(self.__paras)
        elif self.__cmdtype == CmdType.file_exists:    #9001
            return self.__file_exixts__(self.__paras)
        elif self.__cmdtype == CmdType.file_del:    #9004
            return self.__file_del__(self.__paras)
        elif self.__cmdtype == CmdType.dir_file_del:    #9005
            return self.__dir_file_del__(self.__paras)
        elif self.__cmdtype == CmdType.isinfo_file:    #9006
            return self.__isinfo_file__(self.__paras)
        elif self.__cmdtype == CmdType.wait_to_time:
            return self.__wait_to_time__(self.__paras)
        elif self.__cmdtype == CmdType.wait_timespan:
            return self.__wait_timespan__(self.__paras)
        elif self.__cmdtype == CmdType.wait_sql:    #9007
            return self.__wait_sql__(self.__paras)
        elif self.__cmdtype == CmdType.exec_cmd:
            return self.__exec_cmd__(self.__paras)
        elif self.__cmdtype == CmdType.web_driver_create:  # "4001"
            return self.__web_driver_create__(self.__paras)
        elif self.__cmdtype == CmdType.web_driver_quet:  # "4002"
            return self.__web_driver_quit__(self.__paras)
        elif self.__cmdtype == CmdType.web_element_action:   #4003
            return self.__web_element_action__(self.__paras)
        elif self.__cmdtype == CmdType.rdb_read:
            return self.__rdb_querry__(self.__paras)
        elif self.__cmdtype == CmdType.rdb_write:
            return self.__rdb_excute__(self.__paras)
        # else:
        #     PluginManager.LoadAllPlugin();
        #     #遍历所有接入点下的所有插件
        #     bFound = False
        #     for SingleModel in __ALLMODEL__:
        #         plugins = SingleModel.GetPluginObject()
        #         for item in plugins:
        #             if item.get_type() == "Model_StepFunction":
        #                 if item.getid() == self.__cmdtype:
        #                     bFound = True
        #                     return item.exec_func(self.__paras)
        #     if bFound:
        #         return StepExecResult(False,"命令类型不支持",[])

if __name__ == '__main__':
    cmdtype="2001"
    paras = [r'D:\davinciapi\case\zz\对比后删除A\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\case\zz\对比后删除B\farm1_20220816_0000_DQ.wpd','gb2312']
    StepObj(cmdtype,paras).__cmp_file_eq__(paras)
    import filecmp
    # print(filecmp.cmp(paras[0], paras[1]))
    # cmdtype = 5001
    # # a = ["SELECT LONGITUDE,RUNTIME from wind_turbine where ALIASNAME = '风机_1'~QMYSQL~10.8.8.22@3306@DAVINCI@sa@cast1234~3]
    # a = ["SELECT LONGITUDE,RUNTIME from wind_turbine where ALIASNAME = '风机_1'","QMYSQL","10.8.8.22@3306@DAVINCI@sa@cast1234","3"]
    # StepObj(cmdtype,a).__rdb_querry__(a)
    # print(b)

    # cmdtype = 9006
    # a = [r'D:\davinciapi\wen\a - 副本\rxefilecreate.log','[U-17]','_']
    # StepObj(cmdtype,a).__isinfo_file__(a)

    # cmdtype = 3001
    # a = ['dir']
    # StepObj(cmdtype, a).__exec_cmd__(a)
