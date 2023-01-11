#coding:utf-8
'''
    Web界面自动化测试封装接口WebCfg

'''
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import select 
from selenium.webdriver.support.select import Select
import time
from splitcfg import SplitSymbol
from selenium.webdriver.support.wait import WebDriverWait

class WebCfg():
    '''
        web ui自动化测试操作封装，实现基于selenium的常规操作封装，主要包括以下功能：
        - 创建浏览器驱动对象：通过传入的驱动类型，创建一个浏览器驱动对象供后续测试步骤使用
        - 关闭浏览器驱动对象：关闭一个浏览器驱动对象
        - 测试操作：通过定位参数定位界面元素并执行指定的操作
    '''
    def __init__(self):
        self.__symbol_element_type2id = SplitSymbol.SYMBOL_BETWEEN_OBJECT_AND_CONDITION  #"|"
        self.__symbol_action2para = SplitSymbol.SYMBOL_BETWEEN_ELEMENTS_IN_CONDITION  #"@"

        
        self.__symbol_between_element = SplitSymbol.SYMBOL_BETWEEN_MODELLEVEL   #"@@"
        self.__symbol_between_action = SplitSymbol.SYMBOL_BETWEEN_MODELLEVEL   #"@@"
        pass

    def createdriver(self,browser_type:str = "chrome"):
        '''
            创建驱动
            :输入参数：
            - browser_type 驱动类型，缺省为chrome
            
            :输出参数：
            - status        执行状态
            - info          错误信息，执行正确则为空
            - driver        驱动对象
            
            :用法：
                在测试过程中，多个测试步骤需要用同一个driver下执行，则可调用此功能创建一个驱动，用于后续步骤执行
        '''
        self.__logining = True
        # 实例化谷歌浏览器对象，并赋予变量名称driver
        driver = self.__get_driver__(browser_type)   # webdriver.Chrome()   browser_type=chrome
        info = ""
        if driver is None:
            info = "不支持的浏览器[%s]" % browser_type
            return False,info,None

        # 最大化浏览器窗口
        driver.maximize_window()
        
        return True,"",driver
    
    def quitdriver(self,driver):
        '''
            关闭传入的驱动
            :输入参数：
            - driver 驱动对象
            
            :输出参数：
            - status 执行状态
            - info   错误信息，执行正确则为空
            - None   空对象，为了接口统一而已
            
            :用法：
                在测试过程中，与createdriver配套调用，关闭已不再需要的驱动
        '''
        if not driver  is None:
            driver.quit()
        
        return True,"",None

    def element_action(self,url:str,position_para:str,action_str:str,driver=None,browser_type:str = "chrome"):
        '''
            元素操作功能
            :说    明：
                根据传入url，根据定位参数和操作参数，完成元素定位执行指定操作并返回执行结果。
                支持一次执行多个"定位-执行-返回结果"链，多个参数之间用SplitSymbol.SYMBOL_BETWEEN_MODELLEVEL连接。
                注意事项：如果一次执行多个链时，只会返回最后一步的成功执行结果或执行过程中的错误结果
            
            :输入参数：
            - driver        驱动，如果驱动为None,则自动创建一个，并在退出时关闭 
            - url           页面URL
            - position_para 定位参数。详细参见函数“__find_element__”说明
            - action_str    操作参数。详细参见函数“__do_action__”说明
            - browser_type  浏览器驱动类型，缺省为"chrome"
            
            :输出参数：
            - status        执行状态
            - info          错误信息，执行正确则为空
            - data          执行返回数据。详细参见函数“__do_action__”说明
            
            :用    法：
                用例执行核心功能，有一下两种使用情况：\n
                    1）和“createdriver”、“quitdriver”功能配套使用，传入driver不为空，则用传入driver执行相关用例\n
                    2）独立使用，此时传入driver为空或缺省，则创建一个驱动并执行用例，退出前关闭驱动\n
        ''' 
        # 浏览器输入地址
        myDriver = driver
        is_need_quit_driver = False
        if myDriver is None:
            status,info,myDriver = self.createdriver(browser_type)
            is_need_quit_driver = True
            if status is False:
                return status,info,None
        try:
            myDriver.get(url)
        except TimeoutException:
            info = "get页面[%s]超时" % url
            #如果是自动创建的驱动，退出时须关闭
            if is_need_quit_driver is True:
                myDriver.quit()
            return False,info,None
        
        position_para_list = position_para.split(self.__symbol_between_element)   #定位参数，分隔符是“@@"
        action_str_list = action_str.split(self.__symbol_between_action)   #操作参数，分隔符是“@@" ['do_select@龙头风电厂@text','set_datetime@2021-09-03 00:00:00','click']
        # ①通过id定位元素：定位输入框的位置，并赋予变量名称ssk
        status = True
        info = ""
        data = None

        for i in range(0,len(position_para_list)):
            status,info,el = self.__find_element__(myDriver,position_para_list[i])  #获取定位对象el
            if status is False:
                #如果是自动创建的驱动，退出时须关闭
                if is_need_quit_driver is True:
                    myDriver.quit()
                return status,info,None
            
            #执行操作
            status,info,data = self.__do_action__(el,myDriver,action_str_list[i],position_para_list[i])  #执行对象操作
            if status is False:
                #如果是自动创建的驱动，退出时须关闭
                if is_need_quit_driver is True:
                    myDriver.quit()
                return status,info,None
            
            time.sleep(1)

        #如果是自动创建的驱动，退出时须关闭
        if is_need_quit_driver is True:
            myDriver.quit()
        return status,info,data

    def __get_driver__(self,browser_type:str):
        '''
            "@@"
            :输入参数：
            - browser_type 浏览器类型，目前待选为chrome和firefox
            :输出参数：
            - webdriver    "@@"
        '''
        s = browser_type.lower().strip()  #变为小写，去除前后多余的空格
        if s == "chrome":
            options = webdriver.ChromeOptions()
            # 忽略无用的日志
            options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
            driver = webdriver.Chrome(chrome_options=options)
            return driver
            # return webdriver.Chrome()
        elif s == "firefox":
            return webdriver.Firefox()
        else:
            return None
    
    def __find_element__(self,driver,position_para:str):
        '''
            定位页面元素
            :输入参数：
            - driver         浏览器驱动对象\n
            - position_para  定位元素配置，格式为“元素定位类型@元素标识”，其中元素定位类型和selenium的By对应，对应关系如下\n
                                    类型                  |   selenium By  \n
                                    "id"                  |   "id"\n
                                    "name"                |   "name"\n
                                    "xpath"               |   "xpath"\n
                                    "link_text"           |   "link text"\n
                                    "partial_link_text"   |   "partial link text"\n
                                    "tag_name"            |   "tag name"\n
                                    "class_name"          |   "class name"\n
                                    "css_selector"        |   "css selector"\n
            
            :输入参数：
            - status  定位状态，成功为True，失败为False
            - info    定位失败信息，成功则为空
            - el      元素对象，失败则为None
        '''
        ss = position_para.split(self.__symbol_element_type2id)   #"|"
        if len(ss) < 2:
            return False,"定位参数[%s]不正确" % (position_para),None
        
        by = ss[0].strip().lower()
        e_str = ss[1].strip()
        status = False
        el = None
        info = ""
        for trytimes in range(0, 10):
            try:
                if by == "id":
                    el = driver.find_element_by_id(e_str)
                elif by == "name":
                    el = driver.find_element_by_name(e_str)
                elif by == "xpath":
                    el = driver.find_element_by_xpath(e_str)
                elif by == "link_text":
                    el = driver.find_element_by_link_text(e_str)
                elif by == "partial_link_text":
                    el = driver.find_element_by_partial_link_text(e_str)
                elif by == "tag_name":
                    el = driver.find_element_by_tag_name(e_str)
                elif by == "class_name":
                    el = driver.find_element_by_class_name(e_str)
                elif by == "css_selector":
                    el = driver.find_element_by_css_selector(e_str)
                elif by == 'alert':
                    el = driver
                else:
                    info = "不支持的定位类型:类型[%s]在定位串中[%s]" %(by,position_para)
                    return False,info,None
                status = True
                break
            except Exception:
                time.sleep(0.5)
        
        if status is False:
            info = "未找到指定元素[%s]" % position_para
        
        return True,info,el

    def __do_action__(self,el,myDriver,action_str:str,position_str:str):
        '''
            界面元素操作功能
            :输入参数：
            - el          待操作元素
            - action_str  操作方法及参数说明，方法和参数用“@”连接，格式为“方法@参数”。目前只接受一个参数，\n
                          详细说明见操作说明
            
            :输出参数：
            - status 读取状态，读取成功为True，读取失败为False
            - info   读取异常信息，成功为空串
            - data   操作返回数据，内容和格式见操作说明
            
            :操作说明：
            - click 点击 无附加参数，返回(True,"",None)
            - send_keys  输入数据，参数为待输入值，举例为“send_keys#_#参数” ，\n
                                  设置正确则返回(True,"",None)，错误返回(False,错误信息,None)，错误信息主要为缺少参数
            - text  读取元素文本信息 无附加参数，(True,"",text)
            - get_property 读取元素属性值，参数为“属性名”，正确返回(True,"",属性值)，错误返回(False,错误信息,None)
            - value_of_css_property 同4）
            - is_selected 检查元素是否已选中，正确返回(True,"",True)
            - is_enabled  检查元素是否可用，正确返回(True,"",True)
            - is_displayed  检查元素是否显示，正确返回(True,"",True)
            - get_tabledata  读取表格数据，详细说明见方法“__getdata_from_table_element__”说明
            - 不支持的类型   返回(False,"不支持的操作类型:[%s]",None)
        '''
        action_ls = action_str.split(self.__symbol_action2para)   #分隔符"@"  操作参数列表[‘do_select','龙头风电厂','text’]
        if len(action_ls) == 0:
            return False,"动作参数配置为空",None

        act = action_ls[0].strip().lower()
        data = None
        status = True
        info = ""
        data = None

        if act == "click":#点击操作
            el.click()
            time.sleep(1)
        elif act == "send_keys":#设置值操作
            if len(action_ls) < 2:
                info = "动作参数[%s]配置错误:send_keys缺少参数" % action_str
                status = False
            else:
                el.clear()
                el.send_keys(action_ls[1])
        elif act == "text":#取文本操作
            data = el.text
        elif act == "get_property":#取属性操作
            if len(action_ls) < 2:
                info = "动作参数[%s]配置错误:get_property缺少参数" % action_str
                status = False
            else:
                data = el.get_property(action_ls[1])
        elif act == "value_of_css_property":#取CSS属性操作
            if len(action_ls) < 2:
                info = "动作参数[%s]配置错误:value_of_css_property缺少参数" % action_str
                status = False
            else:
                data = el.value_of_css_property(action_ls[1])
        elif act == "is_selected":#判断是否被选中
            data = el.is_selected()
        elif act == "is_enabled":#判断是否可用
            data = el.is_enabled()
        elif act == "is_displayed":#判断是否显示
            data = el.is_displayed()
        elif act == "get_tabledata":#读取表格数据
            fieldinfo = ""
            filterinfo = ""
            count = len(action_ls)
            if count > 1:
                fieldinfo = action_ls[1]
            if count > 2:
                filterinfo = action_ls[2]
            status,info,data = self.__getdata_from_table_element__(el,fieldinfo,filterinfo)
        elif act == "get_bootstraptable_data":#读取表格数据，弃用
            import bootstrap
            fieldinfo = ""
            filterinfo = ""
            count = len(action_ls)
            if count > 1:
                fieldinfo = action_ls[1]
            if count > 2:
                filterinfo = action_ls[2]
            status,info,data = bootstrap.getdata_from_bootstrapp_table(el,fieldinfo,filterinfo)
        elif act == "get_quxian_data":#读取曲线数据
            import bootstrap
            fieldinfo = ""
            filterinfo = ""
            return_type = '3'
            count = len(action_ls)
            if count > 1:
                fieldinfo = action_ls[1]
            if count > 2:
                filterinfo = action_ls[2]
            if count > 3:
                return_type =  action_ls[3]

            status,info,data = bootstrap.getdata_from_bootstrapp_table_quxian(el, myDriver,fieldinfo,filterinfo, return_type)
        elif act == "get_tubiao_data":  # 读取表格数据
            import bootstrap
            fieldinfo = ""
            filterinfo = ""
            return_type ='3'
            count = len(action_ls)
            if count > 1:
                fieldinfo = action_ls[1]
            if count > 2:
                filterinfo = action_ls[2]
            if count > 3:
                return_type = action_ls[3]
            # print('get_tubiao_data传入值', el, myDriver, fieldinfo, filterinfo, return_type)
            status, info, data = bootstrap.getdata_from_bootstrapp_table_tubiao(el, myDriver, fieldinfo, filterinfo, return_type)

        elif act == "getdata_fanstatus":  # 读取风机状态数据
            import bootstrap
            fieldinfo = ""
            filterinfo = ""
            return_type ='3'
            count = len(action_ls)
            if count > 1:
                fieldinfo = action_ls[1]
            if count > 2:
                filterinfo = action_ls[2]
            if count > 3:
                return_type = action_ls[3]
            status, info, data = bootstrap.getdata_fanstatus(el, myDriver, fieldinfo, filterinfo, return_type)

        elif act == "do_select":
            count  = len(action_ls)
            if count < 3:
                info = "动作参数[%s]配置错误:do_select缺少参数" % action_str
                status =  False
            else:
                value = action_ls[1]
                myby = action_ls[2]

                status,info = self.__set_value_of_select_element__(el,value,myby)
        elif act == "set_datetime":
            count  = len(action_ls)
            if count < 2:
                info = "动作参数[%s]配置错误:set_datetime缺少参数" % action_str
                status =  False
            else:
                value = action_ls[1]
                status,info = self.__set_datetime__(position_str,value,myDriver)  #(定位参数，操作参数，驱动)
        elif act == "clear":#清除数据操作
            el.clear()
            time.sleep(1)
        elif act == "alert_text":#清除数据操作
            data = el.switch_to.alert.text
            time.sleep(1)
        elif act == "alert_accept": #确定按钮
            data = myDriver.switch_to.alert.accept()
            time.sleep(1)
        elif act == "alert_dismiss":  #取消操作
            data = myDriver.switch_to.alert.dismiss()
        elif act == "text_select":
            count = len(action_ls)
            if count < 3:
                info = "动作参数[%s]配置错误:text_select缺少参数" % action_str
                status = False
            else:
                value = action_ls[1]
                myby = action_ls[2]

                # status, info = self.__set_value_of_select_element__(el, value, myby)
                status, info, data = self.__get_value_of_select_element__(el, value, myby)
        else:
            info = "不支持的操作类型:[%s]" % action_str
            status = False
        return status,info,data

    def __getdata_from_table_element__(self,el,fields:str="",filter:str=""):
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
        table_tr_list = el.find_elements("tag name", "tr")
        table_list = []  #存放table数据
        is_header = True
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

        table_td_list = table_tr_list[0].find_elements("tag name", "td")
        for td in table_td_list:    #遍历每一个td
                header_list.append(td.text)
        
        #判断过待读取列是否存在
        if len(need_field_list) == 0:
            #table_list.append(header_list)
            pass
        else:
            try:
                for i in range(0,len(need_field_list)):#获取读取列的索引号
                    index =   header_list.index(need_field_list[i])
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

        for tr in table_tr_list[1:]:    #遍历每一个数据行（tr）
            #将每一个tr的数据根据td查询出来，返回结果为list对象
            table_td_list = tr.find_elements("tag name", "td")
            if len(table_td_list) == 0:
                break
            is_filter = True
            for i in range(0,len(filter_fieldindex_list)):
                index = filter_fieldindex_list[i]
                if table_td_list[index] != filter_field_value_list[i]:
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
        return True,"",table_list
    
    def __set_value_of_select_element__(self,el,value:str,by:str = "text"):
        '''
            设置下拉选择框的值
            :输入参数:
            - el             Select控件
            - by             方法类型，备选为"index","value"和"text",对应相应方法，缺省为"text"
            - value          与方法对应参数，by为"index"，则为选项序号；
                             by为"value"，则为对应值；by为"text"，则为对应显示值；
            
            :输出参数:
            - status         执行结果状态，成功为True，反之为False
            - info           出错信息，成功则为空
        '''
        status = True
        info = ""
        myby =by.lower().strip()
        try:
            select_element = Select(el)
            if myby == "index":
                index = int(value)
                #el.select_by_index(0)
                select_element.select_by_index(index)
            elif myby == "value":
                select_element.select_by_value(value)
            elif myby == "text":
                select_element.select_by_visible_text(value)
            else:
                status = False
                info = "设置Select控件值错误：方法[%s]不支持,应为[\"index\",\"Value\",\"text\"]之一" %(by)
        except Exception as e :
            info = "设置Select控件值错误：采用方法{},无对应值{}命中,异常信息为{}".format(by,value,e)
        
        return status,info

    def __get_value_of_select_element__(self, el, indexnum: str, by: str = "text"):
        '''
            设置下拉选择框的值
            :输入参数:
            - el             Select控件
            - by             方法类型，备选为"index","value"和"text",对应相应方法，缺省为"text"
            - value          与方法对应参数，by为"index"，则为选项序号；
                             by为"value"，则为对应值；by为"text"，则为对应显示值；

            :输出参数:
            - status         执行结果状态，成功为True，反之为False
            - info           出错信息，成功则为空
        '''
        status = True
        info = ""
        myby = by.lower().strip()
        value_list = []
        text_list = []
        V = []
        try:
            options_list = el.find_elements_by_tag_name('option')
            for options in options_list:
                value_list.append(options.get_attribute('value'))
                text_list.append(options.text)

            if myby == "value":
                if int(indexnum) >= len(value_list):
                    status = False
                    info = f"输入的下标{indexnum}不存在，没有对应value"
                else:
                    V = value_list[int(indexnum)]
            elif myby == "text":
                if int(indexnum) >= len(value_list):
                    status = False
                    info = f"输入的下标{indexnum}不存在，没有对应text"
                else:
                    V = text_list[int(indexnum)]
            elif myby == "valueall":
                V = value_list
            elif myby == "textall":
                V = text_list
            else:
                status = False
                info = "获取Select选择值错误：方法[%s]不支持,应为[\"Value\",\"text\",\"Valueall\",\"textall\"]之一" % (by)
        except Exception as e:
            info = "设置Select控件值错误：采用方法{},无对应值{}命中,异常信息为{}".format(by, indexnum, e)

        return status, info, V

    def __set_datetime__(self,position_str:str,datetime_str:str,driver:WebDriver):
        '''
            设置时间控件的值
            :输入参数:
            - position_str   时间控件定位串
            - datetime_str   时间字符串
            - driver         驱动
            :输出参数:
            - status         设置状态
            - info           设置错误信息输出
        '''
        ss = position_str.split(self.__symbol_element_type2id)  #"|"
        if len(ss) < 2:
            return False,"定位参数[%s]不正确" % (position_str)
        
        by = ss[0].strip().lower()
        e_str = ss[1].strip()
        status = True
        info = ""
        try:
            js_value = ""
            if by == "id":
                js_value = 'document.getElementById("{}").value="{}"'.format(e_str,datetime_str)
            elif by == "name":
                js_value = 'document.getElementByName("{}").value="{}"'.format(e_str,datetime_str)
            elif by == "xpath":
                js_value = 'document.evaluate("{}",document).iterateNext().value="{}"'.format(e_str,datetime_str)
            elif by == "tag_name":
                js_value = 'document.getElementByTagName("{}").value="{}"'.format(e_str,datetime_str)
            elif by == "class_name":
                js_value = 'document.getElementByClassName("{}").value="{}"'.format(e_str,datetime_str)
            elif by == "css_selector":
                js_value = 'document.querySelectorAll("{}").value="{}"'.format(e_str,datetime_str)
            else:
                info = "不支持的定位类型:[%s]" % position_str
                return False,info,None
            driver.execute_script(js_value)
            # ret = driver.execute_script(js_value)
            # print(ret)

        except Exception as e:
            info = "设置时间控件值错误:{}".format(e)
        
        return status,info

