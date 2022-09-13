#coding:utf-8

import evnbase as eb
import evnfcst  as ef

# import sys
# from pluginmanager import PluginManager
# from pluginmanager import __ALLMODEL__

'''在此增加其他业务环境变量构建类import'''

def setevn(classname):
    myeb = None
    if classname == "EnvFcst": #功率预测环境变量创建
        myeb= ef.EnvFcst()
        if not myeb is None:
            myeb.setenv()
    else:
        pass
        # PluginManager.LoadAllPlugin();
        # #遍历所有接入点下的所有插件
        # bFound = False
        # for SingleModel in __ALLMODEL__:
        #     plugins = SingleModel.GetPluginObject()
        #     for item in plugins:
        #         if item.get_type() == "Model_StepFunction":
        #             if item.getid() == classname:
        #                 bFound = True
        #                 item.init_env()

def setwebdriver(drivername):
    pass