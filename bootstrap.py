from splitcfg import SplitSymbol
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
import logger as lg


def getdata_from_bootstrapp_table(el,fields:str="",filter:str=""):
    '''
        读取表格元素的值
        :输入参数：\n
        - el     指定读取的表格元素，此处为做类型判断，如传入其他元素可能会产生意想不到的错误
        - fields 待读取的列，多列以“,”分隔，如果为空则读取全部列，按界面顺序输出
        - filter 检索命中条件，单个条件格式为“列名=值”，多个条件以“##”连接，如果为空则无检索条件
        
        :输出参数：
        - status 读取状态，读取成功为True，读取失败为False
        - info   读取异常信息，成功为空串
        - data   表格数据信息， 失败为None，成功为一个二维列表，第一行为表头，顺序按照fields传入顺序排列，第二行开始为数据行
        
        :info异常信息说明：
        - 表格为空
        - 待读取的列不存在，属于输入参数错误，一般为带读取列不存在
        - 检索条件配置错误， 属于输入参数错误，一般为检索列不存在
    '''
    # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
    
    table_list = []  #存放table数据
    header_list = []

    need_field_list = []
    #获取待读取数据列
    if len(fields) > 0:
        need_field_list = fields.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)

    filter_field_list = []
    filter_field_value_list =[]
    filter_fieldindex_list = []


    #解析数据检索条件
    if len(filter) > 0:
        fls = filter.split(SplitSymbol.SYMBOL_BETWEEN_ELEMENTS_IN_CONDITION)
        for fl in fls:
            cond = fl.split(SplitSymbol.SYMBOL_COMPARE_EQUAL)
            if len(cond) != 2:
                info = "配置错误：表格检索条件[%s]在[%s]出表达式错误" %(filter,fl)
                return False,info,None
            filter_field_list.append(cond[0])
            filter_field_value_list.append(cond[1])
    field_Order = []

    #读取表头
    thead = el.find_elements("tag name", "thead")
    table_tr_list = thead[0].find_elements("tag name", "tr")
    table_td_list = table_tr_list[0].find_elements("tag name", "th")
    for td in table_td_list:    #遍历每一个td
        div = td.find_elements("tag name","div")
        header_list.append(div[0].get_attribute("innerText"))
    
    #判断过待读取列是否存在
    if len(need_field_list) == 0:
        #table_list.append(header_list)  #由于界面列名均为中文，无法和数据库匹配，暂不带
        pass
    else:
        try:
            for i in range(0,len(need_field_list)):#获取读取列的索引号
                index = header_list.index(need_field_list[i])
                field_Order.append(index)
            #table_list.append(need_field_list)
        except ValueError:
            info = "配置错误:读取列[%s]有列在表中未找到，表的列为[%s]" %(fields,table_td_list)
            return False,info,None

    #判断过滤列是否存在
    try:
        for i in range(0,len(filter_field_list)):#读取检索列的索引号
            index =   header_list.index(filter_field_list[i])
            filter_fieldindex_list.append(index)
    except ValueError:
        info = "配置错误:过滤条件[%s]有列在表中未找到，表的列为[%s]" %(filter,table_td_list)
        return False,info,None

    #读取数据
    tbody = el.find_elements("tag name", "tbody")
    table_tr_list = tbody[0].find_elements("tag name", "tr")
    for tr in table_tr_list:    #遍历每一个数据行（tr）
        #将每一个tr的数据根据td查询出来，返回结果为list对象
        table_td_list = tr.find_elements("tag name", "td")
        if len(table_td_list) == 0:
            break
        is_filter = True
        for i in range(0,len(filter_fieldindex_list)):
            index = filter_field_value_list[i]
            if table_td_list[index].text != filter_field_value_list[i]:
                is_filter = False
                break
        if is_filter is True:
            row_list = []
            if len(field_Order) == 0:
                for i in range(0,len(table_td_list)):
                    row_list.append(table_td_list[i].text)
            else:
                for i in range(0,len(field_Order)):
                    index = field_Order[i]
                    row_list.append(table_td_list[index].text)
            table_list.append(row_list)

    # if len(table_list) == 1:
    #     table_list = table_list[0]
    return True,"",table_list

