
from datetime import datetime as dt

if __name__ == "__main__":

    # type = 'ini'
    type = 'json'
    # type = 'xml'
    # type = 'csv'
    # type = 'log'
    # type = 'aaaaaaaaaa'

    if type == 'ini':
        pass
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
        cfgpath = r"D:\davinciapi\wen\aa\a.json"
        myjson = JsonCfg(cfgpath)
        nodestr = "results@@index"
        fltstr = "index|title@穿衣"
        keystr = "zs"
        value = myjson.readvalue(nodestr, fltstr, keystr, "aaaa")
        assert value == "aaaa"
        print(value)

        # cfgpath = "E:/work/test/hdrconf.json"
        # myjson = JsonCfg(cfgpath)
        # nodestr = "hds"
        # fltstr = "hds|src_hdr@analog_d#AND#target_hdr@analog_d_15"
        # keystr = "target_fields"
        # value = myjson.setvalue(nodestr,fltstr,keystr,"aaaa")
        # myjson.save()
        # print(value)