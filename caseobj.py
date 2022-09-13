from datetime import datetime, timedelta
from stepobj import StepObj
from string import Template
import string
import logger as lg
from splitcfg import SplitSymbol
from dateutil.relativedelta import relativedelta
import os
import platform

STEP_ARG_SPAN = SplitSymbol.SYMBOL_BETWEEN_ARGS

class CaseResult():
    '''用例执行结果结构体
    :属性说明：
    - id:      Case编号
    - status:  执行结果
    - desc:    执行异常信息
    '''
    def __init__(self,id:str,status:int,desc:str):
        '''用例执行结果结构初始化函数'''
        self.id = id
        self.status = status
        self.desc = desc

class StepCfg():
    '''步骤定义
    :属性说明：
    - Order:     步骤序号
    - cmdtype:   步骤命令类型
    - cmdparas:  步骤命令执行参数，类型为LIST
    '''
    def __init__(self,order,cmdtype,cmdparas:str):
        '''步骤定义初始化函数'''
        self.order = order
        self.cmdtype = cmdtype
        self.cmdparas = cmdparas.split(STEP_ARG_SPAN)


class CaseCfg():
    '''用例定义
    :属性说明：
    - id:        用例编号
    - name:      用例名称
    - faulttype  错误处理类型，0为接着执行，1为中断后续用例执行
    - mark       用例等级
    '''
    def __init__(self,id:str,name:str,faulttype=0,mark=""):
        '''用例定义结构初始化函数'''
        self.id = id
        self.name = name
        self.steps=[]
        self.judgestep=None
        self.faulttype=faulttype
        self.stepcount = 0
        self.mark = mark

    def appendstep(self,step:StepCfg):
        '''把步骤加到用例的步骤队列中
        :输入参数：
        - step:        类型为StepCfg

        :输出参数:
        - stepcount:   当前步骤计数
        '''
        self.steps.append(step)
        self.stepcount += 1
        return self.stepcount

    def setjudgestep(self,step:StepCfg):
        '''设置用例判断步骤
        :输入参数：
        - step:        类型为StepCfg

        :输出参数:
        - 无
        '''
        self.judgestep=step

    def checkcase(self):
        '''检查用例完整性
        :输入参数：
        - 无

        :输出参数:
        - status:   完整则返回True，否则返回False
        - info:     错误信息
        '''
        if self.judgestep is None:
            return False,"缺少用例预期结果判定步骤"
        
        if len(self.steps) == 0:
            return False,"用例步骤为空"
        
        if len(self.id) == 0:
            return False,"用例ID未设置"


class SuitCfg():
    '''套件定义
    :属性说明：
    - id:             套件编号
    - name:           套件名称
    - condsteps:      套件前置条件列表
    - condstepcount   套件前置条件数目
    - cases           套件用例列表
    - casecount       套件用例个数
    '''
    def __init__(self,id,name):
        '''套件定义结构初始化函数'''
        self.id = id
        self.name = name
        self.condsteps = []
        self.condstepcount = 0
        self.cases = []
        self.casecount= 0
    
    def appendcondstep(self,step:StepCfg):
        '''把步骤加到套件前置步骤队列中
        :输入参数：
        - step:        类型为StepCfg

        :输出参数:
        - stepcount:   当前前置步骤计数
        '''
        self.condsteps.append(step)
        self.condstepcount += 1
        return self.condstepcount
    
    def appendcase(self,case:CaseCfg):
        '''把用例加到套件用例队列中
        :输入参数：
        - case:        类型为CaseCfg

        :输出参数:
        - casecount:   当前用例个数计数
        '''
        self.cases.append(case)
        self.casecount += 1
        return self.casecount    

