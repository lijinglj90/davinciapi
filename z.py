#
import time
from selenium import webdriver

from selenium.webdriver.support.select import Select
driver = webdriver.Chrome()
# driver = webdriver.chrome()
# driver.get('http://www.baidu.com')

url = "http://10.8.8.26:18080/SPPP-web/login"
driver.get(url)
driver.find_element_by_id('username').send_keys('spfs')
driver.find_element_by_id('password').send_keys('spfs')
driver.find_element_by_id('submit').click()
time.sleep(4)
url = "http://10.8.8.26:18080/SPPP-web/spfsWeather/windSpeed"
driver.get(url)
el = driver.find_element_by_id('plantId')
# select_value = el.get_attribute('value')
a = []
options_list=el.find_elements_by_tag_name('option')

for i in options_list:
    print(i)
    print(i.text)
    print("Value is:%s Text is:%s" % (i.get_attribute("value"), i.text))
    a.append(i.text)
# print(el)
# print(options_list)
print(a)


# print(select_value)


# tbody_list = el.find_elements("tag name", "tbody")  # tbody对象列表
# print(tbody_list)
# time.sleep(30)
#
# tbody_tr_list = tbody_list[0].find_elements("tag name", "tr")
# # print(tbody_tr_list)
# print(len(tbody_tr_list))
# tbody_td_list_list = []
# lj = 0
# for i in tbody_tr_list:
#
#     tbody_td_list_v = i.find_elements("tag name", "td")
#     lj += 1
#     for j in tbody_td_list_v:
#         z = j.get_attribute("innerText")
#         print(z)
#         tbody_td_list_list.append(z)
# print(lj)
# print(tbody_td_list_list)
#
#
#



