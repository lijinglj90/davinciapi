import csv
import os
import logger as lg
import chardet

class CsvCfg:
    ''' Csv文件操作'''

    #条件元串并联连接符
    __con_and = "#AND#"
    __con_inner = "@"

    def __init__(self,cfgpath:str, encoding=''):
        '''构造函数
            功能：
                通过传入参数创建csv对象
            参数：
                cfgpath，文件的路径，建议为绝对路径
        '''
        self.__cfgpath = cfgpath
        get_encoding = self.get_encoding(self.__cfgpath)
        if encoding: #用户指定编码格式  encoding不为空
            self.__encoding = encoding   #使用用户指定编码格式
        else:   #用户没有指定编码格式
            if get_encoding:  #程序自动获取文件编码格式，不为空
                self.__encoding = get_encoding  #使用程序获取的编码格式
            else:
                self.__encoding = 'utf-8' #给一个默认值

 
    def readvalue(self,fltstr:str,attrname:str,default:str):
        '''
        fltstr:检索条件，不能为空。多个条件需要使用"#AND#"隔开。示例：'OBJ_TABLEID@1071#AND#OBJ_ID@115020'
        attrname：目标值的表头，不能为空。仅支持单个查询
        default：缺省值
        '''
        stinfo = "readvalue调用，cfgpath:%s fltstr:%s attrname:%s default:%s" %(self.__cfgpath, fltstr,attrname, default)
        lg.myloger.info(stinfo)

        if not os.path.isfile(self.__cfgpath):
                self.__hasfile = False
                info = "参数错误：csv文件[%s]不存在" %self.__cfgpath
                lg.myloger.error(info)
                return False, info, None
        else:
            self.__hasfile = True
            with open(self.__cfgpath, 'r',encoding=self.__encoding) as f:
                self.__csv = csv.reader(f)
                flts = fltstr.split(self.__con_and)
                if len(flts) < 1:
                    info  = "条件错误：条件为空"
                    lg.myloger.error(info)
                    return False, info, None
                flt_dict = {}
                for flt in flts: #解析条件列
                    temp = flt.split(self.__con_inner)
                    if len(temp) != 2:
                        info = "条件错误：条件[%s]格式错误" % flt
                        lg.myloger.error(info)
                        return False, info, None
                    flt_dict[temp[0]] = temp[1]
                #print(flt_dict)
                header = next(self.__csv)
                col_dict = {}
                index = 0
                findflts = 0
                foundattr = False
                for col in header: #获取条件列和取值列索引
                    if col == attrname:
                        col_dict[attrname] = index
                        foundattr = True
                    elif col in flt_dict:
                        col_dict[col] = index
                        findflts += 1
                    else:
                        pass
                    
                    index += 1
                
                #print(col_dict)
                
                found = True
                if not foundattr: #判断取值列是否存在
                    info = "条件错误：取值列[%s]不存在" % attrname
                    lg.myloger.error(info)
                    found = False
                
                if  findflts != len(flt_dict): #判断条件列是否都存在
                    info = "条件错误：条件[%s]有属性列不存在" % fltstr
                    lg.myloger.error(info)
                    found = False
                
                if not found:
                    return False,info,None
                else:
                    for row in self.__csv:
                        #print(row)
                        getted = True
                        for flt in flt_dict:
                            if row[col_dict[flt]] != flt_dict[flt]:
                                getted = False
                                break
                        if getted:
                            return True,"",row[col_dict[attrname]]
                    lg.myloger.info("未找到，返回缺省值")
                    return default
            return None

    def setvalue_old(self,fltstr:str,attrname:str,value):
        stinfo = "setvalue调用，cfgpath:%s fltstr:%s attrname:%s value:%s" %(self.__cfgpath, fltstr,attrname, value)
        lg.myloger.info(stinfo)

        if not os.path.isfile(self.__cfgpath):
                self.__hasfile = False
                info= "参数错误：csv文件[%s]不存在" %self.__cfgpath
                lg.myloger.error(stinfo)
                return False, info
        else:
            self.__hasfile = True
            with open(self.__cfgpath, 'r',encoding=self.__encoding) as f:
                self.__csv = csv.reader(f)
                flts = fltstr.split(self.__con_and)
                if len(flts) < 1:
                    info = "条件错误：条件为空"
                    lg.myloger.error(stinfo)
                    return False, info
                flt_dict = {}
                for flt in flts: #解析条件列
                    temp = flt.split(self.__con_inner)
                    if len(temp) != 2:
                        info = "条件错误：条件[%s]格式错误" % flt
                        lg.myloger.error(stinfo)
                        return False, info
                    flt_dict[temp[0]] = temp[1]

                header = next(self.__csv)
                col_dict = {}
                index = 0
                findflts = 0
                foundattr = False
                for col in header: #获取条件列和取值列索引
                    if col == attrname:
                        col_dict[attrname] = index
                        foundattr = True
                    elif col in flt_dict:
                        col_dict[col] = index
                        findflts += 1
                    else:
                        pass
                    
                    index += 1
                found = True
                if not foundattr: #判断取值列是否存在
                    info = "条件错误：取值列[%s]不存在" % attrname
                    lg.myloger.error(stinfo)
                    found = False
                
                if  findflts != len(flt_dict): #判断条件列是否都存在
                    info = "条件错误：条件[%s]有属性列不存在" % fltstr
                    lg.myloger.error(stinfo)
                    found = False
                
                if not found:
                    return False,info
                else:
                    fw = open (self.__cfgpath+"temp", 'w')
                    csvwriter = csv.writer(fw)
                    setted = False
                    csvwriter.writerow(header)
                    for row in self.__csv:
                        getted = True
                        for flt in flt_dict:
                            if row[col_dict[flt]] != flt_dict[flt]:
                                getted = False
                                break
                        if getted:
                            row[col_dict[attrname]] = value
                            setted = True
                        csvwriter.writerow(row)
                    fw.close()
                    f.close()
                    if setted:
                        os.remove(self.__cfgpath)
                        os.rename(self.__cfgpath+"temp", self.__cfgpath)
                        lg.myloger.info("设置参数成功")
                        return True,""
                    else:
                        os.remove(self.__cfgpath+"temp")
                        info = "设置参数失败"
                        lg.myloger.error(info)
                        return False,info
            return None

    def get_encoding(self,cfgpath):
        # 二进制方式读取，获取字节数据，检测类型
        with open(cfgpath, 'rb') as f:
            data = f.read()
            return chardet.detect(data)['encoding']

    def setvalue(self, fltstr: str, attrname: str, value):   #1041,1011
        '''
        fltstr:检索条件，不能为空。多个条件需要使用"#AND#"隔开。示例：'OBJ_TABLEID@1071#AND#OBJ_ID@115020'
        attrname：目标值的表头，不能为空。仅支持单个更改
        value：目标值被更改后的数据，不能为空。仅支持单个更改
        '''
        stinfo = "setvalue调用，cfgpath:%s fltstr:%s attrname:%s value:%s" % (self.__cfgpath, fltstr, attrname, value)
        lg.myloger.info(stinfo)

        #判断条件信息
        flts = fltstr.split(self.__con_and)
        if len(flts) < 1:  # 判断条件是否为空
            info = "条件错误：条件为空"
            lg.myloger.error(stinfo)
            return False, info
        flt_dict = {}  # 判断条件字典
        for flt in flts:  # 解析条件列
            temp = flt.split(self.__con_inner)
            if len(temp) != 2:
                info = "条件错误：条件[%s]格式错误" % flt
                lg.myloger.error(stinfo)
                return False, info
            flt_dict[temp[0]] = temp[1]
        # print(flt_dict)

        #判断传入的值不为空
        if not value :
            info = "更改后的键值为空：请检查"
            lg.myloger.error(stinfo)
            return False, info

        #判断文件是否存在
        if not os.path.isfile(self.__cfgpath):
            self.__hasfile = False
            info = "参数错误：csv文件[%s]不存在" % self.__cfgpath
            lg.myloger.error(info)
            return False, info
        else:
            self.__hasfile = True
            a = []  #需要写入的信息
            headers = []  # 表头信息
            with open(self.__cfgpath, 'r+',encoding=self.__encoding)as f:   #只读方式打开文件
                self.__csv = csv.DictReader(f)  #将读取的信息映射为字典
                b = 0   #记录更改次数
                for row in self.__csv:
                    row1 = dict(row)    #每一行都是字典格式
                    headers = list(row1.keys())
                    ifchange = True
                    for i in flt_dict.keys():
                        if i in headers:
                            if flt_dict[i] == row1[i]:     #如果输入的条件表头在文件内，且条件值和此行的数据一致。
                                # print(i)
                                # print(row1[i])
                                pass
                            else:  #如果输入的条件表头在文件内，但是条件值和此行的数据不一致，ifchange = False。说明此行不需要更改
                                ifchange = False
                        else:  #如果输入的条件表头不在文件内
                            info = "条件不存在：条件[%s]不存在" % flt
                            lg.myloger.error(info)
                            return False, info
                    if ifchange == False:   #如果ifchange = False 说明此行不需要更改，则直接把此行信息添加到a列表
                        a.append(row1)
                    elif attrname and attrname in headers:   #如果ifchange = True，且attrname目标表头不为空，且目标表头在文件内。则把此行的值改掉。记录更改次数+1
                        row1[attrname] = value
                        b += 1
                        a.append(row1)
                    else:
                        info = "需要更改的值不存在，请检查"
                        lg.myloger.error(info)
                        return False, info
            # print('@@@@',headers)
            # print(a)
            # print(b)

            if b==0:  #如果更改次数为0，则返回失败信息
                info = f"文件没有任何更改：请检查条件信息: {fltstr}"
                lg.myloger.error(info)
                return False, info
            else:
                with open(self.__cfgpath, 'w', newline='',encoding=self.__encoding)as f:
                    f_csv = csv.DictWriter(f, fieldnames=headers)   #DictWriter按照字典格式写入
                    f_csv.writeheader()
                    f_csv.writerows(a)
                    info = f"有{b}处更改"
                    lg.myloger.error(info)
                return True, ""


# if __name__ == '__main__':
#     pass
#     #读
#     paras = [r'D:\\davinciapi\\aa\\RTDBTHEORYPDATA.csv', 'ID@2#AND#OBJ_TABLEID@1071', 'OBJ_ID','']
#     cc = CsvCfg(paras[0])
#     status, info, value = cc.readvalue(paras[1], paras[2], paras[3])
#     print(status, info, value)
#     ls = []
    # if not status is None:
    #     ls.append(value)
    # print(ls)

    # 写
    # paras = [r'D:\davinciapi\wen\aa\RTDBTHEORYPDATA.csv', 'OBJ_TABLEID@1071#AND#OBJ_ID@115020', 'ID',
    #          '123']
    # cc = CsvCfg(paras[0])
    # value = cc.setvalue(paras[1], paras[2], paras[3])
    # print(value)