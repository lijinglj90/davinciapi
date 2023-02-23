#!/usr/bin/env python

import getopt
import sys


def usage():
    print("=======")
    print("Usage:")
    jieshi = """示例：python pygetopt.py -m 0  或者： python pygetopt.py --mark 0
    -h 帮助信息
    -m 用例等级id，长参数为--mark  控制xml文件内，单条case是否运行  目前建议全部写0
    -f 单个用例文件，长参数为--file  写具体某一个文件，存储到files变量
    -p 用例文件存放路径，长参数为--path  写文件夹，程序活获取次文件夹下所有的xml文件存储到files变量 
    -e 环境变量，长参数为--evnbase，为"模块名.类名",如功率预测的为"evnfcst.EnvFcst"
    """
    print(jieshi)
    # 需要运行的.py文件在哪，在控制台cd到对应目录下执行下方语句
    print("=======")


def getoptmain():
    """
    getopt 模块的用法

    # 解析参数：
    #     -h 帮助信息
    #     -m 用例等级id，长参数为--mark  控制xml文件内，单条case是否运行  目前建议全部写0
    #     -f 单个用例文件，长参数为--file  写具体某一个文件，存储到files变量
    #     -p 用例文件存放路径，长参数为--path  写文件夹，程序活获取次文件夹下所有的xml文件存储到files变量
    #     -b 环境变量，长参数为--evnbase，为"模块名.类名",如功率预测的为"evnfcst.EnvFcst"
    """

    try:
        options,args = getopt.getopt(sys.argv[1:],"-h-m:-f:-p:-b:-l:", ["help","mark=","file=","path=","evnbase=","files="])
    except getopt.GetoptError:
        sys.exit()

    optionss = {'mark': '0', 'file': '','path':'','baseevn':''}
    for name,value in options:
        files = []
        if name in ('-h', '--help'):
            usage()
        elif name in ("-m","--mark"):
            optionss['mark'] = value
        elif name in ("-f","--file"):
            optionss['file'] = value
        elif name in ("-p","--path"):
            optionss['path'] = value
        elif name in ("-b","--evnbase"):
            optionss['baseevn'] = value
        elif name in ("-l", "--files"):
            c = value
            files.append(value)
            optionss['files'] = files
    for name in args:
        optionss["name_{0}".format(name)] = name
    return optionss

# if __name__ == "__main__":
#     a = getoptmain()
#     print(a)