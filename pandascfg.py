import pandas as pd
import os
import logger as lg
from splitcfg import SplitSymbol

class PandasCfg:
    ''' 文件操作,支持(txt、csv、excel(xls/xlsx/xlsm)、json、剪切板、数据库、html、hdf、parquet、pickled文件、sas、stata)'''

    #条件元串并联连接符
    __con_and = "#AND#"
    __con_inner = "@"

    def __init__(self,cfgpath:str, encoding='utf-8'):
        '''构造函数
            功能：
                通过传入参数创建文件对象
            参数：
                cfgpath，文件的路径，建议为绝对路径
        '''
        self.__end = cfgpath.split(".")[-1].strip().lower()
        self.__cfgpath__ = cfgpath
        self.__encoding__ = encoding

    def readvalue(self, fields:str, fltstr:str, return_type:str, sheetname='',
                  file_type='', default=''):
        '''
        读取文件内容
        :输入参数：\n
        - fields 待读取的列，多列以“,”分隔，如果为空则读取全部列，按界面顺序输出
        - fltstr 检索命中条件，单个条件格式为“列名=值”，多个条件以“#AND#”连接，如果为空则无检索条件
        - sheetname 指定的sheet页
        - return_type  返回值类型
        - file_type 文件类型

        :输出参数：
        - status 读取状态，读取成功为True，读取失败为False
        - info   读取异常信息，成功为空串
        - data   表格数据信息， 失败为None，成功为一个二维列表，第一行为表头，顺序按照fields传入顺序排列，第二行开始为数据行

        :info异常信息说明：
        - 表格为空
        - 待读取的列不存在，属于输入参数错误，一般为带读取列不存在
        - 检索条件配置错误， 属于输入参数错误，一般为检索列不存在
        '''
        stinfo = "readvalue调用，cfgpath路径:%s fltstr检索条件:%s fields待读取的目标值:%s default缺省值:%s" % (self.__cfgpath__, fltstr, fields, default)
        # print(stinfo)
        lg.myloger.info(stinfo)
        if not os.path.isfile(self.__cfgpath__):
            self.__hasfile = False
            info = "参数错误：文件[%s]不存在" % self.__cfgpath__
            lg.myloger.error(info)
            return False, info, None

        need_field_list = []   #获取用户待读取的目标值列表
        if len(fields) > 0:
            need_field_list = fields.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","

        # 解析数据检索条件
        fltstr_field_list = []  # 条件表头信息
        fltstr_field_value_list = []  # 条件表头对应的值
        if len(fltstr) > 0 and fltstr != '_':
            fls = fltstr.split(SplitSymbol.SYMBOL_COMBINE_META)  # 筛选条件列表  "#AND#"
            for fl in fls:
                cond = fl.split(SplitSymbol.SYMBOL_COMPARE_EQUAL)  # "="
                if len(cond) != 2:
                    info = "配置错误：表格检索条件[%s]在[%s]出表达式错误" % (fltstr, fl)
                    return False, info, None
                fltstr_field_list.append(cond[0])
                fltstr_field_value_list.append(cond[1])

        if self.__end in ['xls', 'xlsx', 'xlsm'] or file_type in ['xls', 'xlsx', 'xlsm'] :  #读取excel文件，包括xlsx、xls、xlsm格式
            status, info, value = self.__readexcelV__(need_field_list, fltstr_field_list, fltstr_field_value_list,return_type,sheetname)
            return status, info, value
        elif self.__end in ['csv'] or file_type in  ['csv']:  #读取csv格式文件
            status, info, value = self.__readcsvV__(need_field_list, fltstr_field_list, fltstr_field_value_list,return_type,sheetname)
            return status, info, value
        elif self.__end in ['json'] or file_type in ['json']:  #读取json格式文件
            status, info, value = self.__readjsonV__(need_field_list, fltstr_field_list, fltstr_field_value_list,return_type)
            return status, info, value
        elif self.__end in ['txt'] or file_type in ['txt']:   #读取txt表格
            self.__readtxtV__()
        elif self.__end in ['html'] or file_type in ['html']:   #读取html表格
            self.__readhtmlV__()
        '''
        elif self.__end in ['cli']:   #读取剪切板内容
            self.__read_clipboard__()
        elif self.__end in ['pickle']:   #读取plckled持久化文件
            self.__read_pickle__()
        elif self.__end in ['sql']:   #读取数据库数据
            self.__read_sql__()
        elif self.__end in ['dhf']:   #读取hdf5文件
            self.__read_dhf__()
        elif self.__end in ['parquet']:   #读取parquet文件
            self.__read_parquet__()
        elif self.__end in ['sas']:   #读取sas文件
            self.__read_sas__()
        elif self.__end in ['gbq']:   #读取stata文件
            self.__read_gbq__()
        '''

    def setvalue(self, fltstr: str, attrname: str, value:str, sheetname='', file_type=''):
        '''
        读取文件内容
        :输入参数：\n
        - fltstr:检索条件，不能为空。多个条件需要使用"#AND#"隔开。示例：'OBJ_TABLEID@1071#AND#OBJ_ID@115020'
        - attrname：目标值的表头，不能为空。仅支持单个更改
        - value：目标值被更改后的数据，不能为空。仅支持单个更改
        - sheetname 指定的sheet页
        - file_type 文件类型

        :输出参数：
        - status 读取状态，读取成功为True，读取失败为False
        - info   读取异常信息，成功为空串
        - data   表格数据信息， 失败为None，成功为一个二维列表，第一行为表头，顺序按照fields传入顺序排列，第二行开始为数据行

        :info异常信息说明：
        - 表格为空
        - 待读取的列不存在，属于输入参数错误，一般为带读取列不存在
        - 检索条件配置错误， 属于输入参数错误，一般为检索列不存在
        '''
        print('####',fltstr, attrname, value, sheetname, file_type)
        stinfo = "readvalue调用，cfgpath路径:%s fltstr检索条件:%s attrname待更改的目标值:%s value更改后的值:%s" % (
        self.__cfgpath__, fltstr, attrname, value)
        lg.myloger.info(stinfo)

        # 判断条件信息
        flt_dict = {}  # 判断条件字典
        if len(fltstr) > 0 and fltstr != '_':
            fls = fltstr.split(SplitSymbol.SYMBOL_COMBINE_META)  # 筛选条件列表  "#AND#"
            for fl in fls:
                cond = fl.split(SplitSymbol.SYMBOL_COMPARE_EQUAL)  # "="
                if len(cond) != 2:
                    info = "配置错误：表格检索条件[%s]在[%s]出表达式错误" % (fltstr, fl)
                    return False, info, None
                flt_dict[cond[0]] = cond[1]
        # print(flt_dict)

        # 判断文件是否存在
        if not os.path.isfile(self.__cfgpath__):
            self.__hasfile = False
            info = "参数错误：文件[%s]不存在" % self.__cfgpath__
            lg.myloger.error(info)
            return False, info,''

        need_attrname_list = []  # 获取用户待更改的目标值列表
        if len(attrname) > 0:
            need_attrname_list = attrname.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","

        # 判断传入的值不为空
        need_value_list = []
        need_dict={}
        if not value:
            info = "更改后的键值为空：请检查"
            lg.myloger.error(stinfo)
            return False, info,''
        else:
            print(value)
            print(value[0])
            print(type(value))
            if value[0] == '[' and value[-1] == ']':
                if len(need_attrname_list) ==1:
                    need_dict[need_attrname_list[0]] = eval(value)
            else:
                need_value_list = value.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","
                if len(need_attrname_list) != len(need_value_list):
                    info = f"需要更改的键与值不一致，需要更改的键:{attrname}，需要更改的值:{value}"
                    lg.myloger.error(stinfo)
                    return False, info, ''
                else:
                    need_dict = dict(zip(need_attrname_list, need_value_list))
            print(need_value_list, type(need_value_list), len(need_value_list),need_dict)

        print(flt_dict, need_attrname_list, need_value_list)
        if self.__end in ['xls', 'xlsx', 'xlsm'] or file_type in ['xls', 'xlsx', 'xlsm']:  # 读取excel文件，包括xlsx、xls、xlsm格式
            pass
            # status, info, value = self.__setexcelV__(need_attrname_list, fltstr_field_list, fltstr_field_value_list,
            #                                         sheetname)
            # return status, info, value
        elif self.__end in ['csv'] or file_type in ['csv']:  # 读取csv格式文件
            status, info, value = self.__setcsvV__(flt_dict, need_attrname_list, need_value_list,need_dict)
            return status, info, value
        # elif self.__end in ['json'] or file_type in ['json']:  # 读取json格式文件
        #     status, info, value = self.__readjsonV__(need_field_list, fltstr_field_list, fltstr_field_value_list,
        #                                              return_type)
        #     return status, info, value
        # elif self.__end in ['txt'] or file_type in ['txt']:  # 读取txt表格
        #     self.__readtxtV__()
        # elif self.__end in ['html'] or file_type in ['html']:  # 读取html表格
        #     self.__readhtmlV__()

    def __readexcelV__(self, need_field_list, fltstr_field_list, fltstr_field_value_list,return_type,sheetname):
        '''
        读取excel文件内容
        - need_field_list 用户待读取的目标值列表
        - fltstr_field_list 条件表头信息
        - fltstr_field_value_list 条件表头对应的值
        - sheetname 指定的sheet页
        - return_type  返回值类型
        '''

        # stinfo = "__readexcelV__调用，用户待读取的目标值列表need_field_list:%s 条件表头信息fltstr_field_list:%s 条件表头对应的值fltstr_field_value_list:%s 返回值类型return_type:%s,指定的sheet页sheetname:%s" % (
        #     need_field_list, fltstr_field_list, fltstr_field_value_list, return_type, sheetname)
        # lg.myloger.info(stinfo)
        #获取整个文件信息
        excel_data = pd.read_excel(self.__cfgpath__, sheet_name=None)
        #获取文件全部的sheet页
        sheet_list = list(excel_data.keys())
        table_list_dict = []  # [{表头：数据},{表头：数据}]
        # print(excel_data[sheet_list[0]].to_dict(orient="records"))

        if sheetname == '':
            # 读取菜单数据(表头)
            thead_list = excel_data[sheet_list[0]].to_dict(orient="split")['columns']
            table_list_dict = excel_data[sheet_list[0]].to_dict(orient="records")  # 使用to_dict(orient="‘dict’, ‘list’, ‘series’, ‘split’, ‘records’, ‘index’")  records表示转换成我们需要的的列表嵌套字典结构
        else:
            if sheetname not in sheet_list:
                info = f"配置错误：表内没有对应的sheet页{sheetname}"
                return False, info, None
            else:
                # 读取菜单数据(表头)
                thead_list = excel_data[sheetname].to_dict(orient="split")['columns']
                table_list_dict = excel_data[sheetname].to_dict(orient="records")  # 使用to_dict(orient="‘dict’, ‘list’, ‘series’, ‘split’, ‘records’, ‘index’")  records表示转换成我们需要的的列表嵌套字典结构

        # 判断待读取的列是否存在
        if len(need_field_list) > 0 and need_field_list[0] != '_':
            for i in need_field_list:  # 获取读取列的索引号
                # print('这是i的值',i)
                # print(thead_list)
                if i not in thead_list:
                    info = f"配置错误:有列在表中未找到，表的列为{thead_list}"
                    return False, info, None
        status, info, data = self.__getdata__(need_field_list, fltstr_field_list, fltstr_field_value_list, thead_list, table_list_dict, return_type)
        return status, info, data

    # def __readcsvV__(self,  fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
    def __readcsvV__(self, need_field_list, fltstr_field_list, fltstr_field_value_list,return_type,sheetname):
        '''
        读取csv文件内容
        - need_field_list 用户待读取的目标值列表
        - fltstr_field_list 条件表头信息
        - fltstr_field_value_list 条件表头对应的值
        - sheetname 指定的sheet页
        - return_type  返回值类型
        '''

        #获取整个文件信息
        csv_data = pd.read_csv(self.__cfgpath__)

        table_list_dict = []  # [{表头：数据},{表头：数据}]
        # 读取菜单数据(表头)
        thead_list = csv_data.to_dict(orient="split")['columns']
        table_list_dict = csv_data.to_dict(orient="records")  # 使用to_dict(orient="‘dict’, ‘list’, ‘series’, ‘split’, ‘records’, ‘index’")  records表示转换成我们需要的的列表嵌套字典结构

        # 判断待读取的列是否存在
        if len(need_field_list) > 0 and need_field_list[0] != '_':
            for i in need_field_list:  # 获取读取列的索引号
                if i not in thead_list:
                    info = f"配置错误:有列在表中未找到，表的列为{thead_list}"
                    return False, info, None
        status, info, data = self.__getdata__(need_field_list, fltstr_field_list, fltstr_field_value_list, thead_list, table_list_dict, return_type)
        return status, info, data

    def __setcsvV__(self, flt_dict, need_attrname_list, need_value_list,need_dict={}):
        '''
        flt_dict:检索条件字典
        need_attrname_list：
        need_value_list：
        '''

        # print('flt_dict',flt_dict)
        # print('need_dict',need_dict)
        csv_data = pd.read_csv(self.__cfgpath__)
        self.__csv = csv_data.to_dict(orient="records")
        headers = csv_data.to_dict(orient="split")['columns']
        hangshu = len(self.__csv)
        # print(self.__csv)
        # print(headers)
        b = 0   #记录更改次数

        if flt_dict not in [{},'_']:  #判断条件是否为空-不为空则记录修改的行
            for rown,row in enumerate(self.__csv):
                ifchange = True
                # for i,j in enumerate(headers):
                #     if j in flt_dict.keys():
                for i in flt_dict.keys():
                    if i in headers:
                        if not isinstance(row[i],str):
                            row[i] = str(row[i])
                        if flt_dict[i] == row[i]:  # 如果输入的条件表头在文件内，且条件值和此行的数据一致。
                            pass
                        else:  # 如果输入的条件表头在文件内，但是条件值和此行的数据不一致，ifchange = False。说明此行不需要更改
                            ifchange = False
                    else:  # 如果输入的条件表头不在文件内
                        info = "条件不存在：条件[%s]不存在" % flt_dict
                        lg.myloger.error(info)
                        return False, info,""
                if ifchange == False:   #如果ifchange = False 说明此行不需要更改，则直接把此行信息添加到a列表
                    pass
                elif need_dict not in  [{},[],'_']:
                    for attrname, v in need_dict.items():
                        for i, j in enumerate(headers):
                            if j == attrname:
                                csv_data.iloc[rown, i] = v
                                b+=1
                else:
                    info = "需要更改的值不存在，请检查"
                    lg.myloger.error(info)
                    return False, info,""
        else:
            print('条件为空')
            for i,j in need_dict.items():
                print(i,j)
                try:
                    ix = eval(i)
                    print(type(ix), ix)
                    if isinstance(ix, int):
                        try:
                            print(f'这个j传入的是一个值类型type(j)，更改一行值是{j}')
                            csv_data.loc[ix] = j  # 更改/添加一行值
                            b += len(headers)
                        except Exception as e:
                            info = e
                            lg.myloger.error(info)
                            return False, info, ""
                    else:
                        info = f"请检查输入需要更改的信息{need_dict}"
                        lg.myloger.error(info)
                        return False, info, ""

                except:
                    print(type(i), i)
                    if isinstance(i, str):
                        try:
                            print(f'这个j传入的是一个值类型type(j)，更改一列值是{j}')
                            csv_data[i] = j  # 更改/添加一列值
                            b += hangshu
                        except Exception as e:
                            info = e
                            lg.myloger.error(info)
                            return False, info, ""

                    else:
                        info = f"请检查输入需要更改的信息{need_dict}"
                        lg.myloger.error(info)
                        return False, info, ""

        print('######',b)
        if b == 0:  # 如果更改次数为0，则返回失败信息
            info = f"文件没有任何更改：请检查条件信息: {flt_dict}"
            lg.myloger.error(info)
            return False, info, ""
        else:
            # csv_data.to_csv(r"D:\\davinciapi\\wen\\R11.csv", index=False, header=True)
            # csv_data = pd.read_csv(r"D:\\davinciapi\\wen\\R11.csv")
            # print(csv_data)
            csv_data.to_csv(self.__cfgpath__, index=False, header=True)
            info = f"有{b}处更改"
            lg.myloger.error(info)
        return True, info, ""

    def __readjsonV__(self, need_field_list, fltstr_field_list, fltstr_field_value_list,return_type):

        # pass
        # 读取菜单数据(表头)
        json_data = pd.read_json(self.__cfgpath__)
        table_list_dict = []  # [{表头：数据},{表头：数据}]
        # 读取菜单数据(表头)
        thead_list = json_data.to_dict(orient="split")['columns']
        table_list_dict = json_data.to_dict(
            orient="records")  # 使用to_dict(orient="‘dict’, ‘list’, ‘series’, ‘split’, ‘records’, ‘index’")  records表示转换成我们需要的的列表嵌套字典结构

        # 判断待读取的列是否存在
        if len(need_field_list) > 0 and need_field_list[0] != '_':
            for i in need_field_list:  # 获取读取列的索引号
                if i not in thead_list:
                    info = f"配置错误:有列在表中未找到，表的列为{thead_list}"
                    return False, info, None
        status, info, data = self.__getdata__(need_field_list, fltstr_field_list, fltstr_field_value_list, thead_list,
                                              table_list_dict, return_type)
        return status, info, data

    def __readtxtV__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __readhtmlV__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __read_clipboard__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass

        # 读取菜单数据(表头)

    def __read_pickle__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __read_sql__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __read_dhf__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __read_parquet__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __read_sas__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __read_gbq__(self, fltstr: str, fields: str, return_type='3', sheetname='Sheet1', default=''):
        pass
        # 读取菜单数据(表头)

    def __getdata__(self,need_field_list, fltstr_field_list, fltstr_field_value_list, thead_list, table_list_dict, return_type):
        '''
        读取excel文件内容
        - need_field_list 用户待读取的目标值列表
        - fltstr_field_list 条件表头信息
        - fltstr_field_value_list 条件表头对应的值
        - thead_list 文件表头信息
        - table_list_dict 文件全部数据，格式为列表嵌套字典
        - return_type  返回值类型
        '''

        stinfo = "__getdata__调用，用户待读取的目标值列表need_field_list:%s 条件表头信息fltstr_field_list:%s 条件表头对应的值fltstr_field_value_list:%s 返回值类型return_type:%s,文件表头信息thead_list:%s,文件全部内容table_list_dict:%s" % (
            need_field_list, fltstr_field_list, fltstr_field_value_list, return_type,thead_list,table_list_dict)
        lg.myloger.info(stinfo)

        # 判断过滤列是否存在
        table_dict = []  #得到过滤后的数据，格式为列表嵌套字典
        # print('全部的数据',table_list_dict)s
        if len(fltstr_field_list) > 0 and fltstr_field_list[0] != '_':  # 有判断条件
            for i in fltstr_field_list:
                if i not in thead_list:
                    info = "配置错误,不存在的条件选项"
                    return False, info, None
            if len(need_field_list) > 0 and need_field_list[0] != '_':  # 有判断条件且有目标值
                for l in table_list_dict:
                    tt = True
                    for zz in range(0, len(fltstr_field_value_list)):
                        if not isinstance(l[fltstr_field_list[zz]], str) or not isinstance(fltstr_field_value_list[zz],str):
                            l[fltstr_field_list[zz]] = str(l[fltstr_field_list[zz]])
                            fltstr_field_value_list[zz] = str(fltstr_field_value_list[zz])
                        if l[fltstr_field_list[zz]] != fltstr_field_value_list[zz]:
                            tt = False
                    if tt == True:
                        dic = {}
                        for z in need_field_list:
                            dic[z] = l[z]
                        table_dict.append(dic)
            else:  # 有判断条件 没有目标值
                for l in table_list_dict:
                    tt = True
                    for zz in range(0, len(fltstr_field_value_list)):
                        if not isinstance(l[fltstr_field_list[zz]], str) or not isinstance(fltstr_field_value_list[zz], str):
                            l[fltstr_field_list[zz]] = str(l[fltstr_field_list[zz]])
                            fltstr_field_value_list[zz] = str(fltstr_field_value_list[zz])
                        if l[fltstr_field_list[zz]] != fltstr_field_value_list[zz]:
                            tt = False
                    if tt == True:
                        table_dict.append(l)
        else:  # 没有判断条件 有目标值
            if len(need_field_list) > 0 and need_field_list[0] != '_':
                for l in table_list_dict:
                    dic = {}
                    for z in need_field_list:
                        dic[z] = l[z]
                    table_dict.append(dic)
            else:  # 没有判断条件 没有目标值
                table_dict = table_list_dict

        # print('table_dict的值:',table_dict)

        # 根基return_type返回对应的数据类型
        if return_type not in ['4', '5', '6', 4, 5, 6]:  # list
            tb_list = []
            for tb in table_dict:
                tb_list.append(list(tb.values()))
            if len(tb_list) == 1:
                tb_list = tb_list[0]
            return True, "", tb_list
        elif return_type in [4, "4"]:  # str
            tb_list = []
            for tb in table_dict:
                for i in list(tb.values()):
                    tb_list.append(str(i))
            tb_list_str = ",".join(tb_list)
            return True, "", tb_list_str
        elif return_type in [5, "5"]:  # list-dict
            return True, "", table_dict
        elif return_type in [6, "6"]:  # (True, '', [['key1', 'key2'], ['v1', 'v2']])
            tb_list = []
            for i in range(0, len(table_dict)):
                if i == 0:
                    tb_list.append(list(table_dict[i].keys()))
                tb_list.append(list(table_dict[i].values()))
            return True, "", tb_list
        else:
            return False, "请输入对应的返回类型", []