def getdata_from_bootstrapp_table_tubiao(el, driver:WebDriver, fields: str = "", filter: str = "", return_type: str = ""):  # (el对象，‘’，‘’)
    '''
        读取表格元素的值
        :输入参数：\n
        - el     指定读取的表格元素，此处为做类型判断，如传入其他元素可能会产生意想不到的错误
        - fields 待读取的列，多列以“,”分隔，如果为空则读取全部列，按界面顺序输出
        - filter 检索命中条件，单个条件格式为“列名=值”，多个条件以“#AND#”连接，如果为空则无检索条件

        :输出参数：
        - status 读取状态，读取成功为True，读取失败为False
        - info   读取异常信息，成功为空串
        - data   表格数据信息， 失败为None，成功为一个二维列表，第一行为表头，顺序按照fields传入顺序排列，第二行开始为数据行

        :info异常信息说明：
        - 表格为空
        - 待读取的列不存在，属于输入参数错误，一般为带读取列不存在
        - 检索条件配置错误， 属于输入参数错误，一般为检索列不存在
    '''
    time.sleep(1)
    # 获取待读取数据
    need_field_list = []
    if len(fields) > 0:
        need_field_list = fields.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","

    # 解析数据检索条件
    filter_field_list = []  # 条件表头信息
    filter_field_value_list = []  # 条件表头对应的值
    if len(filter) > 0 and filter != '_':
        fls = filter.split(SplitSymbol.SYMBOL_COMBINE_META)  # 筛选条件列表  #"#AND#"
        for fl in fls:
            cond = fl.split(SplitSymbol.SYMBOL_COMPARE_EQUAL)  # "="
            if len(cond) != 2:
                info = "配置错误：表格检索条件[%s]在[%s]出表达式错误" % (filter, fl)
                return False, info, None
            filter_field_list.append(cond[0])
            filter_field_value_list.append(cond[1])

    # 读取菜单数据(表头)
    wait = WebDriverWait(driver, 30, 0.5)
    element = wait.until(lambda thead_list:el.find_elements("tag name", "thead"), message="获取页面元素超时")
    thead_list = el.find_elements("tag name", "thead") # thead对象列表

    if len(thead_list) != 0:
        thead_th_v_list = []  # 存放的表头信息列表
        youxiao_list =[]
        element = WebDriverWait(driver, 30, 0.5).until(lambda thead_tr_list:thead_list[0].find_elements("tag name", "tr"), message="获取页面元素超时")
        thead_tr_list = thead_list[0].find_elements("tag name", "tr")  # th对象列表
        if len(thead_tr_list) == 1 :
            try:
                element = wait.until(lambda thead_div_list:thead_tr_list[0].find_elements("tag name", "div"), message="")
                youxiao_list = thead_tr_list[0].find_elements("tag name", "div")
            except:
                try:
                    element =wait.until(lambda thead_div_list: thead_tr_list[0].find_elements("tag name", "th"), message="")
                    youxiao_list = thead_tr_list[0].find_elements("tag name", "th")  # th对象列表
                except:
                    return False, "", "找不到数据"

            for i in youxiao_list:
                thead_th_v_list.append(i.get_attribute("innerText"))

        elif len(thead_tr_list) == 2 :
            z = 0
            element = wait.until(lambda thead_tr_list:thead_list[0].find_elements("tag name", "th"),message="获取页面元素超时")
            thead_th_list = thead_tr_list[0].find_elements("tag name", "th")
            thead_th_list1 = thead_tr_list[1].find_elements("tag name", "th")
            for j in thead_th_list:
                if j.get_attribute("colspan"):
                    for l in range(z, int(j.get_attribute("colspan"))+z):
                        thead_th_v_list.append(
                            j.get_attribute("innerText") + '-' + thead_th_list1[z].get_attribute("innerText"))
                        z += 1
                else:
                    thead_th_v_list.append(j.get_attribute("innerText"))
        else:
            return False, "", "tr标签个数超过2个"

    else:
        return False, "", "找不到数据"

    # 判断待读取的列是否存在
    if len(need_field_list) > 0 and need_field_list[0] != '_':
        for i in need_field_list:  # 获取读取列的索引号
            if i not in thead_th_v_list:
                info = "配置错误:读取列[%s]有列在表中未找到，表的列为[%s]" % (fields, thead_th_v_list)
                return False, info, None
    # print('getdata_from_bootstrapp_table_tubiao:::',el, driver, need_field_list, filter_field_list, filter_field_value_list, thead_th_v_list,return_type)
    status, info, data = getdata(el, driver, need_field_list, filter_field_list, filter_field_value_list, thead_th_v_list,return_type)
    return status, info, data