# def cmp_part(file1:str,file2:str,encodestr,Leftn,rightn):
#     status = True
#     try:
#         if Leftn:
#                 Leftn = eval(Leftn)
#         if rightn:
#             rightn = eval(rightn)
#         print('Leftn:',Leftn, 'rightn:',rightn)
#     except Exception as e:
#         info = '输入的行号有误，报错信息:' + str(e)
#         print(False, info)
#     with open(file1, 'r', encoding=encodestr) as f1, open(file2, 'r', encoding=encodestr) as f2:
#         line1 = f1.readlines()
#         line2 = f2.readlines()
#         print(len(line1))
#         if len(line1) != len(line2) or len(line1)<1:   #pass
#             print('两个文件大小不一样，或者文件为空')
#             status = False
#             return status
#         elif Leftn>len(line1):
#             print('起始行号超出文件最大行数')
#             return False
#         elif rightn:
#             if rightn >= len(line1) or rightn<=Leftn or rightn < 1:
#                 print('结束行号超出文件最大行数、不正确、小于起始行号')
#                 return False
#         elif not rightn:
#             rightn = len(line1)
#
#         for i in range(0, len(line1)):
#             if i >= Leftn - 1 and i <= rightn - 1:
#                 b1 = line1[i]
#                 b2 = line2[i]
#                 # print(b1)
#                 # print(b2)
#                 if b1 != b2:
#                     status = False
#                     return status
#     return status
# #utf-8
# # c = cmp_part(r'D:\davinciapi\case\zz\对比后删除A\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\case\zz\对比后删除B\farm1_20220816_0000_DQ.wpd','gb2312','4','9')
# # c = cmp_part(r'D:\davinciapi\case\zz\对比后删除A\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\case\zz\对比后删除B\farm1_20220816_0000_DQ.wpd','utf-8','4','9')
# # c = cmp_part(r'D:\davinciapi\case\zz\对比后删除A\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\case\zz\对比后删除B\farm1_20220816_0000_DQ.wpd','gb2312','108','4')
# # c = cmp_part(r'D:\davinciapi\case\zz\对比后删除A\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\case\zz\对比后删除B\farm1_20220816_0000_DQ.wpd','gb2312','100','')
# # # c = cmp_part(r'D:\davinciapi\case\zz\对比后删除B\A\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\case\zz\对比后删除B\A\farm1_20220816_0000_DQ.wpd','gb2312','','4')
# # # c = cmp_part(r'D:\davinciapi\case\zz\对比后删除B\B\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\case\zz\对比后删除B\A\farm1_20220816_0000_DQ.wpd','gb2312','','4')
# #
# # 获取文件编码类型
# import chardet
# import re
# def get_encoding(file):
#     # 二进制方式读取，获取字节数据，检测类型
#     with open(file, 'rb') as f:
#         data = f.read()
#         return chardet.detect(data)['encoding']
#
# def listnum(s:list):
#     l = []
#     try:
#         for r in s:
#             if '-' in r:
#                 rr = r.split('-')
#                 for a in range(int(rr[0]), int(rr[1]) + 1):
#                     print(a)
#                     l.append(str(a))
#             else:
#                 int(r)
#                 l.append(r)
#         # print(l)
#         return True,l
#     except Exception as e:
#         return False,e
#
# # def cmp_wpd(file1:str,file2:str,encodestr,rows=[],lines=[]):
# def cmp_wpd(file1: str, encodestr, rows=[], lines=[]):
#     status = True
#     encodestr = get_encoding(file1)
#     print(encodestr)
#
#     status1, rows = listnum(rows)
#     print('rows:',status1, rows)
#     status2, lines = listnum(lines)
#     print('lines:',status2, lines)
#     if rows == []:
#         info = '传入的ID号%s不能为空' % rows
#         print(info)
#         return False, info
#     if status1 and status2:
#         # print(True)
#         pass
#     else:
#         # print(False)
#         info = '传入的ID号%s，或者列信息%s，不正确' % (rows, lines)
#         print(info)
#         return False, info
#
#     data = []
#     with open(file1, 'r', encoding=encodestr) as f1:
#         line1 = f1.readlines()
#         print(len(line1))
#         for line in line1:
#             if line.startswith('@'):
#                 dataline = line.split()
#                 if dataline[1] != 'id':
#                     info = '请检查文件%s，文件没有单独id列' %file1
#                     return False,info
#             if line.startswith('#'):
#                 dataline = line.split()
#                 for r in rows:
#                     if dataline[1] == r:
#                         print(dataline)
#                         # dataline = dataline[0:4]
#                         new_dataline = []
#                         if lines:
#                             for l in lines:
#                                 new_dataline.append(dataline[int(l)])
#                             data.append(new_dataline)
#                         else:
#                             data.append(dataline)
#                     else:
#                         continue
#     return data
# cmp_wpd(r'D:\davinciapi\wen\farm1_20220816_0000_DQ.wpd',r'D:\davinciapi\wen\farm10001.csv','',10,106)
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',['31'],[])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',['31-33'],[])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',['31-33','40'],[])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',[],[])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',['31'],['5'])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',['31-33'],['5'])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',['31-33','40'],['5-7'])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',['31-33','40'],['5-7','11'])
# d = cmp_wpd(r'D:\davinciapi\wen\2022-09-02.wpd','',[],[])
# d = cmp_wpd(r'D:\davinciapi\wen\farm1_20220816_0000_DQ.wpd','',['31-33','40'],['5-7','11'])
# print(d)
# print(e)

# import pymysql
# host='10.64.14.69'
# port = 3306
# database = 'davinci'
# user = 'sa'
# passwd = 'cast1234'
#
# # sql = 'select FACTOR_VALUE,P from powercurve'
# # sql = 'SELECT AVERAGE FROM hdranastat5m20220925 WHERE ID=49'
# sql = "SELECT AVERAGE FROM hdranastat5m20220925 WHERE id=49 AND hdtime <= '2022-09-25 12:00:00' "
# # db = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=database,charset='utf8')
# db = pymysql.connect(host=host, port=int(port), user=user, passwd=passwd, db=database)
#         # 使用cursor()方法获取操作游标
# cursor = db.cursor()
# cursor.execute(sql)
# # 获取所有记录列表
# results = cursor.fetchall()
# print('results:',results,type(results))
#
# fields = cursor.description
# print('fields:',fields,type(fields))
#
# cursor.close()
# db.close()  #关闭数据库的连接

# mylist = [1,2,2,2,2,3,3,3,4,4,4,4]
# myset = set(mylist)  #myset是另外一个列表，里面的内容是mylist里面的无重复 项
# for item in myset:
#   print("the %d has found %d" %(item,mylist.count(item)))








# a = True
# b = True
# c= True
# if a and b and c:
#     print('TT')
# else:
#     print('dd')





# import os
# CASEPATH = os.getcwd()
# emailfilepath = rf'{CASEPATH}\Report\report.html'
# print(emailfilepath)



