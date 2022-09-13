import os
import re
import datetime

time_regs = {
    '%Y-%m-%d %H:%M:%S':r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})',
    '%Y-%m-%dT%H:%M:%S.%fZ':r'(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2}:\d{1,2}.\d{6}Z)',
    'YYYY-mm-dd hh:MM:ss':r'(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})',
    '%Y-%m-%d':r'(\d{4}-\d{1,2}-\d{1,2})'
}

class LogCfg:
    def __init__(self):
        pass

    @staticmethod
    def getmatchlines(logfilepath:str, starttime:str, endtime:str, fltstr:str, timeformat:str):
        if not os.path.isfile(logfilepath):
            print(">> 无此文件，请核对路径[%s]" % logfilepath)
            return None
        logFile = open(logfilepath, 'r+')
        lines = logFile.readlines()

        if not timeformat in time_regs.keys():
            print("程序错误：目前不支持[%s]时间格式，请联系研发人员" % timeformat)
            return None
        pattern = re.compile(time_regs[timeformat])
        pattern1 = re.compile(fltstr)
        rtlines = ""

        bfindstart = False
        for line in lines:
            #获取时间过滤
            result = pattern.findall(line)

            if result is None or len(result) == 0:
                continue
            else:
                time = datetime.datetime.strptime(result[0], timeformat)
                start = datetime.datetime.strptime(starttime, timeformat)
                end = datetime.datetime.strptime(endtime, timeformat)

                diff1 = time - start 
                diff2 = time - end
                if (diff1.days*86400 + diff1.seconds) >= 0 :   
                    if not bfindstart: #确定第一条记录
                        bfindstart = True
                if not bfindstart:
                    continue

                if (diff2.days*86400 + diff2.seconds) > 0: #确定时间不匹配得第一行，跳出
                    break
                    
            #正则表达式匹配
            if fltstr is None or fltstr == "":
                print(line)
                pass
            else:
                result1 = pattern1.findall(line)
                
                if len(result1) < 1:
                    pass 
                else:
                    rtlines += line
                    
        #关闭文件
        logFile.close()
        print(rtlines)
        return rtlines