if __name__ == '__main__':
    #测试操作
    # url = "http://10.64.14.184:18080/SPPP-web/index"
    url = "http://10.64.14.70:18080/SPPP-web/login"
    position_str_user = "id|username@@id|password@@id|submit"
    # position_str_user_action = "send_keys@wpfs@@send_keys@wpfs@@click"
    # position_str_user_action = "send_keys@cpfs@@send_keys@cpfs@@click"
    position_str_user_action = "send_keys@test@@send_keys@Test123456@@click"


    wc = WebCfg()
    s,i,d = wc.createdriver()
    # print("s:",s)
    # print("i:",i)
    # print("d:",d)
    s,i,aa = wc.element_action(url,position_str_user,position_str_user_action,d,"")

    #
    # url1 = "http://10.64.14.70:18080/SPPP-web/windturbine/windturbineState"
    # position_str_user1='id|states'
    # position_str_user_action1 = "get_tubiao_data@_@_"                             # 1、获取全部信息
    # position_str_user_action1 = "get_tubiao_data@风速:@_"                        # 2、获取全部风机的某一个值
    # position_str_user_action1 = "get_tubiao_data@风速:,有功 :@_"                  #3、获取全部风机的某几个值
    # position_str_user_action1 = "get_tubiao_data@_@风机：风机_8"                  # 4、获取某一个风机的全部数据
    # position_str_user_action1 = "get_tubiao_data@风速:@风机：风机_8"               # 5、获取某一个风机的某一个数据
    # position_str_user_action1 = "get_tubiao_data@有功 : , 状态 : @风机：风机_5"     # 6、获取某一个风机的某几个数据
    # position_str_user_action1 = "get_tubiao_data@有功 : , 状态 : @风机：风机_5,风机：风机_6"  #7、获取某几个风机的某几个数据
    # position_str_user_action1 = "get_tubiao_data@风速:@风机：风机_5,风机：风机_6"  # 8、获取某几个风机的某一个数据
    # position_str_user_action1 = "get_tubiao_data@_@风机：风机_5,风机：风机_6"  # 9、获取某几个风机的全部数据
    # s,i,aa = wc.element_action(url1,position_str_user1,position_str_user_action1,d,"")
    # print("s:",s)
    # print("i:",i)
    # print("曲线图:",aa)

    # url1 = "http://10.64.14.184:18080/SPPP-web/fcstcastmodify/fcstcastModifyJump"
    # position_str_user1='xpath|//*[@id="fcstcastTbody"]/tr[1]/td[5]/a@@xpath|//*[@id="coefficient96"]@@xpath|//*[@id="coefficient96"]@@xpath|//*[@id="bSubmit"]@@alert|alert@@alert|alert@@xpath|/html/body/div[5]/div[7]/div/button'
    # position_str_user_action1 = 'click@@clear@@send_keys@0.5@@click@@alert_text@@alert_accept@@click'
    # s,i,aa = wc.element_action(url1,position_str_user1,position_str_user_action1,d,"")
    # print("s:",s)
    # print("i:",i)
    # print("曲线图:",aa)

    # #获取input的值
    # # url1 = "http://10.8.8.22:8080/SPPP-web/contrastcurve/windPowerContrastCurve"
    # url1 = "http://10.64.14.144:18080/SPPP-web/datagovern/weatherStatistics/windSpeed"
    # position_str_user2 = "id|statisticsTable"
    # # position_str_user_action2 = "get_tubiao_data@_@日期=2022-05-17 00:30:00"  # 获取全部信息
    # position_str_user_action2 = "get_tubiao_data@日期,死数,占比,越限,占比,逻辑,占比,跳变,占比	正常	占比@日期=2022-05-23"
    #
    # s, i, aa = wc.element_action(url1, position_str_user2, position_str_user_action2, d, "")
    # print("s:", s)
    # print("i:", i)
    # print("机组信息:", aa)


    # # 机组信息
    # url1 = "http://10.64.14.182:18080/SPPP-web/fcstcastmodify/fcstcastModifyJump"
    # position_str_user1="id|pointTable"
    # position_str_user_action1 = "get_tubiao_data"  #获取全部信息
    # # # position_str_user_action1 = "get_tubiao_data@_@设备名称=风机_1"  # 获取某一行的值
    # # # position_str_user_action1 = "get_tubiao_data@_@设备名称=风机_1@2"  # 获取某一行的值
    # # # position_str_user_action1 = "get_tubiao_data@并网时间"   #获取操作这一列的信息
    # # # position_str_user_action1 = "get_tubiao_data@并网时间@_@4"  # 获取操作这一列的信息
    # # # position_str_user_action1 = "get_tubiao_data@并网时间@设备名称=风机_1@2"  #通过一个筛选项获取某一个值
    # # # position_str_user_action1 = "get_tubiao_data@并网时间@设备名称=风机_1"  #通过一个筛选项获取某一个值
    # # position_str_user_action1 = "get_tubiao_data@经度,并网时间@设备名称=风机_1#AND#电厂名称=龙头风电场@1"   #通过多个筛选项获取某几个值
    # s,i,aa = wc.element_action(url1,position_str_user1,position_str_user_action1,d,"")
    # print("s:",s)
    # print("i:",i)
    # print("机组信息:",aa)


''' 
    url1 = "http://10.8.8.132:18080/SPPP-web/plantCap/turnjsp"
    position_str_user1="id|plantId@@id|starttime@@id|endtime@@id|search"
    position_str_user_action1 = "do_select@瀚高风电厂2@text@@set_datetime@2021-10-25 10:00:00@@set_datetime@2021-11-25 10:00:00@@click"
    time.sleep(10)
    s,i,aa = wc.element_action(url1,position_str_user1,position_str_user_action1,d,"")
    print(s)
    print(i)

    position_str_user1="id|starttime"
    position_str_user_action1 = "set_datetime@2021-10-25 10:00:00"
    s,i,aa = wc.element_action(url1,position_str_user1,position_str_user_action1,d,"")
    print(s)
    print(i)

    position_str_user1="id|endtime"
    position_str_user_action1 = "set_datetime@2021-11-25 10:00:00"
    s,i,aa = wc.element_action(url1,position_str_user1,position_str_user_action1,d,"")
    print(s)
    print(i)
    position_str_user1="id|search"
    position_str_user_action1 = "click"
    s,i,aa = wc.element_action(url1,position_str_user1,position_str_user_action1,d,"")

    print(s)
    print(i)
'''
    #wc.quitdriver(d)
    
