#!/usr/bin/python
# -*- coding: UTF-8 -*-
 

import os
import json
import logger as lg
from splitcfg import SplitSymbol
import chardet

class JsonCfg():
    '''Json操作类'''

    #节点串连接符
    __node_splitstr=SplitSymbol.SYMBOL_BETWEEN_MODELLEVEL

    #条件串外层连接符
    __con_filter=SplitSymbol.SYMBOL_BETWEEN_MODELLEVEL
    #条件串外层连接符
    __con_nodefilter=SplitSymbol.SYMBOL_BETWEEN_OBJECT_AND_CONDITION

    #条件元串连接符
    __con_innerfilter=SplitSymbol.SYMBOL_BETWEEN_ELEMENTS_IN_CONDITION

    #条件元串并联连接符
    __con_and = SplitSymbol.SYMBOL_COMBINE_META
    
    def __init__(self,cfgpath:str): 
        '''构造函数
            功能：
                通过传入参数创建DOM对象
            参数：
                cfgpath，文件的路径，建议为绝对路径
        '''
        self.__cfgpath = cfgpath

        get_encoding = self.get_encoding(self.__cfgpath)
        if get_encoding:  # 程序自动获取文件编码格式，不为空
            self._encoding = get_encoding  # 使用程序获取的编码格式
        else:
            self._encoding = 'utf-8'  # 给一个默认值

        if not os.path.isfile(cfgpath):
            self.__hasfile = False
        else:
            self.__hasfile = True
            with open(self.__cfgpath, 'r', encoding=self._encoding) as f:
                    self.__json = json.load(f) 

    def get_encoding(self,cfgpath):
        # 二进制方式读取，获取字节数据，检测类型
        with open(cfgpath, 'rb') as f:
            data = f.read()
            return chardet.detect(data)['encoding']

    class Filter():
        '''节点选择定位条件结构。通过当前对象的一个子对象值定位当前对象，从而获取其他子对象
            属性说明：
                subname: 条件对象的子对象或属性
                value: 条件对象的子对象取值
        '''
        def __init__(self,subname,value):
            self.subobjname = subname
            self.subobjvalue = value
    
    class Node_Filter():
        '''节点-条件对结构
            属性说明：
                Obj：作用对象名
                filters: 条件对，多个条件取与关系，不支持或关系
        '''

        def __init__(self,Obj):
            self.node = Obj
            self.filters = []
        
        
        def addfilter(self, subname, value):
            '''添加条件到队列
                参数参见Filter属性
            '''
            _filter  = JsonCfg.Filter(subname,value)
            self.filters.append(_filter)

    
    def __compilecon__(self,con_str:str):
        '''条件处理
            把条件字符串分拆成条件对
            参数：
                条件字符串，格式举例：Node1_Name|AttrCon@A@value#AND#NodeCoN@value@@Node2_Name|AttrCon@value#AND#NodeCoN@value
            返回：
                条件映射：如正确解析，返回条件映射。当异常时为None，当条件串为空时为None
        '''
        dict_nodeflt = {}
        if con_str == "":
            info = ">> 条件为空[%s]" % con_str
            lg.myloger.error(info)
            return dict_nodeflt,info

        nodeftrs = con_str.split(self.__con_filter)
        for nodeftr in nodeftrs:
            ftrpair = nodeftr.split(self.__con_nodefilter)
            if len(ftrpair) != 2:
                info = ">> 条件[%s]格式错误：在[%s]处" % (con_str,nodeftr)
                lg.myloger.error(info)
                return None,info
            nodeflr_obj = JsonCfg.Node_Filter(ftrpair[0])
            fltstr = ftrpair[1]
            flts = fltstr.split(self.__con_and)
            for flt in flts:
                items = flt.split(self.__con_innerfilter)
                if len(items) != 3:
                    info = ">> 条件[%s]格式错误：在[%s]处" % (con_str,flt)
                    lg.myloger.error(info)
                    return None,info
                if items[0].upper() != "ATTRCON":
                    info = ">> 条件[%s]格式错误：在[%s]处出现不支持的条件类型[%s]" % (con_str,flt,items[1])
                    lg.myloger.error(info)
                    return None,info
                nodeflr_obj.addfilter(items[1], items[2])

            dict_nodeflt[ftrpair[0]] = nodeflr_obj

        return dict_nodeflt,""

    #读取xml项的值
    def readvalue(self, nodestr:str, filtstr:str, keystr:str, default = ""):  
        '''读取节点的属性值
            传入参数：
                nodestr：节点串，为"根节点@@子节点@@子节点@@...@@子节点"
                filtstr：配置条件串，格式为"Node1_Name|AttrCon@A@value#AND#NodeCoN@value@@Node2_Name|AttrCon@value#AND#NodeCoN@value"
                keystr：取值定义串，如取节点属性，格式为"AttrName";其中AttrName用实际属性名代替
            返回值：返回属性的取值或文本串，过程出错返回None，无法匹配返回缺省值
        '''
        stinfo = "开始读取json值，nodestr:%s, filtstr:%s, keystr:%s, default:%s" %(nodestr, filtstr, keystr, default)
        lg.myloger.info(stinfo)
        if not self.__hasfile:
            info = ">> 无此文件，请核对路径[%s]" % self.__cfgpath
            lg.myloger.error(info) 
            return False, info, ""

        temp_list = nodestr.split(self.__node_splitstr)
        dict_nodeflts = {}
        if filtstr != "":
            dict_nodeflts,info = self.__compilecon__(filtstr)
            if dict_nodeflts is None:
                return False, info, ""
        
        if len(temp_list) < 1:
            if len(dict_nodeflts) > 1:
                info = ">> 过滤条件[%s]格式化错误，请核对" % filtstr
                lg.myloger.error(info)
                return False,info,""
            else: 
                getted = False
                value = None
                if isinstance(self.__json,dict):
                    if keystr in currNode.keys():
                        value = self.__json[keystr]
                        getted = True
                    else:
                        info = "参数错误：设置节点不存在"
                else:
                    info = "参数错误：节点列表为空且根节点不是字典对象"

                if value is None and not default is None:
                        value = default
                        info = "未找到对应配置，用缺省值代替"
                        getted = True
                        lg.myloger.info("未找到对应配置，用缺省值代替")
                
                return getted,info,value
        else:
            currNode = self.__json
            count = len(temp_list)
            pos = 0
            while pos < count:
                nodeName = temp_list[pos]
                if isinstance(currNode,dict):
                    found = False
                    for key in currNode.keys():
                        if key == nodeName:
                            currNode = currNode[key]
                            if isinstance(currNode,dict):
                                pos = pos + 1
                            found = True
                            break;    
                    if not found:
                        info = "节点定位失败[%s]" % nodeName
                        lg.myloger.error(info) 
                        return False, info, ""
                elif isinstance(currNode,list) or isinstance(currNode, tuple):
                    flts = None
                    if nodeName in dict_nodeflts.keys():
                        flts = dict_nodeflts[nodeName]

                    found = True
                    for data in currNode:
                        if not flts is None and len(flts.filters) > 0:
                            for flt in flts.filters:
                                if data[flt.subobjname] != flt.subobjvalue:
                                    found = False
                                    break
                        if found:
                            currNode = data
                            if isinstance(currNode,dict):
                                pos = pos + 1
                            break
                    if not found:
                        info = "节点定位失败[%s]" % nodeName
                        lg.myloger.error(info) 
                        return False, info, ""
                if nodeName == temp_list[-1]:
                    value = None
                    if isinstance(currNode,dict):
                        if nodeName in currNode.keys():
                            value = currNode[keystr]
                        else:
                            info = "参数错误：目标节点[%s]在[%s]中不存在" %(nodestr,nodeName)
                            lg.myloger.error(info)
                    elif isinstance(currNode,list) or isinstance(currNode, tuple):
                        info = "in list,curr key is [%s]" % key
                        lg.myloger.info(info)

                        flts = None
                        if nodeName in dict_nodeflts.keys():
                            flts = dict_nodeflts[nodeName]
                        found = False
                        for data in currNode:
                            found = True
                            if not flts is None and len(flts.filters) > 0:
                                for flt in flts.filters:
                                    if data[flt.subobjname] != flt.subobjvalue:
                                        found = False
                                        break
                            if found:
                                if keystr in data.keys():
                                    value = data[keystr]
                                else:
                                    info = "参数错误：对象[%s]的无子对象[%s]" %(nodestr,keystr)
                                    lg.myloger.error(info)
                                break
                        
                        if not found:
                            info = "参数错误：无符合读取对象[%s]和条件[%s]的数据" %(nodestr,filtstr)
                            lg.myloger.error(info)
 
                    if value is None:
                        lg.myloger.info("未找到对应配置，用缺省值代替")
                        value = default
                    return True,"",value
    
    
    def setvalue(self, nodestr:str, filtstr:str, keystr:str, value:str):
        '''设置节点的属性值
            传入参数：
               nodestr：节点串，为"根节点@@子节点@@子节点@@...@@子节点"
                filtstr：配置条件串，格式为"Node1_Name|AttrCon@Attr_Name@value#AND#NodeCoN@_@value@@Node2_Name|AttrCon@Attr_Name@value#AND#NodeCoN@_@value"
                keystr：取值定义串，如取节点属性，格式为"AttrName";其中AttrName用实际属性名代替
                value：设置目标值
            返回值：设置成果则返回True，设置错误则返回False，参数错误返回None
            注意事项：本方法调用并未写文件，需随后调用写文件操作放可生效
        '''
        stinfo = "开始写入json值，nodestr:%s, filtstr:%s, keystr:%s, value:%s" %(nodestr, filtstr, keystr, value)
        lg.myloger.info(stinfo)

        info = ""
        if not self.__hasfile:
            info = ">> 无此文件，请核对路径[%s]" % self.__cfgpath
            lg.myloger.error(info)
            return False, info

        temp_list = nodestr.split(self.__node_splitstr)
        dict_nodeflts = {}
        if filtstr != "":
            dict_nodeflts,info = self.__compilecon__(filtstr)
            if dict_nodeflts is None:
                lg.myloger.error("过滤条件错误")
                return False, info

        setted = False
        if len(temp_list) < 1:
            if len(dict_nodeflts) > 1:
                info = ">> 过滤条件[%s]格式化错误，请核对" % filtstr
                lg.myloger.error(info)
                return False,info
            else:
                if isinstance(self.__json,dict):
                    if keystr in currNode.keys():
                        self.__json[keystr] = value
                        setted = True
                    else:
                        info = "参数错误：设置节点不存在"
                else:
                    info = "参数错误：节点列表为空且根节点不是字典对象"
        else:
            currNode = self.__json
            count = len(temp_list)
            pos = 0
            while pos < count:
                nodeName = temp_list[pos]
                if isinstance(currNode,dict):
                    found = False
                    for key in currNode.keys():
                        if key == nodeName:
                            currNode = currNode[key]
                            if isinstance(currNode,dict):
                                pos = pos + 1
                            found = True
                            break
                    if not found:
                        info = "节点定位失败[%s]" % nodeName
                        lg.myloger.error(info) 
                        return False, info
                elif isinstance(currNode,list) or isinstance(currNode, tuple):
                    flts = None
                    if nodeName in dict_nodeflts.keys():
                        flts = dict_nodeflts[nodeName]

                    found = True
                    for data in currNode:
                        if not flts is None and len(flts.filters) > 0:
                            for flt in flts.filters:
                                if data[flt.subobjname] != flt.subobjvalue:
                                    found = False
                                    break
                        if found:
                            currNode = data
                            if isinstance(currNode,dict):
                                pos = pos + 1
                            break
                    if not found:
                        info = "节点定位失败[%s]" % nodeName
                        lg.myloger.error(info) 
                        return False, info
                if nodeName == temp_list[-1]: #最后一个节点
                    if isinstance(currNode,dict):
                        currNode[keystr] = value
                        setted = True
                    elif isinstance(currNode,list) or isinstance(currNode, tuple):
                        flts = None
                        if nodeName in dict_nodeflts.keys():
                            flts = dict_nodeflts[nodeName]
                        found = False
                        for data in currNode:
                            found = True
                            if not flts is None and len(flts.filters) > 0:
                                for flt in flts.filters:
                                    if data[flt.subobjname] != flt.subobjvalue:
                                        found = False
                                        break
                            if found:
                                data[keystr] = value
                                setted = True
                                break
                        if not found:
                            info = "参数错误：无符合读取对象[%s]和条件[%s]的数据" %(nodestr,filtstr)
                            lg.myloger.error(info)
        return setted,info
        
    #写入配置文件    
    def save(self):
        with open(os.path.join(self.__cfgpath), 'w' ,encoding=self._encoding) as fh:
                json.dump(self.__json, fh,indent=4,ensure_ascii=False)