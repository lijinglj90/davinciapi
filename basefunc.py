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

def cmp_file(file1:str,file2:str,encodestr=''):
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
    print('cmp_file:',file1,file2,encodestr)

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
    return filecmp.cmp(file1,file2),""


def isinfofile(file, keywords,type='1',CheckType='',separate='',return_type='3',encodingstr=''):
    """
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
    """
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

# if __name__ == '__main__':
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