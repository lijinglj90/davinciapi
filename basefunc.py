# coding:utf-8
'''常用命令实现
'''

import re
import subprocess
#from typing_extensions import TypeVarTuple
import logger as lg
import os
import time
import datetime
import filecmp
import math
import copy
import platform
import chardet
from splitcfg import SplitSymbol


def runcmd(command):
    '''执行命令功能
    :输入参数：
    - command 命令脚本

    :输出参数：
    - status 命令执行状态，正确执行为True，反之为False
    - info   如果过程执行异常信息
    - result 命令执行标准输出
    '''
    plat = platform.system().lower()
    if plat == 'windows':
        print('现在使用的是windows系统')
        encodstr = "gbk"
    elif plat == 'linux':
        print('现在使用的是linux系统')
        encodstr = "utf-8"

    ret = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding=encodstr,timeout=600)
    if ret.returncode == 0:
        print(ret.stdout)
        return True, "" #,ret.stdout
    else:
        info = "执行脚本[%s]返回错误，错误信息:[%s]" %(command,ret.stderr)
        lg.myloger.error(info)
        return False, ret.stderr #,None

def hasfile(filepath,encodestr=''):
    '''检查文件是否存在功能
    :输入参数:
    - filepath 文件路径，请传入文件绝对路径

    :输出参数:
    - result  文件存在则为True，反之为False
    '''
    if encodestr not in ['']:
        filepath = filepath.encode(encoding=encodestr)
    print('filepath::', filepath, encodestr)
    return os.path.exists(filepath)

'''等待功能'''
def waitto(stime:str,bnextday:bool = False):
    '''等待到指定时刻
    :输入参数:
    - stime，指定时刻，格式为"%H:%M:%S"的字符串
    - bnextday，是否强制下一天,缺省为False

    :输出参数:
    - 无

    :说明：
        如果bnextday为True，则等到下一天指定时刻，反之
        stime在当前时间之后，则等待到stime时刻，如果在之前，则等到下一天的stime时刻
    '''
    tar_time = time.strptime(stime,"%H:%M:%S")
    tar_seconds = tar_time.tm_hour * 3600 + tar_time.tm_min * 60 + tar_time.tm_sec + 86400
    # now_time = datetime.datetime.now()
    now_time1 = datetime.datetime.now().strftime("%H:%M:%S")
    now_time = time.strptime(now_time1, "%H:%M:%S")
    now_seconds = now_time.tm_hour * 3600 + now_time.tm_min * 60 + now_time.tm_sec
    
    wait_span = tar_seconds - now_seconds
    if bnextday is False:
        wait_span %= 86400
    print('wait_span:',wait_span)
    time.sleep(wait_span)

def waitspan(seconds:str):
    '''等待指定长的时间
    :输入参数:
    - seconds 等待时长，单位为秒

    :输出参数:
    - 无
    '''
    timespan = int(seconds)
    if timespan > 0:
        time.sleep(timespan)
    else:
        lg.myloger.error("等待时间小于0")

def cmp_file(file1:str,file2:str,encodestr='',Leftn='',rightn=''):
    '''检查文件是否一致，如果不一致则返回差异信息
    :输入参数：
    - file1 文件1
    - file2 文件2

    :输出参数：
    - status 比较过程信息，过程执行正确为True，执行异常则为False
    - info   如果过程执行异常信息
    - result 如果一致则返回True，否则返回False
    '''
    '处理文件名称包含的特殊字符'
    if encodestr not in ['']:
        file1 = file1.encode(encoding=encodestr)
        file2 = file2.encode(encoding=encodestr)
    else:
        encodestr = get_encoding(file1)
    # print('cmp_file:',file1,file2,encodestr,Leftn,rightn)

    '检查文件是否存在'
    file_exist = os.path.exists(file1)
    if file_exist is False:
        info = "文件[%s]不存在" % file1
        lg.myloger.error(info)
        return False, info

    file_exist = os.path.exists(file2)
    if file_exist is False:
        info = "文件[%s]不存在" % file2
        lg.myloger.error(info)
        return False, info

    '检查文件名是否一致'
    _,filename1=os.path.split(file1)
    _,filename2=os.path.split(file2)
    if filename1 != filename2:
        info = "传入文件[%s,%s]文件名不一致" % (file1,file2)
        lg.myloger.error(info)
        return False, info

    '检查内容是否一致'
    if not Leftn and not rightn:  #两个值均为空
        # print('两个值均为空,对应的文件编码',encodestr)
        status = filecmp.cmp(file1, file2)
    else:   #有一个为空，或者均不为空

        '检查传入参数是否正确'
        try:
            if Leftn:
                Leftn = eval(Leftn)
            if rightn:
                rightn = eval(rightn)
        except Exception as e:
            info = '输入的行号有误，报错信息:' + str(e)
            return False, info
        # print('有一个为空，或者均不为空,对应的文件编码',encodestr,'Leftn:',Leftn, 'rightn:',rightn)
        status = cmp_part(file1, file2,encodestr,Leftn,rightn)

    if status:
        return status, ""
    else:
        info = "传入文件[%s],与文件[%s]内容不一致,比对失败，请检查" % (file1,file2)
        lg.myloger.error(info)
        return status, info

