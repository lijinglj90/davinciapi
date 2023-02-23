from rdbobj import RdbObj
# 以下测试多个参数缺省
# paras = ['select * from biao','','','','','','']   #参数个数错误
# paras = ['select * from biao','','','','','']  #使用系统默认 LOCALHOST 3306 DAVINCI sa cast1234
# paras = ['select * from biao','','','','']     #同上
# paras = ['select * from biao','_','_']     #同上
# paras = ['select * from biao','_']     #同上
# paras = ['select * from biao']     #同上
# paras = ['']  #参数个数错误
# paras = []  #参数个数错误

#以下测试数据类型和环境变量的互斥关系
# paras = ['select * from biao','','','','','']  #全部使用系统默认QMYSQL LOCALHOST 3306 DAVINCI sa cast1234
# paras = ['select * from biao','','','','EnvFcst','']   #全部使用环境变量：
# paras = ['select * from biao','QMYSQL','','','','']  #使用用户传入QMYSQL LOCALHOST 3306 DAVINCI sa cast1234
# paras = ['select * from biao','QMYSQL','','','EnvFcst','']  #类型使用用户传入QMYSQL 其他使用环境变量
# paras = ['select * from biao','QKINGBASE','','','','']   #使用用户传入QMYSQL LOCALHOST 3306 DAVINCI sa cast1234
# paras = ['select * from biao','QKINGBASE','','','EnvFcst','']
# paras = ['select * from biao','ALL','','','EnvFcst','']
# paras = ['select * from biao','all','','','EnvFcst','']
# paras = ['select * from biao','all','','','','']
# paras = ['select * from biao','ALL','','','','']
#
#
# # #以下测试ip+端口号+库+用户名+密码 和环境变量的互斥关系
# # 执行的是Mysql数据库 10.8.8.26 5236 davinci_main_databak davinci_main_databak davinci
# paras = ['select * from biao','','10.8.8.26@5236@davinci_main_databak@davinci_main_databak@davinci','','','']
# # 执行的是达梦数据库 10.8.8.26 5236 davinci_main_databak davinci_main_databak davinci
# paras = ['select * from biao','','10.8.8.26@5236@davinci_main_databak@davinci_main_databak@davinci','','EnvFcst','']
# # 执行的是金仓数据库 10.8.8.26 5236 davinci_main_databak davinci_main_databak davinci
# paras = ['select * from biao','QKINGBASE','10.8.8.26@5236@davinci_main_databak@davinci_main_databak@davinci','','','']
# # 执行的是Mysql数据库 10.8.8.26 5236 davinci_main_databak davinci_main_databak davinci
# paras = ['select * from biao','ALL','10.8.8.26@5236@davinci_main_databak@davinci_main_databak@davinci','','','']
# # 执行的是达梦数据库 10.8.8.26 5236 davinci_main_databak davinci_main_databak davinci
# paras = ['select * from biao','all','10.8.8.26@5236@davinci_main_databak@davinci_main_databak@davinci','','EnvFcst','']
# # 执行的是Mysql数据库 10.8.8.26 3306 DAVINCI sa cast1234
# paras = ['select * from biao','','10.8.8.26@_@_@_@_','','','']
# # 执行的是达梦数据库 127.0.0.1 5236 davinci_xx_ davinci_main_databak davinci
# paras = ['select * from biao','','_@_@davinci_xx_@_@_','','EnvFcst','']
# # 执行的是Mysql数据库 LOCALHOST 52436 DAVINCI sa cast1234
# paras = ['select * from biao','ALL','_@52436@_@_@_','','','']
# # 执行的是达梦数据库 127.0.0.1 5236 davinci_main_databak davinci_main_databak dav_xx
# paras = ['select * from biao','all','_@_@_@_@dav_xx','','EnvFcst','']


#以下测试多个sql语句
#
# paras = ['select * from biao','QMYSQL','','','','QMYSQL@select * from biao_QMYSQL@@QKINGBASE@select * from biao_QKINGBASE@@QDMOCI@select * from biao_QDMOCI@@QPSQL@select * from biao_QPSQL@@QINSQL@select * from biao_QINSQL']
# paras = ['select * from biao','QMYSQL','','','','QMYSQL@select * from biao_QMYSQL@@QKINGBASE@select * from biao_QKINGBASE']
# paras = ['select * from biao','QMYSQL','','','','QDMOCI@select * from biao_QDMOCI']
# paras = ['select * from biao','QMYSQL','','','','']
# paras = ['select * from biao','','','','','']
# paras = ['select * from biao','','','','','QMYSQL@select * from biao_QMYSQL@@QKINGBASE@select * from biao_QKINGBASE']
paras = ['select * from biao','all','','','EnvFcst','QMYSQL@select * from biao_QMYSQL@@QKINGBASE@select * from biao_QKINGBASE']
# paras = ['select * from biao','all','','','','QDMOCI@select * from biao_QDMOCI']
# paras = ['select * from biao','ALL','','','','']