# excel_data = pd.read_excel(r"D:\davinciapi\wen\龙头风电场_受阻电量(机头风速法)月报2021-10到2022-04.xls")# ,engine='xlrd', skiprows=3, usecols="C:F", index_col=None, sheet_name = 0, dtype = {"ID":str, "InStore":str})
# # excel_data2 = pd.read_excel(r"D:\davinciapi\wen\龙头风电场_受阻电量(机头风速法)月报2021-10到2022-04.xlsx")
# # excel_data2 = pd.read_excel(r"D:\davinciapi\wen\RTDBTHEORYPDATA.xls",engine='xlrd', skiprows=3, usecols="C:F", index_col=None, sheet_name = 0, dtype = {"ID":str, "InStore":str})
# csv_data = pd.read_csv(r"D:\davinciapi\wen\RTDBTHEORYPDATA.csv")
# txt_data = pd.read_table(r"D:\davinciapi\wen\RTDBTHEORYPDATA.txt")
# # json_data = pd.read_json(r"D:\davinciapi\wen\RTDBTHEORYPDATA.json")
# # print("excel数据", os.linesep, excel_data)
# # print("excel数据", os.linesep, excel_data2)
# # print("csv数据", os.linesep, csv_data)
# # print("txt数据", os.linesep, txt_data)
# # print("json数据", os.linesep, json_data)
# data1 = excel_data.to_dict(orient="records")
# data10 = excel_data.to_dict(orient="list")
# data2 = csv_data.to_dict(orient="dict")
# data3 = txt_data.to_dict(orient="series")
# # data4 = json_data.to_dict(orient="records")
# print(data1)
# print(data10)
# print(data2)
# print(data3)