def cmp_part(file1:str,file2:str,encodestr,Leftn,rightn):
    status = True
    with open(file1, 'r', encoding=encodestr) as f1, open(file2, 'r', encoding=encodestr) as f2:
        line1 = f1.readlines()
        line2 = f2.readlines()
        # print(len(line1))
        if not Leftn:
            Leftn = 1
        elif not rightn:
            rightn = len(line1)
        elif len(line1) != len(line2) or len(line1)<1:   #pass
            info = '两个文件大小不一样，或者文件为空'
            lg.myloger.error(info)
            status = False
            return status
        elif Leftn>len(line1):
            info = '起始行号超出文件最大行数'
            lg.myloger.error(info)
            return False
        elif rightn:
            if rightn >= len(line1) or rightn<=Leftn or rightn < 1:
                info = '结束行号超出文件最大行数、不正确、小于起始行号'
                lg.myloger.error(info)
                status = False
                return status
        stinfo = '用户传入的文件[%s]和文件[%s]，编码格式[%s],起始行号[%s]，结束行号[%s]' %(file1,file2,encodestr,Leftn,rightn)
        lg.myloger.info(stinfo)
        for i in range(0, len(line1)):
            if i >= Leftn - 1 and i <= rightn - 1:
                b1 = line1[i]
                b2 = line2[i]
                # print(b1)
                # print(b2)
                if b1 != b2:
                    status = False
                    return status
    return status


def isinfofile(file, keywords,type='1',CheckType='',separate='',return_type='3',encodingstr=''):
    '''
        :输入参数：\n
        - file     文件目录地址
        - keywords 检索目标值  case1：“检索目标值”  case2:“检索目标值A@检索目标值B”
        - type  匹配类型  默认1：包含匹配，其他待开发
        - CheckType 返回数据规则 默认3：返回整行数据。当keywords为case2的时候建议输入1：返回目标值A和目标值B中间的数据
        - separate  目标值A和目标值B之间的数据分隔符  --可以不传
        - return_type  返回数据类型，默认3列表格式   --可以不传
        - encodingstr 文件编码格式 --可以不传

        :输出参数：
        - status 读取状态，读取成功为True，读取失败为False
        - info   备注信息
        - data   表格数据信息， 失败为None，成功为一个列表
    '''
    #默认utf-8编码格式打开，后期有需要再扩展
    stinfo = "isinfofile调用，file路径:%s keywords检索目标值:%s type 匹配类型:%s CheckType返回数据匹配规则:%s" % (file, keywords, type, CheckType)
    # print(stinfo)
    lg.myloger.info(stinfo)
    plat = platform.system().lower()
    if encodingstr in ['','_']:
        encodstr = get_encoding(file)
        print("当前使用的系统环境是：",plat,"当前文本的编码格式是：",encodstr)
    else:
        encodstr = encodingstr
    n = 0
    data = []
    CheckedDataList= []
    key= keywords.split(SplitSymbol.SYMBOL_BETWEEN_ELEMENTS_IN_CONDITION)  # ‘@’分割
    if key in ['','_']:
        return False, '需要检索的关键字为空，请检查', ''
    elif len(key) != 2 and CheckType in [1,'1']:
        return False, '需要检索的关键字为两个，格式为：A@B', ''
    if separate in ['','_']:
        separate = ', '
    with open(file, "r", encoding=encodstr) as f:
        files = f.readlines()
    for file in files:
        if type == '1':
            if key[0] in file:
                # print('file:',file)
                CheckedDataList.append(file)
                n += 1
        else:
            return False, '不支持的校验类型', ''
    if CheckType:
        data,n = isinfofile_fuzzy(CheckType,CheckedDataList,key,separate)
    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@',data, n)
    if n == 1:
        return True, '检索数据存在，且唯一', data
    elif n > 1:
        return True, f'检索数据存在，一共匹配到{n}个,返回最后一条匹配的数据', data
    else:
        return False, '遍历全部文件内容，没有匹配到对应文案', ''