def __generate_rt_paras__():
    '''生成实时变量
    - RTPARA_TODAY_1：      "%Y%m%d"格式的当前日期
    - RTPARA_TODAY_2：      "%Y-%m-%d"格式的当前日期
    - RTPARA_TODAY_3：      "%Y/%m/%d"格式的当前日期
    - RTPARA_CURRTIME_1：   "%Y-%m-%d %H:%M:%S"格式的当前时刻
    - RTPARA_YEAR_1：       "%Y"格式的当前年份  [2022]
    - RTPARA_YEAR_2：       "%y"格式的当前年份  [22]
    - RTPARA_YEARMONTH_1：  "%Y%m"格式的当前月份
    - RTPARA_YEARMONTH_2：  "%Y-%m"格式的当前月份
    - RTPARA_YEARMONTH_3：  "%Y/%m"格式的当前月份
    - RTPARA_MONTH_1：      "%m"格式的当前月份 [01,02,03,04~~]
    - RTPARA_MONTH_2：      "%m"格式的当前月份 [1,2,3,4~~]
    - RTPARA_DAY_1：        "%d"格式的当前日 [01,02,03,04~~]
    - RTPARA_DAY_2：        "%d"格式的当前日 [1,2,3,4~~]
    - RTPARA_YESTERDAY_1：      "%Y%m%d"格式的昨日日期
    - RTPARA_YESTERDAY_2：      "%Y-%m-%d"格式的昨日日期
    - RTPARA_YESTERDAY_3：      "%Y/%m/%d"格式的昨日日期
    - RTPARA_YESTERDAY_DAY_1：  "%d"格式的昨天-日 [01,02,03,04~~]
    - RTPARA_YESTERDAY_DAY_2：  "%d"格式的昨天-日 [1,2,3,4~~]
    - RTPARA_TOMORROW_1：      "%Y%m%d"格式的明日日期
    - RTPARA_TOMORROW_2：      "%Y-%m-%d"格式的明日日期
    - RTPARA_TOMORROW_3：      "%Y/%m/%d"格式的明日日期
    - RTPARA_TOMORROW_DAY_1   "%d"格式的明天-日 [01,02,03,04~~]
    - RTPARA_TOMORROW_DAY_2   "%d"格式的明天-日 [1,2,3,4~~]
    - RTPARA_LASTYEAR_1       "%Y"格式的去年年份  [2021]
    - RTPARA_LASTYEAR_2       "%y"格式的去年年份  [21]
    - RTPARA_NEXTYEAR_1       "%Y"格式的明年年份  [2023]
    - RTPARA_NEXTYEAR_2       "%y"格式的明年年份  [23]
    - RTPARA_YEAR_LASTMONTH_1  "%Y%m"格式的上个月月份
    - RTPARA_YEAR_LASTMONTH_2  "%Y-%m"格式的上个月月份
    - RTPARA_YEAR_LASTMONTH_3  "%Y/%m"格式的上个月月份
    - RTPARA_LASTMONTH_1      "%m"格式的上个月月份  [01,02,03~~]m
    - RTPARA_LASTMONTH_2      "%m"格式的上个月月份 [1,2,3,4~~]
    - RTPARA_YEAR_NEXTMONTH_1  "%Y%m"格式的下个月月份
    - RTPARA_YEAR_NEXTMONTH_2  "%Y-%m"格式的下个月月份
    - RTPARA_YEAR_NEXTMONTH_3  "%Y/%m"格式的下个月月份
    - RTPARA_NEXTMONTH_1      "%m"格式的下个月月份 [01,02,03,04~~]
    - RTPARA_NEXTMONTH_2      "%m"格式的下个月 [1,2,3,4~~]

    '''
    # start_date = datetime.strptime("2019-04-15", "%Y-%m-%d")

    paras = {}
    #当前时间
    paras["RTPARA_TODAY_1"] = datetime.now().strftime("%Y%m%d")
    paras["RTPARA_TODAY_2"] = datetime.now().strftime("%Y-%m-%d")
    paras["RTPARA_TODAY_3"] = datetime.now().strftime("%Y/%m/%d")
    paras["RTPARA_CURRTIME_1"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #当前年
    paras["RTPARA_YEAR_1"] = datetime.now().strftime("%Y")
    paras["RTPARA_YEAR_2"] = datetime.now().strftime("%y")
    #当前年月
    paras["RTPARA_YEARMONTH_1"] = datetime.now().strftime("%Y%m")
    paras["RTPARA_YEARMONTH_2"] = datetime.now().strftime("%Y-%m")
    paras["RTPARA_YEARMONTH_3"] = datetime.now().strftime("%Y/%m")
    #当前月
    paras["RTPARA_MONTH_1"] = datetime.now().strftime("%m")
    paras["RTPARA_MONTH_2"] = datetime.now().month
    #当前日
    paras["RTPARA_DAY_1"] = datetime.now().strftime("%d")
    paras["RTPARA_DAY_2"] = datetime.now().day

    #昨天
    dt_y = datetime.now() + timedelta(days=-1)
    paras["RTPARA_YESTERDAY_1"] = dt_y.strftime("%Y%m%d")
    paras["RTPARA_YESTERDAY_2"] = dt_y.strftime("%Y-%m-%d")
    paras["RTPARA_YESTERDAY_3"] = dt_y.strftime("%Y/%m/%d")

    paras["RTPARA_YESTERDAY_DAY_1"] = dt_y.strftime("%d")
    paras["RTPARA_YESTERDAY_DAY_2"] = dt_y.day

    #明天
    dt_t = datetime.now() + timedelta(days=1)
    paras["RTPARA_TOMORROW_1"] = dt_t.strftime("%Y%m%d")
    paras["RTPARA_TOMORROW_2"] = dt_t.strftime("%Y-%m-%d")
    paras["RTPARA_TOMORROW_3"] = dt_t.strftime("%Y/%m/%d")

    paras["RTPARA_TOMORROW_DAY_1"] = dt_t.strftime("%d")
    paras["RTPARA_TOMORROW_DAY_2"] = dt_t.day

    #去年
    dt_lasty = datetime.now().date() - relativedelta(years=1)
    paras["RTPARA_LASTYEAR_1"] = dt_lasty.strftime("%Y")
    paras["RTPARA_LASTYEAR_2"] = dt_lasty.strftime("%y")

    #明年
    dt_nexty = datetime.now().date() + relativedelta(years=1)
    paras["RTPARA_NEXTYEAR_1"] = dt_nexty.strftime("%Y")
    paras["RTPARA_NEXTYEAR_2"] = dt_nexty.strftime("%y")

    #上个月
    dt_lastm = datetime.now().date() - relativedelta(months=1)
    paras["RTPARA_YEAR_LASTMONTH_1"] = dt_lastm.strftime("%Y%m")
    paras["RTPARA_YEAR_LASTMONTH_2"] = dt_lastm.strftime("%Y-%m")
    paras["RTPARA_YEAR_LASTMONTH_3"] = dt_lastm.strftime("%Y/%m")
    paras["RTPARA_LASTMONTH_1"] = dt_lastm.strftime("%m")
    paras["RTPARA_LASTMONTH_2"] = dt_lastm.month

    #下个月
    dt_nextm = datetime.now().date() + relativedelta(months=1)
    paras["RTPARA_YEAR_NEXTMONTH_1"] = dt_nextm.strftime("%Y%m")
    paras["RTPARA_YEAR_NEXTMONTH_2"] = dt_nextm.strftime("%Y-%m")
    paras["RTPARA_YEAR_NEXTMONTH_3"] = dt_nextm.strftime("%Y/%m")
    paras["RTPARA_NEXTMONTH_1"] = dt_nextm.strftime("%m")
    paras["RTPARA_NEXTMONTH_2"] = dt_nextm.month

    # windows的下载路径：C:\Users\Administrator\Downloads
    # linux-sprixin下载目录：/home/sprixin/下载
    # linux-root下载目录：/root/下载
    plat = platform.system().lower()
    if plat == 'windows':
        print('现在使用的是windows系统')
        HOMEPATH = os.getenv('HOMEPATH')
        USERPROFILE = os.getenv('USERPROFILE')
        paras["DOWM_HOME"] = USERPROFILE + '\Downloads'
    elif plat == 'linux':
        print('现在使用的是linux系统')
        HOME = os.getenv('HOME')
        paras["DOWM_HOME"] = HOME + '/下载'


    # 项目当前路径
    CASEPATH = os.getcwd()
    paras["CASE_HOME"] = CASEPATH

    return paras

class CaseObj():
    '''用例对象
        用例执行主体
    :属性说明:
    - __case:               类型为CaseCfg，用例定义结构
    - __step_return_paras:  用例类公有参数，由构造时传入套件参数和执行过程中返回参数组成，可用用于随后的步骤执行
    '''
    def __init__(self,case:CaseCfg,suitparas ={}): 
        '''用例对象初始化函数'''
        self.__case = case
        self.__step_return_paras={}
        self.__step_return_paras.update(suitparas)
    
    def myexec(self):
        '''用例执行
        :输入参数:
        - 无
        :输出参数:
        - status   执行状态。0表示成功，1表示失败，2表示过程异常
        - info     执行出错信息

        "流程说明"
        - 按顺序执行用例操作步骤，如果执行步骤异常且因异常需返回则返回2
        - 执行预期结构判断，如果一致则返回0表示用例通过，如果不一致则返回1表示用例不通过
        - 在执行前替换掉步骤参数中的变量，参数中变量采用'$'开头，格式为“steppara_%d_%d”，
                其中第一个%d表示生成数据的步骤序号，第二个%d表示数据在其生成步骤返回值中的序号
                均以1开始
        - 在步骤执行过程中需把执行返回参数更新到返回参数map中
        '''
        try:
            info = "开始执行用例%s" % self.__case.name
            lg.myloger.info(info)

            for step in self.__case.steps:
                stepparas = self.__checkstepparas__(step.cmdparas)
                stepobj = StepObj(step.cmdtype,stepparas)
                stepretult = stepobj.myexec()
                if stepretult.status is False :
                    errorstr = "用例步骤[%s]执行异常：%s" % (step.order,stepretult.errordesc)
                    lg.myloger.error(errorstr)
                    return 2,errorstr

                suborder = 1
                for relpara in stepretult.returndatas:
                    key = "steppara_%s_%d" % (step.order,suborder)
                    self.__step_return_paras[key] = relpara

            judgestepparas = self.__checkstepparas__(self.__case.judgestep.cmdparas)
            judgeobj = StepObj(self.__case.judgestep.cmdtype,judgestepparas)
            stepretult = judgeobj.myexec()
            if stepretult.status is False :
                errorstr = "用例[%s]执行失败：%s" % (self.__case.id,stepretult.errordesc)
                lg.myloger.error(errorstr)
                return 1,errorstr
            else:
                return 0,""
        except Exception as e:
            info = '用例存在书写错误，请校验并检查。报错信息为：'+ str(e)
            return 1,info

        # info = "开始执行用例%s" % self.__case.name
        # lg.myloger.info(info)
        #
        # for step in self.__case.steps:
        #     stepparas = self.__checkstepparas__(step.cmdparas)
        #     stepobj = StepObj(step.cmdtype, stepparas)
        #     stepretult = stepobj.myexec()
        #     if stepretult.status is False:
        #         errorstr = "用例步骤[%s]执行异常：%s" % (step.order, stepretult.errordesc)
        #         lg.myloger.error(errorstr)
        #         return 2, errorstr
        #
        #     suborder = 1
        #     for relpara in stepretult.returndatas:
        #         key = "steppara_%s_%d" % (step.order, suborder)
        #         self.__step_return_paras[key] = relpara
        #
        # judgestepparas = self.__checkstepparas__(self.__case.judgestep.cmdparas)
        # judgeobj = StepObj(self.__case.judgestep.cmdtype, judgestepparas)
        # stepretult = judgeobj.myexec()
        # if stepretult.status is False:
        #     errorstr = "用例[%s]执行失败：%s" % (self.__case.id, stepretult.errordesc)
        #     lg.myloger.error(errorstr)
        #     return 1, errorstr
        # else:
        #     return 0, ""

    def __checkstepparas__(self,paras:list):
        '''替换参数中的变量
        :输入参数:
        - paras： 待替换的参数串列表

        :输出参数:
        - derparas：替换后的参数串列表
        '''
        '生成基于当前时间的参数'
        key_paras = __generate_rt_paras__()
        key_paras.update(self.__step_return_paras)
        derparas = []

        for parastr in paras:
            if parastr in key_paras.keys():
                derparas.append(key_paras[parastr])
            else:
                template = Template(parastr)
                mystr = template.substitute(key_paras)
                if isinstance(mystr,str ) and '##' in mystr:
                    mystr = mystr.replace("##", "")
                    # print('hahaha', mystr)
                derparas.append(mystr)
        return derparas

        
class SuitObj():
    '''套件对象'''

    def __init__(self,suit:SuitCfg): 
        '''套件初始化函数'''
        self.__suit = suit
        self.__case_return_paras={}
        self.__condstepparas={}
    
    def __checkstepparas__(self,paras:list):
        '''替换参数中的变量
        :输入参数:
        - paras： 待替换的参数串列表

        :输出参数:
        - derparas：替换后的参数串列表
        '''
        # print('qianqianqian',paras)
        '生成基于当前时间的参数'
        key_paras = __generate_rt_paras__()
        key_paras.update(self.__condstepparas)
        derparas = []
        for parastr in paras:
            if parastr in key_paras.keys():
                derparas.append(key_paras[parastr])
            else:
                template = Template(parastr)
                mystr = template.substitute(key_paras)
                if isinstance(mystr,str ) and '##' in mystr:
                    mystr = mystr.replace("##", "")
                    # print('hahaha', mystr)
                derparas.append(mystr)
        return derparas

    def myexec(self,mark=""):
        '''套件执行
        :输入参数:
        - mark 执行等级 如果为空，则执行所有用例，如果不为空则执行等级<=mark的用例

        :输出参数:
        - info  如果前置步骤执行异常则输出异常信息，否则输出执行报告
    
        '''

        info = "开始执行套件%s" % self.__suit.name
        lg.myloger.info(info)

        '执行前置条件'
        for step in self.__suit.condsteps:
            stepparas = self.__checkstepparas__(step.cmdparas)
            stepobj = StepObj(step.cmdtype,stepparas)
            stepretult = stepobj.myexec()
            if stepretult.status is False :
                errorstr = "******************套件id[%s]套件name[%s]前置步骤[%s]执行异常：%s，整个xml文件放弃执行******************" % (self.__suit.id,self.__suit.name,step.order,stepretult.errordesc)
                lg.myloger.error(errorstr)
                return errorstr

            suborder = 1
            for relpara in stepretult.returndatas:
                key = "suitcondpara_%s_%d" % (step.order,suborder)
                self.__condstepparas[key] = relpara
                suborder += 1

        '执行用例'
        for case in self.__suit.cases:
            if mark == "" or int(case.mark) <= int(mark):
                caseobj = CaseObj(case,self.__condstepparas)
                rel,relstr = caseobj.myexec()
                caserel = CaseResult(case.id,rel,relstr)
                self.__case_return_paras[case.id] = caserel
                if rel != 0 and case.faulttype == 1:
                    break

        '''生成套件执行报告'''
        return self.__report__()
    
    def __report__(self):
        '''
        生成套件执行报告函数
        :输入参数:
        - 无

        :输出参数:
        - report  报告内容。包括如下信息：\n
                  1)执行情况汇总信息。执行用例条数、成功调试、失败调试、执行过程异常和未执行条数
                  2）分项信息。包括成功用例ID列表，失败用例及原因，过程异常用例及原因列表

        '''
        reportstr = ""
        succeedcount = 0
        succeedinfo = ""
        failedcount = 0
        failedinfo = ""
        abnormalcount = 0
        abnormalinfo = ""
        notexecutedcount = 0
        notexecuteinfo = ""
        
        for caserelkey in self.__case_return_paras:
            caserel = self.__case_return_paras[caserelkey]
            if caserel.status == 0:
                succeedcount += 1
                if len(succeedinfo) > 0:
                    succeedinfo += ","
                succeedinfo += caserel.id
            elif caserel.status == 1:
                failedcount += 1
                failedinfo += "        " + caserel.id+":" + caserel.desc + "\n"
            else:
                abnormalcount += 1
                abnormalinfo += "        " + caserel.id+":" + caserel.desc + "\n"
        
        count = succeedcount + failedcount + abnormalcount
        if self.__suit.casecount > count:
            notexecutedcount = self.__suit.casecount - count
            for case in self.__suit.cases:
                if case.id not in self.__case_return_paras:
                    if len(notexecuteinfo) > 0:
                        succeedinfo += ","
                    notexecuteinfo += case.id
                
        reportstr = "******************套件id[%s]套件name[%s]执行情况******************\n" % (self.__suit.id,self.__suit.name)
        reportstr += "汇总信息：%d通过,%d未通过,%d执行异常,%d未执行\n" % (succeedcount,failedcount,abnormalcount,notexecutedcount)
        reportstr += "详细信息：\n"
        reportstr += "    执行通过用例数[%d]:\n" % succeedcount
        reportstr += "        %s\n" % succeedinfo
        reportstr += "    执行未通过用例数[%d]:\n" % failedcount
        reportstr += failedinfo
        reportstr += "    执行异常用例数[%d]:\n" % abnormalcount
        reportstr += abnormalinfo
        reportstr += "    未执行用例数[%d]:\n" % notexecutedcount
        reportstr += "        %s\n\n" % notexecuteinfo

        return reportstr

if __name__ == '__main__':
    a = __generate_rt_paras__()
    print(a)