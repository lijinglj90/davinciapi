#coding:utf-8
'''
功能说明：
    本模块为自动化测试框架入口程序，通过传入参数执行响应的自动化测试用例并输出执行结果.

    1）本框架包含测试用例读取功能和执行框架入口，支持执行单个用例模块文件和以目录为参数执行多个用例文件的形式；

    2）本框架支持通过传入用例等级号限定需要执行的用例范围，用例等级号为0开始的整数，数值越小等级越高。
    
       举例说明，当输入用例等级为3时，则执行用例中等级为0、1、2和3的用例；
    
    3）本框架支持在执行期特化环境变量，用于用例中使用；

    4）用例文件存储。用例以xml格式存储为一个树型结构，结构层次为“模块”->“测试套件”->“测试用例”->“测试步骤”，其中说明如下：
       
       模块：一个物理文件形式的测试用例集合为一个模块，测试工程师可根据测试需要规划和定义，其可以包括1至n个测试套件；

    

:解析参数：

    -m 用例等级id，长参数为--mark，用于控制执行时选取需执行的用例

    -f 用例文件，长参数为--file

    -p 用例文件存放路径，长参数为--path，当需要执行选定目录下的所有用例文件时使用

    -e 环境变量，长参数为--evnbase，为"模块名.类名",如功率预测的为"evnfcst.EnvFcst"，用于特立化执行环境

'''
from caseobj import SuitObj
from caseobj import StepCfg
import xml.etree.ElementTree as ET
import caseobj as cb
import sys
import getopt
import os
import evnobj as eo
import logger as lg


#全局唯一标识
unique_id = 1
   
#遍历所有的节点
def __readstep__(node):
    '''
    读取用例文档步骤定义信息
    
    传入参数：

        node：用例文档（xml格式）的步骤节点（xml.etree.ElementTree）
    
    返回参数：

        step_temp：StepCfg对象，参见StepCfg相关说明

    '''
    step_temp = cb.StepCfg(node.attrib["order"],node.attrib["cmdtype"],node.attrib["cmdparas"])
    return step_temp

def __readcase__(node):
    '''读取用例信息'''
    case_temp = cb.CaseCfg(node.attrib["id"],node.attrib["name"],node.attrib["faulttype"],node.attrib["mark"])

    step_node = node.getchildren()
    if len(step_node) > 0:
        for step in step_node:
            step_temp = __readstep__(step)
            if step.tag == "step":
               case_temp.appendstep(step_temp)
            elif step.tag == "judgestep":
                case_temp.setjudgestep(step_temp)
            else:
                pass
    
    return case_temp

def __readsuit__(node,result_list):
    '''读取套件配置信息'''
    suit = cb.SuitCfg(node.attrib["id"],node.attrib["name"])
    children_node = node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        if child.tag == "precondition":
            step_node = child.getchildren()
            if len(step_node) > 0:
                for step in step_node:
                    step_temp = __readstep__(step)
                    suit.appendcondstep(step_temp)            
        elif child.tag == "case":
            case_temp = __readcase__(child)
            suit.appendcase(case_temp)
        else:
            pass  
         
    return suit
 
def __readfile__(file_name):
    '''读取测试用例文件'''
    import logger as lg
    try:
        tinfo = '******************开始读取[%s]内容******************'% file_name
        # print(tinfo)
        lg.myloger.info(tinfo)
        result_list = []
        root = ET.parse(file_name).getroot()
        if root.tag == "test":
            children_node = root.getchildren()
            if len(children_node) == 0:
                return True, []
            for child in children_node:
                if child.tag == "suit":
                  suit =  __readsuit__(child, result_list)
                  result_list.append(suit)
        return True, result_list
    except Exception as e:
        info = """ ******************[%s]用例书写错误整个用例未执行****************** 
        报错信息：[%s] 
        """ % (file_name, str(e))
        # lg.myloger.info(info)
        return False, info

def __findfiles__(path, t):
    files = os.listdir(path)
    for f in files:
        npath = path + '/' + f
        if(os.path.isfile(npath)):
            if(os.path.splitext(npath)[1] ==".xml"):
                t.append(npath)
        if(os.path.isdir(npath)):
            if (f[0] == '.'):
                pass
            else:
                __findfiles__(npath, t)
    return


if __name__ == "__main__":
    # '''
    # 解析参数：
    #     -m 用例等级id，长参数为--mark
    #     -f 用例文件，长参数为--file
    #     -p 用例文件存放路径，长参数为--path
    #     -e 环境变量，长参数为--evnbase，为"模块名.类名",如功率预测的为"evnfcst.EnvFcst"
    # '''
    # try:
    #     options,args = getopt.getopt(sys.argv[1:],"m:f:p:b:l", ["mark=","file=","path=","evnbase=","files="])
    # except getopt.GetoptError:
    #     sys.exit()
    #
    mark = "0"    #控制xml文件内，单条case是否运行  目前建议全部写0
    file = ""     #忽略
    # 写文件夹，程序活获取次文件夹下所有的xml文件存储到files变量  files=[]
    # path = r"D:/davinciapi/case/SpFcst/UI"
    # path = r"D:\davinciapi\case\zz"
    path = ''
    # path = r'C:\davinciapi\case\SpFcst\UI'
    baseevn = ""  #忽略
    # 写具体某一个xml文件  path变量需要为空，path=[]
    # files = [r"D:/davinciapi/case/SpFcst/UI/COMMON/test_cdqyc.xml"]
    #
    # # print(options)
    # for name,value in options:
    #     if name in ("-m","--mark"):
    #         mark = value
    #     elif name in ("-f","--file"):
    #         file = value
    #     elif name in ("-p","--path"):
    #         path=value
    #     elif name in ("-b","--evnbase"):
    #         baseevn=value
    #     elif name in ("-l", "--files"):
    #         c = value
    #         files.append(value)

    files = []
    if not file.strip()=="":
        files.append(file)

    if not path.strip()=="":
        tfs = []
        __findfiles__(path,tfs)
        files.extend(tfs)
    print(files)

    # '''设置基本环境变量'''
    # if len(baseevn) > 0:
    #     eo.setevn(baseevn)
    #
    # if len(files) == 0:
    #     lg.myloger.error("参数错误:未传入有效用例文件")

    #暂时先这么写死，后期会增改的哦
    # mark = "0"
    # file = ""
    #path = ""
    # baseevn = ""
    files = [r"D:/davinciapi/case/zz/test_yichang.xml"]
    # files = [r"/home/sprixin/davinciapi/case/test_yichang.xml"]

    report_info = ""

    '''读取用例数据'''

    for casefile in files:
        suits = []
        info = '######################用例[%s]执行情况：######################'% casefile
        report_info += info
        report_info += "\n\n"
        status,subsuits =__readfile__(casefile)
        # print(status, subsuits)

        if status:   #True
            suits.extend(subsuits)
            '''执行用例套件'''
            for suit in suits:
                sb = SuitObj(suit)
                rp = sb.myexec(mark)
                report_info += rp
                report_info += "\n\n"
        else:
            report_info += subsuits
            report_info += "\n\n"




    '''发出报告'''
    print(report_info)