def isinfofile_fuzzy(CheckType,CheckedDataList,key,separate):
    if CheckType in [1,'1']:   ##取两个被检索值中间的数据
        # CheckedD = re.findall('(?<='+keywords+').*$', CheckedData)[0].split(separate)

        CheckedD = []
        data = []
        n = 0
        # CheckedData = CheckedDataList[-1]
        # CheckedD = CheckedData[CheckedData.rfind(key[0])+len(key[0]):CheckedData.rfind(key[1])].split(separate)
        # print('hhhhh', CheckedD, len(CheckedD))
        for CheckedData in CheckedDataList:
            leftnum = CheckedData.rfind(key[0])+len(key[0])
            rightnum = CheckedData.rfind(key[1])
            if leftnum>=0 and rightnum>=0:
                CheckedD = CheckedData[leftnum:rightnum].split(separate)
                n +=1
                # print('hhhhh', CheckedD, len(CheckedD),n)
        if len(CheckedD) == 0:
            return data, 0
        elif len(CheckedD) == 1:
            data = CheckedD
        else:
            for i in CheckedD:
                z = []
                if i in ['']:
                    continue
                z.append(i)
                data.append(z)
        # print("aaaaaaaaaaaaaaaaaaaaaaaaaaaa",data,n)
        return data, n
    elif CheckType in [2,'2']:  ##2、 被检索值右侧的数据，默认返回列表格式      ##暂未实现，后期补充
        pass
    elif CheckType in [3,'3']:   ##3、 被检索值左侧的数据，默认返回列表格式      ##暂未实现，后期补充
        pass
    elif CheckType in [4,'4']:   ##4、 被检索值整行的数据，默认返回列表格式      ##暂未实现，后期补充
        pass

def cmp_eq(type:str,v1:str, v2:str):
    '''相等比较判断函数
    :输入参数：
    - type 数据类型，1为整数，2为浮点数，....
    - v1 为待比较的数据，均为字符串格式
    - v2 同v1

    :输出参数：
    - status 如果相等返回True，反之返回False
    '''

    try:
        if type == "1": #整数
            if v1.isdigit() and v2.isdigit():
                value1 = int(v1)
                value2 = int(v2)
                if value1 == value2:
                    return True
                else:
                    return False
            else:
                return False

        elif type == "2": #浮点数
            value1 = float(v1)
            value2 = float(v2)
            if math.fabs(value1 - value2) < 0.006 :
                return True
            else:
                return False

        elif type == "3":  # list
            try:
                if isinstance(v1, str):
                    v1 = eval(v1)
                if isinstance(v2, str):
                    v2 = eval(v2)
            except Exception as e:
                return False
            # print('v1:',v1,'v2:',v2)
            i = 0
            j = 0
            if len(v1) == len(v2):
                while i < len(v1):
                    while j < len(v2):
                        if v1[i] == v2[j]:
                            v2.remove(v2[j])
                            break
                        elif isinstance(v1[i], list) and isinstance(v2[j], list) :
                            newv2 = []
                            newv2 = str(v2[j])  #直接赋值，后期v2内数据删除后newv2内数据也会被删除
                            if cmp_eq('3',v1[i],v2[j]):
                                if v2[j] == []:
                                    v2.remove(v2[j])
                                break
                            else:
                                v2[j] = eval(newv2)
                        else:
                            try:
                                newi = float(v1[i])
                                newj = float(v2[j])
                                if math.isclose(newi, newj, abs_tol=0.006):
                                    v2.remove(v2[j])
                                    break
                                else:
                                    pass
                            except:
                                pass
                        j += 1
                    i += 1
                    j = 0
            else:
                info = "两个列表的长度不一样，预期：%s,实际:%s" % (v1, v2)
                return False
            if len(v2) > 0:
                info = "两个列表的值不一致，预期：%s,实际:%s" % (v1, v2)
                return False
            else:
                return True

        elif type == "4": #str
            if v1 == v2:
                return True
            else:
                return False
    except ValueError:
        return False
    
