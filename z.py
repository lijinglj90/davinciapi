# #
# import time
# from selenium import webdriver
#
# from selenium.webdriver.support.select import Select
# driver = webdriver.Chrome()
# # driver = webdriver.chrome()
# # driver.get('http://www.baidu.com')
#
# url = "http://10.8.8.26:18080/SPPP-web/login"
# driver.get(url)
# driver.find_element_by_id('username').send_keys('spfs')
# driver.find_element_by_id('password').send_keys('spfs')
# driver.find_element_by_id('submit').click()
# time.sleep(4)
# url = "http://10.8.8.26:18080/SPPP-web/spfsWeather/windSpeed"
# driver.get(url)
# el = driver.find_element_by_id('plantId')
# # select_value = el.get_attribute('value')
# a = []
# options_list=el.find_elements_by_tag_name('option')
#
# for i in options_list:
#     print(i)
#     print(i.text)
#     print("Value is:%s Text is:%s" % (i.get_attribute("value"), i.text))
#     a.append(i.text)
# # print(el)
# # print(options_list)
# print(a)
#
#
#


###############
import os
from pygetopt import *
from inicfg import IniCfg
#获取目录地址
CASEPATH = os.getcwd()
print(CASEPATH)
#
# pygetopt = getoptmain()
# print(pygetopt)
# mark = pygetopt['mark']
# file = pygetopt['file']
# path = pygetopt['path']
# baseevn = pygetopt['baseevn']
#
# if 'SpFcst' in path or 'SpFcst' in file:
#     print('haha')
# paras = [r'D:\davinciapi\wen\nrfmEfileToSim.ini','EFILE@@ceshi','']
# paras_gongcheng = [r'D:\davinciapi\wen\system.ini','project@@name','']
# status,info,value_gongcheng = IniCfg.readvalue_static(paras_gongcheng[0],paras_gongcheng[1],paras_gongcheng[2])
# print(status,info,value_gongcheng)
#
# paras_shujuku_IP = [fr'D:\davinciapi\wen\hdrpara.ini','dbconfig@@hd_db1_ip_1','']
# status0,info0,value_IP = IniCfg.readvalue_static(paras_shujuku_IP[0],paras_shujuku_IP[1],paras_shujuku_IP[2])
# print(status0,info0,value_IP)
# paras_shujuku_user = [fr'D:\davinciapi\wen\hdrpara.ini','dbconfig@@hd_db1_user','']
# status1,info1,value_user = IniCfg.readvalue_static(paras_shujuku_user[0],paras_shujuku_user[1],paras_shujuku_user[2])
# print(status1,info1,value_user)
# paras_shujuku_passwd = [fr'D:\davinciapi\wen\hdrpara.ini','dbconfig@@hd_db1_passwd','']
# status2,info2,value_passwd = IniCfg.readvalue_static(paras_shujuku_passwd[0],paras_shujuku_passwd[1],paras_shujuku_passwd[2])
# print(status2,info2,value_passwd)
# paras_shujuku_type = [fr'D:\davinciapi\wen\hdrpara.ini','dbconfig@@database1_type','']
# status3,info3,value_type = IniCfg.readvalue_static(paras_shujuku_type[0],paras_shujuku_type[1],paras_shujuku_type[2])
# print(status3,info3,value_type)
#
# # paras = [r'/home/sprixin/davinci/etc/system.ini','','']
# paras_shujuku_0 = [fr'/home/sprixin/davinci/usr/{value_gongcheng}/hdr/hdrpara.ini','','']
# print(paras_shujuku_0)
#
import socket
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP
print(extract_ip())
# print(value_IP,type(value_IP),extract_ip())
# if value_IP in '127.0.0.1' or value_IP == extract_ip():
#     print('4',extract_ip())



# a = ''
# a = None
# a = False
# a = '_'
# if not a:
#     print('shi kong ')
# else:
#     print('buweikong')



