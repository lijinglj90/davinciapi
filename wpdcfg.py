
import logger as lg
import chardet
from splitcfg import SplitSymbol

class WpdCfg:
    ''' wpd文件操作'''

    def __init__(self,wpdpath:str, encoding=''):
        '''构造函数
            功能：
                通过传入参数创建文件对象
            参数：
                wpdpath，文件的路径，建议为绝对路径
        '''
        self.__end = wpdpath.split(".")[-1].strip().lower()
        self.__wpdpath__ = wpdpath

        get_encoding = self.get_encoding(self.__wpdpath__)
        if encoding:  # 用户指定编码格式  encoding不为空
            self.__encoding = encoding  # 使用用户指定编码格式
        else:  # 用户没有指定编码格式
            if get_encoding:  # 程序自动获取文件编码格式，不为空
                self.__encoding = get_encoding  # 使用程序获取的编码格式
            else:
                self.__encoding = 'utf-8'  # 给一个默认值


    def get_encoding(self,cfgpath):
        # 二进制方式读取，获取字节数据，检测类型
        with open(cfgpath, 'rb') as f:
            data = f.read()
            return chardet.detect(data)['encoding']

    def listnum(self, s:str):
        l = []
        try:
            if s == '':
                return True, l
            s1 = s.split(SplitSymbol.SYMBOL_BETWEEN_METAINLIST)   #','
            for r in s1:
                if '-' in r:
                    rr = r.split('-')
                    for a in range(int(rr[0]), int(rr[1]) + 1):
                        print(a)
                        l.append(str(a))
                else:
                    int(r)
                    l.append(r)
            # print(l)
            return True, l
        except Exception as e:
            return False, e


    def readvalue_wpd(self, rows:str, lines:str):
        stinfo = "readvalue调用，cfgpath:%s rows:%s lines:%s" % (self.__wpdpath__, rows, lines)
        lg.myloger.info(stinfo)

        encodestr = self.__encoding
        # print(encodestr)

        file = self.__wpdpath__

        status1, rowsl = self.listnum(rows)
        # print('rows:', status1, rowsl)
        status2, linesl = self.listnum(lines)
        # print('lines:', status2, linesl)

        if rows == '' or rowsl == []:
            info = '传入的ID号%s错误，不能为空' % rows
            lg.myloger.error(info)
            return False, info, None

        if status1 and status2:
            # print(True)
            pass
        else:
            # print(False)
            info = '传入的ID号%s，或者列信息%s，不正确' % (rows, lines)
            lg.myloger.error(info)
            return False, info, None

        data = []
        n=0
        with open(file, 'r', encoding=encodestr) as f1:
            line1 = f1.readlines()
            # print(len(line1))
            numline1 = len(line1)
            for line in line1:
                n += 1
                if line.startswith('@'):
                    dataline = line.split()
                    if dataline[1] != 'id':
                        info = '请检查文件%s，文件没有单独id列' % file
                        lg.myloger.error(info)
                        return False, info, None
                if line.startswith('#'):
                    dataline = line.split()
                    for r in rowsl:
                        if dataline[1] == r:
                            new_dataline = []
                            if lines:
                                for l in linesl:
                                    if int(l) >= len(dataline):
                                        info = '请检查输入的下标%s，超出文件最大下标值' % lines
                                        lg.myloger.error(info)
                                        return False, info, None
                                    new_dataline.append(dataline[int(l)])
                                data.append(new_dataline)
                            else:
                                data.append(dataline)
                        else:
                            continue
            if n == numline1 and data == []:
                info = '传入的ID号%s，没有匹配到' % rows
                lg.myloger.error(info)
                return False, info, None
        if len(data) == 1:
            data = data[0]
        return True,'', data