def cmp_gr(type:str,v1:str, v2:str):
    '''大于比较判断函数
    :输入参数：
    - type 数据类型，1为整数，2为浮点数，....
    - v1 为待比较的数据，均为字符串格式
    - v2 同v1

    :输出参数：
    - status 如果v1>v2返回True，反之返回False
    '''
    try:
        if type == "1": #整数
            value1 = int(v1)
            value2 = int(v2)
            if value1 > value2:
                return True
            else:
                return False
        elif type == "2": #浮点数
            value1 = float(v1)
            value2 = float(v2)
            if value1 - value2 > 0.0001 :
                return True
            else:
                return False
        else:
            return False
    except ValueError:
        return False

def cmp_ge(type:str,v1:str, v2:str):
    '''大于等于比较判断函数
    :输入参数：
    - type 数据类型，1为整数，2为浮点数，....
    - v1 为待比较的数据，均为字符串格式
    - v2 同v1

    :输出参数：
    - status 如果v1大于等于v2返回True，反之返回False

    '''
    try:
        if type == "1": #整数
            value1 = int(v1)
            value2 = int(v2)
            if value1 >= value2:
                return True
            else:
                return False
        elif type == "2": #浮点数
            value1 = float(v1)
            value2 = float(v2)
            if value1 - value2 > 0.0001 or math.fabs(value1 - value2) < 0.0001:
                return True
            else:
                return False
        else:
            return False
    except ValueError:
        return False

def cmp_ne(type:str,v1:str, v2:str):
    '''不等于比较判断函数
    :输入参数：
    - type 数据类型，1为整数，2为浮点数，....
    - v1 为待比较的数据，均为字符串格式
    - v2 同v1

    :输出参数：
    - status 如果v1不等于v2返回True，反之返回False
    '''
    ret = cmp_eq(type,v1,v2)
    if ret is True:
        return False
    else:
        return True

def cmp_eq_ManyToOne(type:str,v1:str, v2:str):
    '''相等比较判断函数
    :输入参数：
    - type 数据类型，1为整数，2为浮点数，....
    - v1 为待比较的数据，均为字符串格式
    - v2 同v1

    :输出参数：
    - status 如果相等返回True，反之返回False
    '''
    print('type:',type, 'v1:', v1, 'v2:', v2)
    try:
        if type == "1": #整数
            if v1.isdigit() and v2.isdigit():
                value1 = int(v1)
                value2 = int(v2)
                pass

        elif type == "2": #浮点数
            value1 = float(v1)
            value2 = float(v2)
            pass

        elif type == "3":  # list
            try:
                if isinstance(v1, str):
                    v1 = eval(v1)
                if isinstance(v2, str):
                    v2 = eval(v2)
            except Exception as e:
                return False
            # print('v1:',v1,'v2:',v2,len(v2))
            if len(v2)==1:
                z = 0
                for i in v1:
                    if i == v2[0]:
                        z += 1
                        pass
                    else:
                        return False
                return True
            else:
                info = 'V2的值应该只有一个'
                return False

        elif type == "4": #str
            pass
    except ValueError:
        return False

# 获取文件编码类型
def get_encoding(file):
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read()
        return chardet.detect(data)['encoding']

