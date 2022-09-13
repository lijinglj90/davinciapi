#coding:utf-8

'''
    davinci平台实时库访问接口
        通过http接口与davinci平台的实时库接口进行数据交互，实现实时库的数据读取和修改
'''
import json
import requests
from splitcfg import SplitSymbol

class RtdbCfg():
    def __init__(self,ip:str,port:str):
        self.__ip = ip
        self.__port = port
        self.__getfunc = "get_value_from_table"
        self.__setfunc = "set_value_for_table2field"

    def readvalue(self,tableid:int,recordids:str,fields:str,conditions=str):
        '''
            读取实时库数据
            :输入参数:
            - tableid       实时库表id，整数型数据
            - recordids     读取指定记录id，多个以","分隔，空为不以id做检索条件
            - fields        读取列名称，多列用","分隔，空为读取全部列
            - conditions    检索条件，格式为"属性名@比较符@值"，多个条件以"#AND#"连接，比较符如下:\n
                            "=="，">"，"<",">=","<=","!="和"in"

            :输出参数:
            - status        读取是否成功操作状态，如果不成功，出错信息写在info中
            - info          出错信息
            - data          返回数据。数据为一个二维list，数据第一行为属性名，从第二行起为数据
        '''
        print('传入条件参数为：','tableid:',tableid,'recordids:',recordids,'fields:',fields,'conditions:',conditions)
        url = "http://%s:%s/rtdb/%s" %(self.__ip,self.__port,self.__getfunc)
        para = {}

        if tableid <=0:
            return False,"tableid错误",None
        para["tableId"] = tableid

        if recordids in ['', '_']:
            ls_re_int = []
        else:
            ls_re = recordids.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","
            ls_re_int = list(map(lambda x: int(x),ls_re))
        para["recordId"] = ls_re_int

        if fields in ['','_']:
            ls_fld = []
        else:
            ls_fld = fields.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)
        para["fieldName"] = ls_fld

        if conditions in ['','_']:
            condition = []
        else:
            status, info, condition = self.__format_conditions__(conditions)
            if status == False:
                return status, info, None
        para["condition"] = condition


        header = {}
        header["para"] = json.dumps(para)
        header_json = header
        print('传入参数:','url:',url,'header:',header,)
        
        res  = requests.get(url,headers=header_json)
        status = False
        info = ""
        data = None
        if res.status_code == 200:
            # r_info = json.loads(res.content)
            r_info = res.json()
            # if r_info["status"] is True:
            if r_info['statusMsg'] == 'successfully.':
                data = r_info["data"]
                # data.insert(0,r_info["fieldName"])
                status =  True
            else:
                info = "实时库查询失败，返回信息:[%s]" %(r_info["statusMsg"])
        else:
            info = "http请求错误：错误代码为[%d]" %(res.status_code)

        print(status, info, data)
        return status,info,data

    
    def setvalue(self,tableid:int,recordids:str,fields:str,values:str,conditions=str):
        '''
            修改实时库数据
            :输入参数:
            - tableid       实时库表id，整数型数据
            - recordids     指定记录id，多个以","分隔，空为不以id做检索条件
            - fields        待修改列名称，多列用","分隔，空为读取全部列
            - values        待修改列数据值，和fields一一对应
            - conditions    检索条件，格式为"属性名@比较符@值"，多个条件以"#AND#"连接，比较符如下:\n
                            "=="，">"，"<",">=","<=","!="和"in"

            :输出参数:
            - status        读取是否成功操作状态，如果不成功，出错信息写在info中
            - info          出错信息
            - data          None
        '''
        # print(tableid,recordids,fields,values,conditions)
        url = "http://%s:%s/rtdb/%s" %(self.__ip,self.__port,self.__setfunc)
        para = {}
        if tableid <=0:
            return False,"tableid错误"
        para["tableId"] = tableid

        if recordids in ['', '_']:
            ls_re_int = []
        else:
            ls_re = recordids.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)
            ls_re_int = list(map(lambda x: int(x),ls_re))
        para["recordId"] = ls_re_int

        if fields in ['', '_'] or values in ['', '_']:
            info = 'fields-修改目标字段名 和 values-目标字段值 两个不能为空'
            return False, info
        else:
            ls_fld = fields.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)
            para["fieldName"] = ls_fld
            ls_fldV = values.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)
            para["fieldValue"] = ls_fldV

        if conditions in ['','_']:
            condition = []
        else:
            status,info,condition = self.__format_conditions__(conditions)
            if status == False:
                return status,info
        para["condition"] = condition

        body ={}
        body["para"] = para
        print('传入参数: url:',url,type(body),body)
        res = requests.post(url, json=body)
        status = False
        info = ""
        if res.status_code == 200:
            # r_info = json.loads(res.content)
            r_info = res.json()
            # if r_info["status"] is True:
            if r_info['statusMsg'] == 'successfully.':
                status = True
            else:
                info = "修改失败实时库表[%d]，返回信息:[%s]" %(tableid,r_info["statusMsg"])
        else:
            info = "http请求错误：错误代码为[%d]" %(res.status_code)

        print(status, info)
        return status,info

    def delvalue(self,tableid:int,recordids:str):
        '''
            修改实时库数据
            :输入参数:
            - tableid       实时库表id，整数型数据
            - recordids     指定记录id，多个以","分隔，空为不以id做检索条件
            - fields        待修改列名称，为空[]
            - values        待修改列数据值，为空[]
            - conditions    检索条件，为空[]

            :输出参数:
            - status        读取是否成功操作状态，如果不成功，出错信息写在info中
            - info          出错信息
            - data          None
        '''
        # print(tableid,recordids,fields,values,conditions)
        url = "http://%s:%s/rtdb/%s" %(self.__ip,self.__port,self.__setfunc)
        para = {}
        if tableid <=0:
            return False,"tableid错误"
        para["tableId"] = tableid

        if recordids in ['', '_']:
            ls_re_int = []
        else:
            ls_re = recordids.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)
            ls_re_int = list(map(lambda x: int(x),ls_re))
        para["recordId"] = ls_re_int

        para["fieldName"] = []
        para["fieldValue"] = []
        para["condition"] = []

        body ={}
        body["para"] = para
        print('传入参数: url:',url,type(body),body)
        res = requests.post(url, json=body)
        status = False
        info = ""
        if res.status_code == 200:
            r_info = res.json()
            if r_info['statusMsg'] == 'successfully.':
                status = True
            else:
                info = "修改失败实时库表[%d]，返回信息:[%s]" %(tableid,r_info["statusMsg"])
        else:
            info = "http请求错误：错误代码为[%d]" %(res.status_code)

        print(status, info)
        return status,info


    def __format_conditions__(self,conditions_str:str):
        '''
            解析条件字符串
            :输入参数:
            - conditions    检索条件，格式为"属性名@比较符@值"，多个条件以"#AND#"连接，比较符如下:\n
                            "=="，">"，"<",">=","<=","!="和"in"

            :输出参数:
            - status        解析是否成功操作状态，如果不成功，出错信息写在info中
            - info          出错信息
            - data          输出一个条件list，元素为一个包含列名、判断符和值的元组
        '''
        print('__format_conditions__传入参数：',conditions_str)
        condition = []
        #条件元串连接符
        con_innerfilter=SplitSymbol.SYMBOL_BETWEEN_ELEMENTS_IN_CONDITION   #"@"

        #条件元串并联连接符
        con_and = SplitSymbol.SYMBOL_COMBINE_META   #"#AND#"

        cons = conditions_str.split(con_and)
        for con in cons:
            items = con.split(con_innerfilter)
            if len(items) != 3:
                info = "条件[%s]格式错误:在[%s]处条件表达式不完整" % (conditions_str,con)
                return False, info, None
            else:
                con_item = {}
                con_item["field"] = items[0]
                con_item["cond"] = items[1]
                con_item["val"] = items[2]
                condition.append(con_item)
        print(condition)
        return True, "",condition