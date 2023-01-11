

from datetime import datetime as dt

if __name__ == "__main__":

    str = "2021-10-6"
    time = dt.strptime(str,"%Y-%m-%d")
    str = time.strftime("%Y%m%d")
    print(str)
    
    #type = 'ini'
    # type = 'json'
    type = 'xml'
    #type = 'csv'
    #type = 'log'
    #type = 'aaaaaaaaaa'

    if type == 'ini':
        from inicfg import IniCfg
        #测试inicfg功能
        #测试静态读取
        print("-----测试IniCfg静态接口------")
        cfgpath = "E:/work/test/measureconf.ini"
        #测试正常获取
        key = "COUNT@@N"
        value = IniCfg.readvalue_static(cfgpath,key)
        print("[%s] value is [%s]" %(key,value))
        assert value == "87"
        #测试参数错误,option不存在
        key = "COUNT@@aaa"
        value = IniCfg.readvalue_static(cfgpath,key)
        print("[%s] value is [%s]" %(key,value))
        assert value == ""

        key = "ErrorSection@@"
        value = IniCfg.readvalue_static(cfgpath,key)
        print("[%s] value is [%s]" %(key,value))
        assert value is None

        #测试参数格式错误
        key = "COUNT@@"
        value = IniCfg.readvalue_static(cfgpath,key)
        print("[%s] value is [%s]" %(key,value))
        assert value is None
    

        #测试文件不存在
        cfgpath = "E:/work/test/measureconf_error.ini"
        key = "COUNT@@222"
        value = IniCfg.readvalue_static(cfgpath,key,"haha")
        print("[%s] value is [%s]" %(key,value))
        assert value is None

        #测试静态写入
        cfgpath = "E:/work/test/measureconf.ini"
        key = "COUNT@@N"
        ret = IniCfg.setvalue_static(cfgpath,key,"100")
        print(ret)
        value = IniCfg.readvalue_static(cfgpath,key)
        assert value == "100"
        ret = IniCfg.setvalue_static(cfgpath,key,"87")


        #测试对象接口
        print("-----测试IniCfg对象接口------")

        #测试无文件错误
        cfgpath = "E:/work/test/measureconf_error.ini"
        myinicfg_error = IniCfg(cfgpath)
        key = "COUNT@@N"
        value = myinicfg_error.readvalue(key)
        assert value is None


        cfgpath = "E:/work/test/measureconf.ini"
        myinicfg = IniCfg(cfgpath)

        #测试正常获取
        key = "COUNT@@N"
        value = myinicfg.readvalue(key)
        print("[%s] value is [%s]" %(key,value))
        assert value == "87"
        #测试参数错误,option不存在
        key = "COUNT@@aaa"
        value = myinicfg.readvalue(key)
        print("[%s] value is [%s]" %(key,value))
        assert value == ""

        key = "ErrorSection@@"
        value = myinicfg.readvalue(key)
        print("[%s] value is [%s]" %(key,value))
        assert value is None

        #测试参数格式错误
        key = "COUNT@@"
        value = myinicfg.readvalue(key)
        print("[%s] value is [%s]" %(key,value))
        assert value is None
    

        #测试文件不存在
        key = "COUNT@@222"
        value = myinicfg.readvalue(key,"haha")
        print("[%s] value is [%s]" %(key,value))
        assert value == "haha"

        #测试动态接口写入
        key = "COUNT@@N"
        ret = myinicfg.setvalue(key,"100")
        myinicfg.save()
        print(ret)
        value = IniCfg.readvalue_static(cfgpath,key)
        assert value == "100"
        ret = IniCfg.setvalue_static(cfgpath,key,"87")
    elif type == "json":
        from jsoncfg import JsonCfg

        # #测试文件不存在
        # cfgpath = "E:/work/test/hdrconf_error.json"
        # myjson = JsonCfg(cfgpath)
        # nodestr = "hds"
        # fltstr = "hds|src_hdr@analog_d#AND#target_hdr@analog_d_15"
        # keystr = "target_fields"
        # value = myjson.readvalue(nodestr,fltstr,keystr,"aaaa")
        #
        # # #测试正常读取
        # cfgpath = "E:/work/test/hdrconf.json"
        # myjson = JsonCfg(cfgpath)
        # nodestr = "hds"
        # fltstr = "hds|src_hdr@analog_d#AND#target_hdr@analog_d_15"
        # keystr = "target_fields"
        # value = myjson.readvalue(nodestr,fltstr,keystr,"aaaa")
        # # assert value == "maxvalue, maxtime | minvalue, mintime "
        # print(value)

        # #测试条件异常读取
        # cfgpath = "E:/work/test/hdrconf.json"
        # myjson = JsonCfg(cfgpath)
        # nodestr = "hds"
        # fltstr = "hds|src_hdr@analog_d#AND#"
        # keystr = "target_fields"
        # value = myjson.readvalue(nodestr,fltstr,keystr,"aaaa")
        # assert value is None
        # print(value)
        #
        # cfgpath = "E:/work/test/hdrconf.json"
        # myjson = JsonCfg(cfgpath)
        # nodestr = "hds"
        # fltstr = "hds@@@src_hdr@analog_d#AND#target_hdr@analog_d_15"
        # keystr = "target_fields"
        # value = myjson.readvalue(nodestr,fltstr,keystr,"aaaa")
        # assert value is None
        # print(value)
        #
        #
        # cfgpath = r"E:\work\test\aaa\a.json"
        # myjson = JsonCfg(cfgpath)
        # nodestr = "results@@index"
        # fltstr = "results|AttrCon@currentCity@青岛@@index|AttrCon@title@穿衣"
        # keystr = "zs"
        # value = myjson.readvalue(nodestr, fltstr, keystr, "aaaa")
        # assert value == "aaaa"
        # print(value)

        # cfgpath = "E:/work/test/hdrconf.json"
        cfgpath = 'D:\davinciapi\wen\hdrconf.json'
        myjson = JsonCfg(cfgpath)
        nodestr = "hds"
        # fltstr = "hds|src_hdr@analog_d#AND#target_hdr@analog_d_15"
        fltstr = "hds|AttrCon@src_hdr@analog_d#AND#AttrCon@target_hdr@analog_d_15"
        keystr = "target_fields"
        value = myjson.setvalue(nodestr,fltstr,keystr,"aaaa")
        myjson.save()
        print(value)

    elif type == "xml":
        from xmlcfg import XmlCfg
        #测试文件不存在
        # cfgpath = "E:/work/test/g_xgfsyzxx.xml"
        cfgpath = r"D:\davinciapi\wen\f_fgsztxx.xml"
        myobj = XmlCfg(cfgpath)
        nodestr = "key@@value@@time"
        # fltstr = "key|AttrCon@name@date@@value|AttrCon@order@1#AND#AttrCon@datatype@0"
        fltstr = "key|AttrCon@name@date@@value|AttrCon@order@1@@time|AttrCon@timetype@1"
        keystr = "AttrCon@format"
        value = myobj.readvalue(nodestr,fltstr,keystr,"aaaa")
        print(value)
        assert value == "yyyy-MM-dd"

        # b = myobj.setvalue(nodestr,fltstr,keystr,"dd/MM/yyyy")
        # print(b)
        # myobj.save()
        # value = myobj.readvalue(nodestr,fltstr,keystr,"aaaa")
        # print('@@@@@',value)
        # assert value == "dd/MM/yyyy"

    elif type == "csv":
        from csvcfg import CsvCfg

        cfgpath = "E:/work/test/tabmodule.csv"
        myobj = CsvCfg(cfgpath,"GBK")
        fltstr = "#IMODULEID@3"
        keystr = "STRMODULENAME"
        value = myobj.readvalue(fltstr,keystr,"aaaa")
        print(value)
        assert value == "rxftpserver"


        value = myobj.setvalue(fltstr,"IAUTHORITYCODE","4")
        print(value)
        pass
        
    elif type == "log":
        from logcfg import LogCfg
        
        cfgpath = "E:/work/test/mysqld.log"
        starttime = "2020-08-05T02:40:36.000000Z"
        endtime = "2020-08-05T02:40:43.000000Z"
        timeformat = "%Y-%m-%dT%H:%M:%S.%fZ"
        LogCfg.getmatchlines(cfgpath,starttime,endtime,"Warning",timeformat)

        cfgpath = "E:/work/test/rxsysmon.log"
        starttime = "2021-04-23 11:32:04"
        endtime = "2021-04-23 11:32:32"
        timeformat = "%Y-%m-%d %H:%M:%S"
        LogCfg.getmatchlines(cfgpath,starttime,endtime,"WARNING",timeformat)
    else:
        pass