def fuzzy_find(dir, name):
    # 文件名模糊匹配，暂时仅支持dir路径下的文件
    # print(dir)
    fuzzy_find_list = []
    for i in [x for x in os.listdir(dir) if os.path.isfile(os.path.join(dir, x)) and name in os.path.splitext(x)[0]]:
        print(os.path.join(dir, i))
        fuzzy_find_V = os.path.join(dir, i)
        fuzzy_find_list.append(fuzzy_find_V)

    # os.path.isfile() 需要完整路径或者相对当前目录的相对路径
    #  如果需要查下dir路径下所有文件夹下的文件，开放以下代码。。暂时仅支持dir路径下的文件
    # for i in [x for x in os.listdir(dir) if os.path.isdir(os.path.join(dir, x))]:
    #     if os.listdir(os.path.join(dir, i)):
    #         # 防止因为权限问题报错
    #         try:
    #             fuzzy_find(os.path.join(dir, i), name)
    #         except:
    #             pass
    return fuzzy_find_list


from calculation import *
def air_density_info(wen_list,ya_list):
    wen_status, wen_info, wen_list_float = str_to_float(wen_list)
    ya_status, ya_info, ya_list_float = str_to_float(ya_list)
    V = []
    if wen_status and ya_status :  # 2个状态均为True
        air_v = air_density(wen_list_float, ya_list_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：wen_info:'+  wen_info + 'ya_info:'+ ya_info
        return False,info,[]

def Wind_power_density_info(wen_list,ya_list,UAVG4_list):
    wen_status, wen_info, wen_list_float=str_to_float(wen_list)
    ya_status, ya_info, ya_list_float=str_to_float(ya_list)
    UAVG4_status, UAVG4_info, UAVG4_list_float=str_to_float(UAVG4_list)
    V = []
    if wen_status and ya_status and UAVG4_status:  #三个状态均为True
        Wind_power_density_infoV = Wind_power_density(wen_list_float,ya_list_float,UAVG4_list_float)
        # print(Wind_power_density_infoV,type(Wind_power_density_infoV))
        V.append(Wind_power_density_infoV)
        return True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：wen_info:'+  wen_info + 'ya_info:'+ ya_info + 'UAVG4_info:'+UAVG4_info
        return False,info,[]

def average_info(records_list):
    status, info, records_list_float = str_to_float(records_list)
    V = []
    if status :  #  状态均为True
        air_v = get_average(records_list_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info
        return False,info,[]

def average_jing_info(records_list):
    status, info, records_list_float = str_to_float(records_list)
    V = []
    if status :  # 状态均为True
        air_v = get_average_jing(records_list_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info
        return False,info,[]

def get_sum_info(records_list):
    status, info, records_list_float = str_to_float(records_list)
    V = []
    if status :  # 状态均为True
        air_v = get_sum(records_list_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info
        return False,info,[]

def get_mse_info(records_Pmi_list,records_Ppi_list):
    status1, info1, records_Pmi_float = str_to_float(records_Pmi_list)
    status2, info2, records_Ppi_float = str_to_float(records_Ppi_list)
    V = []
    if status1 and status2 :  # 2个状态均为True
        air_v = get_mse(records_Pmi_float,records_Ppi_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info1+info2
        return False,info,[]

def get_rmse_info(records_Pmi_list,records_Ppi_list,records_Sop_list):
    status1, info1, records_Pmi_float = str_to_float(records_Pmi_list)
    status2, info2, records_Ppi_float = str_to_float(records_Ppi_list)
    status3, info3, records_Sop_float = str_to_float(records_Sop_list)
    V = []
    if status1 and status2 and status3 :  # 3个状态均为True
        air_v = get_rmse(records_Pmi_float,records_Ppi_float,records_Sop_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+ info1+info2+info3
        return False,info,[]

def get_mae_info(records_Pmi_list,records_Ppi_list,records_Sop_list):
    status1, info1, records_Pmi_float = str_to_float(records_Pmi_list)
    status2, info2, records_Ppi_float = str_to_float(records_Ppi_list)
    status3, info3, records_Sop_float = str_to_float(records_Sop_list)
    V = []
    if status1 and status2 and status3 :  # 3个状态均为True
        air_v = get_mae(records_Pmi_float,records_Ppi_float,records_Sop_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info1+info2+info3
        return False,info,[]

def get_colrel_info(records_Pmi_list,records_Ppi_list):
    status1, info1, records_Pmi_float = str_to_float(records_Pmi_list)
    status2, info2, records_Ppi_float = str_to_float(records_Ppi_list)
    V = []
    if status1 and status2 :  # 2个状态均为True
        air_v = get_colrel(records_Pmi_float,records_Ppi_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info1+info2
        return False,info,[]

def get_qualify_info(records_Pmi_list,records_Ppi_list,records_Sop_list,ratio):
    status1, info1, records_Pmi_float = str_to_float(records_Pmi_list)
    status2, info2, records_Ppi_float = str_to_float(records_Ppi_list)
    status3, info3, records_Sop_float = str_to_float(records_Sop_list)
    ratio_float = float(ratio)
    V = []
    if status1 and status2 and status3 :  # 3个状态均为True
        air_v = get_qualify(records_Pmi_float,records_Ppi_float,records_Sop_float,ratio_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info1+info2+info3
        return False,info,[]

def get_max_errorlv_info(max_error_list,ratio):
    status, info, records_Pmi_float = str_to_float(max_error_list)
    ratio_float = float(ratio)
    V = []
    if status :  # 状态均为True
        air_v = get_max_errorlv(records_Pmi_float,ratio_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info
        return False,info,[]

def get_er_Harmonic_mean_info(records_Pfi_list,records_Pri_list,records_Sop_list):
    status1, info1, records_Pfi_float = str_to_float(records_Pfi_list)
    status2, info2, records_Pri_float = str_to_float(records_Pri_list)
    status3, info3, records_Sop_float = str_to_float(records_Sop_list)
    V = []
    if status1 and status2 and status3 :  # 3个状态均为True
        air_v = get_er_Harmonic_mean(records_Pfi_float,records_Pri_float,records_Sop_float)
        V.append(air_v)
        return  True, '', V
    else:
        info ='此类型仅支持值为浮点数类型的数据，详细信息参考：info:'+  info1+info2+info3
        return False,info,[]

def str_to_float(strtoint):
    strtointV=[]
    try:
        if isinstance(strtoint, list):
            for i in strtoint:
                if isinstance(i, list):
                    for j in i:
                        strtointV.append(float(j))
                else:
                    strtointV.append(float(i))
        print(strtointV)
        return True,'', strtointV
    except Exception as e:
        info = str(e)
        return False, info ,[]


if __name__ == '__main__':
    # v1 = ['25','25','25','25','29']   #失败
    # v1 = ['25', '25', '25', '25', '25']  #通过
    # v2 = ['25']
    # v1 = ['25.33', '25.33', '25.33', '25.33', '25.333']  # 失败
    # v1 = ['25.33', '25.33', '25.33', '25.33', '25.33']  # 通过
    # v2 = ['25.33']
    # v1 = ['a', 'a', 'a', 'a', 'v']  # 失败
    # v1 = ['a', 'a', 'a', 'a', 'a']   # 通过
    # v2 = ['a']
    # v1 = [['a'], ['a'], ['a'], ['a'], ['v']]  # 失败
    # v1 = [['a'], ['a'], ['a'], ['a']]   # 通过
    # v2 = [['a']]
    # a = cmp_eq_ManyToOne('3',v1,v2)
    # print(a)
    # c = "{'wen_list':{'sql':'select AVERAGE from hdranastat5m20220925 h WHERE  h.ID = 150 AND hdtime &lt;= 2022-09-25 12:00:00','dbtype':'QMYSQL','concectstr':'10.64.14.70@3306@davinci@_@_','return_type':'3'},'ya_list':{'sql':'select AVERAGE from hdranastat5m20220925 WHERE ID = 152AND hdtime &lt;= 2022-09-25 12:00:00','dbtype':'QMYSQL','concectstr':'10.64.14.70@3306@davinci@_@_','return_type':'3'},'UAVG4_list':{'sql':'select AVERAGE from hdranastat5m20220925 h WHERE  h.ID = 118 AND hdtime &lt;= 2022-09-25 12:00:00','dbtype':'QMYSQL','concectstr':'10.64.14.70@3306@davinci@_@_','return_type':'3'}}"

    # c = "{'wen_list':{'sql':'select AVERAGE from hdranastat5m20220925 h WHERE  h.ID = 150 AND hdtime <= \"2022-09-25 12:00:00\"','dbtype':'QMYSQL','concectstr':'10.64.14.70@3306@davinci@_@_','return_type':'3'},'ya_list':{'sql':'select AVERAGE from hdranastat5m20220925 WHERE ID = 152 AND hdtime <= \"2022-09-25 12:00:00\"','dbtype':'QMYSQL','concectstr':'10.64.14.70@3306@davinci@_@_','return_type':'3'},'UAVG4_list':{'sql':'select AVERAGE from hdranastat5m20220925 h WHERE  h.ID = 118 AND hdtime <= \"2022-09-25 12:00:00\"','dbtype':'QMYSQL','concectstr':'10.64.14.70@3306@davinci@_@_','return_type':'3'}}"
    # zz = Wind_power_density_info(c)
    # print(zz)
    wen_list = [18.080883, 18.146992, 18.997122, 17.270521, 14.848958, 15.579979, 15.730692, 15.136827, 16.550747,
                16.693224, 15.69696, 16.121559, 15.397946, 16.41503, 15.372396, 14.925009, 16.133266, 14.094671,
                15.663481, 13.680895, 14.153921, 15.216837, 14.008252, 13.206653, 14.757754, 15.424355, 14.902432,
                14.743851, 14.174669, 13.510941, 14.49704, 14.521811, 14.929316, 15.317182, 14.467303, 15.301455,
                14.751183, 13.171198, 15.174275, 14.786418, 14.920753, 14.158562, 15.039986, 15.92536, 14.089961,
                14.976439, 16.312267, 14.280208, 14.581764, 14.809026, 15.769786, 14.455037, 14.769136, 14.494644,
                15.062724, 14.561975, 14.182638, 14.178203, 14.188215, 14.770731, 14.537947, 13.973462, 14.462481,
                14.648555, 15.109258, 13.596306, 14.065555, 14.798264, 15.882815, 14.701647, 16.289982, 15.824636,
                15.660245, 15.255106, 14.600351, 13.750204, 16.111528, 15.500712, 14.960322, 14.723643, 15.824072,
                15.57301, 14.460184, 15.399426, 13.390574, 15.533084, 15.181247, 15.935135, 15.56382, 15.553515,
                15.604373, 15.784166, 16.014088, 17.072958, 16.563173, 16.065205, 15.245549, 15.098117, 15.959723,
                16.712467, 17.127872, 17.71043, 15.91936, 18.141941, 17.285915, 17.513311, 17.517384, 17.716255,
                17.396917, 17.158464, 18.758165, 20.10442, 19.493979, 19.734114, 20.785976, 19.194504, 20.147345,
                19.05809, 21.146671, 18.461926, 22.01532, 19.653027, 21.131748, 21.106976, 22.121136, 19.784822,
                22.293369, 21.190825, 23.218082, 23.147083, 24.267294, 22.912989, 23.307728, 24.230083, 22.425404,
                22.583181, 24.860432, 22.083473, 23.115351, 22.443157, 25.214792, 23.461481, 25.432896, 21.972866,
                23.813848]
    ya_list = [965.172241, 982.585571, 1070.912231, 1008.069824, 931.344727, 919.641418, 1088.778931, 982.770813,
               1082.627197, 1012.066101, 998.327637, 969.60437, 962.877136, 1056.975342, 962.887695, 1089.05542,
               1004.81427, 995.336548, 914.813477, 987.86261, 1017.208496, 1053.126221, 1004.685181, 928.64679,
               983.539062, 954.212769, 1001.829956, 954.527161, 970.430664, 1025.261108, 1034.56543, 1060.087646,
               1031.903809, 895.050415, 990.48407, 1067.82251, 976.737, 993.243469, 991.15741, 994.780273, 976.364441,
               1009.649597, 997.250854, 1012.435364, 964.134644, 991.871887, 1005.106445, 1028.738281, 989.685181,
               1008.036255, 1005.358582, 968.600098, 1046.937256, 981.408813, 953.084351, 1072.827393, 1055.609253,
               1011.358765, 989.982544, 1038.352417, 1041.193604, 887.989624, 1053.900391, 1021.782593, 985.600281,
               1052.486572, 937.00647, 1004.649902, 1011.81543, 932.849792, 1049.757202, 976.976562, 1003.807434,
               973.179199, 955.375977, 986.27948, 900.563599, 997.119141, 888.479797, 1051.702759, 979.408569,
               1030.243042, 1025.72876, 925.431458, 972.608276, 975.318054, 966.262329, 1056.792847, 1022.13562,
               963.114868, 1079.64917, 994.020996, 924.965515, 1076.390625, 1056.88208, 899.119324, 972.302734,
               1005.443665, 991.372375, 1024.360229, 939.636536, 1053.595337, 1006.932312, 1074.522339, 1001.156128,
               1033.109619, 999.384155, 1095.758057, 1090.059814, 1037.734009, 1082.939697, 1004.284668, 986.997864,
               991.588257, 1034.16626, 1077.788086, 1058.408081, 1050.389404, 998.372681, 973.578613, 1037.615967,
               993.55127, 1009.130066, 942.129517, 925.634949, 1036.079712, 1077.960205, 1032.586426, 1062.578857,
               1062.33374, 967.860046, 1040.9729, 1045.366455, 993.26709, 916.296265, 1042.066406, 1138.586548,
               980.255188, 1020.958801, 983.046265, 1086.649658, 934.062378, 1115.530151, 950.957214, 944.792175]
    UAVG4_list = [6.600135, 6.902103, 7.288026, 7.162987, 6.026829, 5.862588, 5.956954, 6.477087, 5.789676, 5.54744,
                  6.269628, 6.488135, 5.775191, 5.848012, 6.284585, 6.100736, 5.684309, 6.414113, 6.473575, 6.40672,
                  5.934304, 6.130612, 5.776731, 6.751481, 7.109408, 5.792567, 6.123112, 6.230389, 6.677688, 6.415565,
                  5.806245, 6.216517, 6.244184, 6.087986, 5.897303, 6.050489, 6.323955, 5.768836, 5.907832, 6.190647,
                  5.884389, 6.194135, 6.011926, 6.078424, 6.047881, 6.347197, 6.176398, 5.771305, 6.05608, 6.295416,
                  5.951276, 6.268971, 6.247163, 6.194509, 5.953842, 6.124961, 5.821764, 6.661878, 5.83452, 6.026638,
                  5.782928, 6.327443, 6.631525, 6.667573, 6.431901, 6.38371, 6.855026, 6.295933, 6.411194, 6.012984,
                  6.130702, 6.32671, 5.717523, 6.437647, 6.604208, 6.063986, 6.430025, 6.54708, 6.692842, 6.380589,
                  5.925869, 6.523567, 6.864968, 6.926992, 6.446718, 6.230165, 5.795476, 7.124116, 6.254269, 6.645165,
                  5.984663, 6.624059, 6.09376, 6.214676, 6.170628, 6.450087, 6.66549, 6.139302, 6.243759, 6.466268,
                  6.096755, 6.316548, 6.279651, 5.994401, 6.617434, 6.49678, 6.122848, 5.76351, 5.893606, 5.847435,
                  5.732307, 6.380158, 5.658645, 5.7197, 5.624493, 5.811643, 5.854457, 5.309171, 5.947221, 5.514572,
                  5.030105, 4.798052, 5.543616, 5.458755, 5.464671, 4.86673, 5.295035, 5.362599, 5.237343, 5.429326,
                  5.208882, 5.400497, 5.26118, 5.428751, 5.18083, 5.57345, 4.88712, 5.657399, 5.2132, 5.594353,
                  5.361287, 5.499493, 5.295648, 5.337471, 5.20715]
    a = Wind_power_density_info(wen_list, ya_list, UAVG4_list)
    print(a)