def getdata_from_bootstrapp_table_quxian(el, driver:WebDriver, fields: str = "", filter: str = "", return_type: str = ""):  # (el对象，‘’，‘’)
    '''
        读取表格元素的值
        :输入参数：\n
        - el     指定读取的表格元素，此处为做类型判断，如传入其他元素可能会产生意想不到的错误
        - fields 待读取的列，多列以“,”分隔，如果为空则读取全部列，按界面顺序输出
        - filter 检索命中条件，单个条件格式为“列名=值”，多个条件以“#AND#”连接，如果为空则无检索条件

        :输出参数：
        - status 读取状态，读取成功为True，读取失败为False
        - info   读取异常信息，成功为空串
        - data   表格数据信息， 失败为None，成功为一个二维列表，第一行为表头，顺序按照fields传入顺序排列，第二行开始为数据行

        :info异常信息说明：
        - 表格为空
        - 待读取的列不存在，属于输入参数错误，一般为带读取列不存在
        - 检索条件配置错误， 属于输入参数错误，一般为检索列不存在
    '''
    time.sleep(5)
    # 获取待读取数据
    need_field_list = []
    if len(fields) > 0:
        need_field_list = fields.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","

    # 解析数据检索条件
    filter_field_list = []  # 条件表头信息
    filter_field_value_list = []  # 条件表头对应的值
    if len(filter) > 0 and filter != '_':
        fls = filter.split(SplitSymbol.SYMBOL_COMBINE_META)  # 筛选条件列表  #"#AND#"
        for fl in fls:
            cond = fl.split(SplitSymbol.SYMBOL_COMPARE_EQUAL)  # "="
            if len(cond) != 2:
                info = "配置错误：表格检索条件[%s]在[%s]出表达式错误" % (filter, fl)
                return False, info, None
            filter_field_list.append(cond[0])
            filter_field_value_list.append(cond[1])

    # 读取菜单数据(表头)
    wait = WebDriverWait(driver, 30, 0.5)
    element = wait.until(lambda thead_list: el.find_elements("tag name", "thead"), message="获取页面元素超时")
    thead_list = el.find_elements("tag name", "thead")  # thead对象列表
    element = wait.until(lambda thead_th_list: thead_list[0].find_elements("tag name", "th"), message="获取页面元素超时")
    thead_th_list = thead_list[0].find_elements("tag name", "th")  # th对象列表
    thead_th_v_list = []  # 存放的表头信息列表
    for i in thead_th_list:
        thead_th_v_list.append(i.get_attribute("innerText"))

    # 判断待读取的列是否存在
    if len(need_field_list) > 0 and need_field_list[0] != '_':
        for i in need_field_list:  # 获取读取列的索引号
            if i not in thead_th_v_list:
                info = "配置错误:读取列[%s]有列在表中未找到，表的列为[%s]" % (fields, thead_th_v_list)
                return False, info, None

    status, info, data = getdata(el, driver, need_field_list, filter_field_list, filter_field_value_list, thead_th_v_list,return_type)
    return status, info, data