# paras = ['select * from biao','','','','','']



# QMYSQL@select * from biao_QMYSQL
# @@
# QKINGBASE@select * from biao_QKINGBASE
# @@
# QDMOCI@select * from biao_QDMOCI
# @@
# QPSQL@select * from biao_QPSQL
# @@
# QINSQL@select * from biao_QINSQL

l = len(paras)
print(l)
sqldata = {}
A = ['QMYSQL','QKINGBASE','QDMOCI','QPSQL','QINSQL']
if 0<l<7 and paras[0] != '':
    # sqldata = {}
    paras = paras + [''] * (6 - len(paras))
    print(paras)
    obj = RdbObj(paras[1], paras[2], paras[4])
    if paras[3] in ['_', '']:
        paras[3] = 3

    print('使用的数据类型是：',obj.mytype)


    if paras[1] in ['all','ALL','','_']:
        for i in A:
            sqldata[i] = paras[0]
        if paras[5]:
            print('buweikong')
            l = paras[5].split('@@')
            for j in l:
                z = j.split('@')
                sqldata[z[0]] = z[1]
    elif paras[5]:
        # print('不为空')
        sqldata[paras[1]] = paras[0]
        l = paras[5].split('@@')
        for j in l:
            z = j.split('@')
            sqldata[z[0]] = z[1]
    else:
        sqldata[paras[1]] = paras[0]

    print(sqldata)
    ssql = sqldata[obj.mytype]
    print(ssql)
    # status, info, data = obj.exec_querry(ssql, paras[3])
    # status, info, data = obj.exec_querry(paras[0], paras[3])
else:
    print(False, "参数个数错误", [])
	

# #coding=gbk
#导入psycopg2包和UUID包
#瀚高
# import psycopg2
# import uuid
# import datetime
# import time
# conn = psycopg2.connect(database="davinci", user="postgres", password="postgres", host="10.64.14.67", port="5432")
# # #建立游标，用来执行数据库操作
# cursor = conn.cursor()
# # # #执行SQL命令
# sql = "SELECT A.ID FROM analoginput A WHERE A.TYPE = ( SELECT M.ID FROM measurementtype M WHERE M.NAME = 'UAVG1') LIMIT 1"
# cursor.execute(sql)
# res = cursor.fetchall()
# print(res)
# cursor.close()
# #关闭数据库连接
# conn.close()
#
# #金仓
# import psycopg2
# conn = psycopg2.connect(database="test", user="system", password="system", host="10.8.8.201", port="54321")
# cursor = conn.cursor()
# # cursor.execute("create table PUBLIC.test0811(id integer,name varchar(23),age integer)")
# # cursor.execute("insert into PUBLIC.test0811 values(%s,%s,%s)", (1, "xiexie1", 11))
# # cursor.execute("insert into PUBLIC.test0811 values(%s,%s,%s)", (2, "xiexie2", 12))
# # # cursor.execute("drop table PUBLIC.test0811")
# # cursor.commit()
# cursor.execute("select * from PUBLIC.test0811")
# rows = cursor.fetchall()
# print(rows)
# cursor.close()
# # #关闭数据库连接
# cursor.close()
# # 原文链接：https://blog.51cto.com/u_13646489/2786177
# 金仓原文链接：https://zhuanlan.zhihu.com/p/398579679


# #达梦
# import dmPython
# try:
#     conn = dmPython.connect(user='SYSDBA', password='SYSDBA', server='10.8.8.26', port=5236)
#     cursor = conn.cursor()
#     print('python: conn success!')
#     cursor.execute("SELECT M.ID FROM DAVINCI.measurementtype M WHERE M.NAME = 'UAVG1'")
#     values = cursor.fetchall()
#     print(values)
#     conn.close()
# except Exception as err:
#     print(err)
# conn.close()
# # #关闭数据库连接
# cursor.close()