if __name__ == '__main__':
    # #测试xls类型文件读取
    # 获取全部信息
    paras = [r"C:\Users\Administrator\Downloads\测试风电厂_风电场风速2022-07-15到2022-07-16.xls", '气象预报风速,Unnamed: 8,Unnamed: 9', '日期=2022-07-15','3']
    # 获取单个具体的值
    # paras = [r"D:\\davinciapi\\wen\\测试风电厂_测风塔_1_1层_20220705-20220706.xls", '风速(m/s)', '日期=2022-07-05 00:00:00','3']
    # 取多个具体的值
    # paras = [r"D:\\davinciapi\\wen\\江苏协鑫鑫日光伏电站_环境监测仪_1_温度优化_20220512.xls", '实际气象站温度,优化气象站温度', '日期=2022-05-12#AND#时间=00:00','4']
    # 获取行值
    # paras = [r"D:\\davinciapi\\wen\\江苏协鑫鑫日光伏电站_环境监测仪_1_温度优化_20220512.xls", '_', '时间=00:00','3']
    # 取列的值
    # paras = [r"D:\\davinciapi\\wen\\江苏协鑫鑫日光伏电站_环境监测仪_1_温度优化_20220512.xls", '实际气象站温度', '_','3']
    # #
    a = PandasCfg(paras[0])
    status, info, value = a.readvalue(paras[1],paras[2],paras[3])
    print(status, info, value)
    #
    # paras = [r"D:\\davinciapi\\wen\\江苏协鑫鑫日光伏电站_环境监测仪_1_温度优化_20220512.xls", '日期=2022-05-12#AND#时间=00:00', '实际气象站温度', '123']
    # a = PandasCfg(paras[0])
    # status, info, value = a.setvalue(paras[1],paras[2],paras[3])
    # print(status, info, value)

    # #测试csv文件的读取
    # 获取全部信息
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', '_', '']
    # 获取单个具体的值
    # paras = [r"D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv", 'OBJ_ID', 'ID=3#AND#OBJ_TABLEID=107132']
    # 取多个具体的值
    # paras = [r"D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv", 'OBJ_ID,THEORYP', 'ID=3#AND#OBJ_TABLEID=107132']
    # 获取行值
    # paras = [r"D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv", '_', 'ID=123']
    # 取列的值
    # paras = [r"D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv", 'OBJ_ID', '_']
    # cc = PandasCfg(paras[0])
    # status, info, value = cc.readvalue(paras[1], paras[2])
    # print(status, info, value)

    #只有一行数据满足条件，只更改一个值
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', 'ID=3#AND#OBJ_TABLEID=107132', 'OBJ_ID','y115020']
    # 只有一行数据满足条件，更改多个值
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', 'ID=3#AND#OBJ_TABLEID=107132', 'OBJ_ID,FCST_NODETYPE', 'y123,y456']
    # 有多行数据满足条件，更改多个值
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', 'ID=3', 'OBJ_ID,OBJ_TABLEID','y123,y456']

    # 无条件，更改多列值
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', 'OBJ_ID', 'y123']
    # 无条件，更改多列值
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', 'OBJ_ID,OBJ_TABLEID', 'y123,y456']
    # 无条件，新增一列值，且每个值都一样-str
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', 'xx', 'gxxgg']
    # 无条件，新增一列值，且每个值都一样-int
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', 'xx', '1112345']
    # 无条件，新增一列值，且每个值都不样list
    # paras = [r'D:\davinciapi\wen\aa\RTDBTHEORYPDATA.csv', '_', 'xx', '[1,2,3]']
    # 无条件，新增多列值，类型组合--不支持
    # paras = [r'D:\davinciapi\wen\aa\RTDBTHEORYPDATA.csv', '_', 'x,y,z', 'gxxgg,1112345,[1,2,3]']

    # 无条件，更改一行值
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', '0', '123']
    # 无条件，更改多行值
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', '0,1', 'y123,y456']
    # 无条件，新增多列值，且每个值都一样-str
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', '4', 'gxxgg']
    # 无条件，新增多列值，且每个值都一样-int
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', '_', '4', '1112345']
    # 无条件，新增多列值，且每个值都不样list
    # paras = [r'D:\davinciapi\wen\aa\RTDBTHEORYPDATA.csv', '_', '4', '[1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,3,1,2,3]']
    # 无条件，新增多列值，类型组合--不支持
    # paras = [r'D:\davinciapi\wen\aa\RTDBTHEORYPDATA.csv', '_', '3,4,5', 'gxxgg,1112345,[1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3,3,1,2,3]']
    # paras = [r'D:\\davinciapi\\wen\\aa\\RTDBTHEORYPDATA.csv', 'ID=3#AND#OBJ_TABLEID=107132', 'OBJ_ID,FCST_NODETYPE','123,5']
    # a = PandasCfg(paras[0])
    # print('@@@@',paras[1], paras[2], paras[3])
    # status, info, value = a.setvalue(paras[1], paras[2], paras[3])
    # print(status, info, value)

    # pass
    #测试规范json文件的读取
    # 获取全部信息
    # paras = [r'D:\\davinciapi\\wen\\aa\\data.json', '_', '_', '']
    #获取单个具体的值
    # paras = [r'D:\\davinciapi\\wen\\aa\\data.json', 'Duration', 'Pulse=110', '']
    #取多个具体的值
    # paras = [r'D:\\davinciapi\\wen\\aa\\data.json', 'Duration,Maxpulse', 'Pulse=110#AND#Calories=409.1', '']
    #获取行值
    # paras = [r"D:\\davinciapi\\wen\\aa\\data.json", '_', 'Pulse=110#AND#Calories=409.1']
    #取列的值
    paras = [r"D:\\davinciapi\\wen\\aa\\data.json", 'Duration', '_']
    cc = PandasCfg(paras[0])
    status, info, value = cc.readvalue(paras[1], paras[2])
    print(status, info, value)

# try:
#     jx = eval(j)
#     if isinstance(jx, list) and len(jx) == len(headers):
#         csv_data.loc[ix] = jx  # 更改/添加一行值
#         b += len(headers)
#     elif isinstance(jx, int):
#         csv_data.loc[ix] = jx  # 更改/添加一行值
#         b += len(headers)
#     else:
#         info = f"添加行数据个数与表头(列数)不一致，输入的行信息为：{j},实际表头信息为：{headers}"
#         lg.myloger.error(info)
#         return False, info, ""
# except:
#     csv_data.loc[ix] = j  # 更改/添加一行值
#     b += len(headers)

