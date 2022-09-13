#coding:utf-8

'''
    配置使用分隔符定义
'''

class SplitSymbol(object):
    '''
        为了简化自动化测试参数配置和解析中分隔符的使用统一和减少出错，在此统一定义各级分隔符，包括如下定义：
            1）命令参数分隔符“~”。为了简化配置，把不定个数的参数用“命令参数分隔符”连接，后续功能业务自行约定和校验
            2）并联分隔符#AND#。用于
            3）列表分隔符“,”。用于列表转换为字符串时使用
            4) 层级分隔符"@@"。用于模型层级之间的分隔符号
            5）条件因素分隔符“@”。用于定义一个条件相关元素之间的分隔，如xml中的“属性@属性名@属性值”
            6）条件作用分隔符“|”。用于定义条件与作用对象的分隔符

        用法：
            模块中

    '''
    SYMBOL_BETWEEN_ARGS = "~"
    SYMBOL_BETWEEN_METAINLIST = ","
    SYMBOL_BETWEEN_MODELLEVEL = "@@"
    SYMBOL_COMBINE_META = "#AND#"
    SYMBOL_COMBINE_OR_META = "#OR#"
    SYMBOL_BETWEEN_ELEMENTS_IN_CONDITION = "@"
    SYMBOL_BETWEEN_OBJECT_AND_CONDITION = "|"
    SYMBOL_COMPARE_EQUAL = "="