def getdata(el, driver:WebDriver, need_field_list, filter_field_list, filter_field_value_list, thead_th_v_list, return_type: str = "3"):
# def getdata(el, need_field_list, filter_field_list, filter_field_value_list, thead_th_v_list, return_type: str = "3"):
    # 读取内容与菜单一起组成一个字典
    time.sleep(1)
    wait = WebDriverWait(driver, 30, 0.5)
    element = wait.until(lambda tbody_list:el.find_elements("tag name", "tbody"), message="获取页面元素超时")
    tbody_list = el.find_elements("tag name", "tbody")  # tbody对象列表

    element = wait.until(lambda tbody_tr_list:tbody_list[0].find_elements("tag name", "tr"), message="获取页面元素超时")
    tbody_tr_list = tbody_list[0].find_elements("tag name", "tr")  # tr对象列表
    table_list_dict = []  # [{表头：数据},{表头：数据}]
    for j in tbody_tr_list:
        element = wait.until(lambda tbody_td_list: j.find_elements("tag name", "td"), message="获取页面元素超时")
        tbody_td_list = j.find_elements("tag name", "td")  # td对象列表
        thead_tbody = {}  # {表头：数据}字典
        for z in range(0, len(tbody_td_list)):
            tbody_td_v = tbody_td_list[z].get_attribute("innerText")
            thead_tbody[thead_th_v_list[z]] = tbody_td_v
        table_list_dict.append(thead_tbody)
    # print(thead_tbody)
    # print(table_list_dict)


    # 判断过滤列是否存在,并生成对应的值
    table_dict = []
    if len(filter_field_list) > 0 and filter_field_list[0] != '_':   #有判断条件
        for i in filter_field_list:
            if i not in thead_th_v_list:
                info = "配置错误,不存在的条件选项"
                return False, info, None
        if len(need_field_list) > 0 and need_field_list[0] != '_':   #有判断条件且有目标值
            for l in table_list_dict:
                tt = True
                for zz in range(0, len(filter_field_value_list)):
                    if not isinstance(l[filter_field_list[zz]], str) or not isinstance(filter_field_value_list[zz],str):
                        l[filter_field_list[zz]] = str(l[filter_field_list[zz]])
                        filter_field_value_list[zz] = str(filter_field_value_list[zz])
                    if l[filter_field_list[zz]] != filter_field_value_list[zz]:
                        tt = False
                if tt == True:
                    dic = {}
                    for z in need_field_list:
                        dic[z] = l[z]
                    table_dict.append(dic)
        else:         #有判断条件 没有目标值
            for l in table_list_dict:
                tt = True
                for zz in range(0, len(filter_field_value_list)):
                    if not isinstance(l[filter_field_list[zz]], str) or not isinstance(filter_field_value_list[zz], str):
                        l[filter_field_list[zz]] = str(l[filter_field_list[zz]])
                        filter_field_value_list[zz] = str(filter_field_value_list[zz])
                    if l[filter_field_list[zz]] != filter_field_value_list[zz]:
                        tt = False
                if tt == True:
                    table_dict.append(l)
    else:            #没有判断条件 有目标值
        if len(need_field_list) > 0 and need_field_list[0] != '_':
            for l in table_list_dict:
                dic = {}
                for z in need_field_list:
                    dic[z] = l[z]
                table_dict.append(dic)
        else:        #没有判断条件 没有目标值
            table_dict = table_list_dict

    #根据return_type返回对应的数据类型
    # print(table_dict)
    # if return_type not in ['4','5','6',4, 5, 6]:   #list
    if return_type in ['3', 3]:  # list
        tb_list = []
        for tb in table_dict:
            tb_list.append(list(tb.values()))
        if len(tb_list) == 1:
            tb_list = tb_list[0]
        return True, "", tb_list
    elif return_type in [4, "4"] : #str
        tb_list = []
        for tb in table_dict:
            for i in list(tb.values()):
                tb_list.append(i)
        tb_list_str = ",".join(tb_list)
        return True, "", tb_list_str
    elif return_type in [5, "5"]: #list-dict
        return True, "", table_dict
    elif return_type in [6, "6"]: #(True, '', [['key1', 'key2'], ['v1', 'v2']])
        tb_list = []
        for i in range(0, len(table_dict)):
            if i == 0:
                tb_list.append(list(table_dict[i].keys()))
            tb_list.append(list(table_dict[i].values()))
        return True, "", tb_list
    else:
        return False, "请输入对应的返回类型", []


