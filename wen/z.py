# import time
# from selenium import webdriver
# driver = webdriver.Chrome()
# # driver.get('http://www.baidu.com')
#
# url = "http://10.64.14.70:18080/SPPP-web/login"
# driver.get(url)
# driver.find_element_by_id('username').send_keys('test')
# driver.find_element_by_id('password').send_keys('Test123456')
# driver.find_element_by_id('submit').click()
# time.sleep(4)
# url = "http://10.64.14.70:18080/SPPP-web/theoretical/outWindObstructed"
# driver.get(url)
# el = driver.find_element_by_id('oTable')
# print(el)
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

import os
# def find(dir, name):
#     # print(dir)
#     fuzzy_find_list = []
#     for i in [x for x in os.listdir(dir) if os.path.isfile(os.path.join(dir, x)) and name in os.path.splitext(x)[0]]:
#         print(os.path.join(dir, i))
#         fuzzy_find_V = os.path.join(dir, i)
#         fuzzy_find_list.append(fuzzy_find_V)
#
#     # os.path.isfile() 需要完整路径或者相对当前目录的相对路径
#     # for i in [x for x in os.listdir(dir) if os.path.isdir(os.path.join(dir, x))]:
#     #     if os.listdir(os.path.join(dir, i)):
#     #         # 防止因为权限问题报错
#     #         try:
#     #             find(os.path.join(dir, i), name)
#     #         except:
#     #             pass
#     return fuzzy_find_list
#
#
# find(r'D:\用例设计器使用\casedesigner', 'test')
# CheckType = 1
CheckType = []
if CheckType:
    print('不为控股')
else:
    print('jjjj')