def getdata_fanstatus(el, driver:WebDriver, fields: str = "", filter: str = "", return_type: str = "3"):  # (el对象，‘’，‘’)
    '''
        读取表格元素的值
        :输入参数：\n
        - el     指定读取的表格元素，此处为做类型判断，如传入其他元素可能会产生意想不到的错误
        - fields 待读取的列，多列以“,”分隔，如果为空则读取全部列，按界面顺序输出
        - filter 检索命中条件，单个条件格式为“列名=值”，多个条件以“#AND#”连接，如果为空则无检索条件

        :输出参数：
        - status 读取状态，读取成功为True，读取失败为False
        - info   读取异常信息，成功为空串
        - data   表格数据信息， 失败为None，成功为一个二维列表，第一行为表头，顺序按照fields传入顺序排列，第二行开始为数据行

        :info异常信息说明：
        - 表格为空
        - 待读取的列不存在，属于输入参数错误，一般为待读取列不存在
        - 检索条件配置错误， 属于输入参数错误，一般为检索列不存在
    '''
    time.sleep(1)
    stinfo = "传入参数，fields待读取:%s, filter条件:%s, return_type返回信息类型:%s" % (fields, filter, return_type)
    lg.myloger.info(stinfo)
    # 获取待读取数据
    need_field_list = []   #目标值--子菜单
    if len(fields) > 0:
        field_list = fields.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","
        for ne in field_list:
            need_field_list.append(ne.replace(" ", ""))


    # 解析数据检索条件
    filter_field_list = []  # 目标值--菜单
    if len(filter) > 0:
        field_list_fi = filter.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)  # ","
        for fi in field_list_fi:
            filter_field_list.append(fi.replace(" ", ""))

    # 读取菜单数据(表头)、子菜单数据、子菜单数据对应的值
    wait = WebDriverWait(driver, 30, 0.5)

    h4_list_v=[]   #菜单数据
    span_list_v=[]   #子菜单数据
    strong_list_v=[]   #子菜单数据对应的值
    span_list_allv=[]  #子菜单全部的值
    strong_list_allv = []  #子菜单数据对应的全部值

    element = wait.until(lambda thead_list:el.find_elements("class name", "panel_list"), message="获取页面元素panel_list超时")
    panel_list = el.find_elements("class name", "panel_list") # panel_list对象列表
    # print(panel_list)
    # print(len(panel_list))
    for i in range(0,len(panel_list)):
        element = wait.until(lambda thead_list: el.find_elements("tag name", "h4"), message="获取页面元素h4超时")
        h4_list = panel_list[i].find_elements("tag name", "h4")  # h4对象列表
        element = wait.until(lambda thead_list: el.find_elements("tag name", "span"), message="获取页面元素span超时")
        span_list = panel_list[i].find_elements("tag name", "span")  # span对象列表
        element = wait.until(lambda thead_list: el.find_elements("tag name", "strong"), message="获取页面元素strong超时")
        strong_list = panel_list[i].find_elements("tag name", "strong")  # strong对象列表
        # print(len(h4_list),len(span_list),len(strong_list))
        if len(h4_list)==1:
            h4 = h4_list[0].get_attribute("innerText")
            h4.replace(" ", "")
            h4_list_v.append(h4)
        else:
            return False,'暂不支持','暂不支持'
        if len(span_list) == len(strong_list):
            span_list_v_zi = []
            strong_list_v_zi = []
            for j in range(0,len(span_list)):
                span = span_list[j].get_attribute("innerText").replace(" ", "")
                span_list_v_zi.append(span)
                span_list_allv.append(span)
                strong = strong_list[j].get_attribute("innerText").replace(" ", "")
                strong_list_v_zi.append(strong)
                strong_list_allv.append(strong)
            span_list_v.append(span_list_v_zi)
            strong_list_v.append(strong_list_v_zi)
    # print(h4_list_v,'@',span_list_allv,'@','@', strong_list_allv)

    #组合成字典格式的列表
    h4_list_v_v = []
    if len(h4_list_v) == len(span_list_v) == len(strong_list_v):
        for i in range(0, len(span_list_v)):
            dict1 = dict(zip(span_list_v[i], strong_list_v[i]))
            h4_list_v_v.append(dict1)

        dict_all = dict(zip(h4_list_v, h4_list_v_v))
        # print(dict_all)
    else:
        info = f"表头名称和对应的值个数不一致，表头：{h4_list_v},子表头信息：{span_list_v},子表头信息对应的值{strong_list_v}"
        return False, info, None

    # 判断待读取的列是否存在
    if len(need_field_list) > 0 and need_field_list[0] != '_':
        for i in need_field_list:  # 获取读取列的索引号
            if i not in span_list_allv:
                info = "配置错误:读取列[%s]有列在表中未找到，表的列为[%s]" % (fields, span_list_allv)
                return False, info, None

    # 判断过滤列是否存在,并生成对应的值
    table_dict = []
    if len(filter_field_list) > 0 and filter_field_list[0] != '_':   #有菜单数据
        zj_list = []
        for i in filter_field_list:
            if i not in h4_list_v:
                info = "配置错误:读取列[%s]有列在表中未找到，表的列为[%s]" % (filter, h4_list_v)
                return False, info, None
            else:
                zj_list.append(dict_all[i])
        if len(need_field_list) > 0 and need_field_list[0] != '_':   #有菜单，有子菜单
            for zj in zj_list:
                for n in need_field_list:
                    zj_vv = zj[n].split(', ')
                    table_dict.append(zj_vv)
        else:         #有菜单 没有子菜单
            for zj in zj_list:
                for zj_v in list(zj.values()):
                    zj_vv = zj_v.split(', ')
                    table_dict.append(zj_vv)
    else:
        if len(need_field_list) > 0 and need_field_list[0] != '_':   #没有菜单，有子菜单
            for zj in list(dict_all.values()):
                for n in need_field_list:
                    zj_vv = zj[n].split(', ')
                    table_dict.append(zj_vv)
        else:           #没有判断条件 没有目标值  获取全部的值
            for zj_v in strong_list_allv:
                zj_vv = zj_v.split(', ')
                table_dict.append(zj_vv)
    return True, "", table_dict