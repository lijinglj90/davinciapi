import os
import time

adb = [
    #'python -m pip install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com',
	#'pip install openpyxl',
	#'pip install xlrd==1.2.0',
    #'pip install pandas',
    #'pip install selenium==4.1.0',
    #'pip install pyOpenSSL',
    #'pip install python-dateutil',
    #'pip install pycryptodome',
    #'pip install pymysql -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com',
    #'pip install test\mysqlclient-1.4.6-cp37-cp37m-win_amd64.whl',
    # 'yum install mysql-devel',
    # 'pip install mysqlclient',
    # 'yum install -y postgresql-devel',
    # 'pip install psycopg2',
    # 'pip install requests',
    # 'pip install chardet',
    ]
linuxadb = [  #全部使用的是root权限安装
    'pip3 install --upgrade pip -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com',
    # 'pip3 install pymysql',
    # 'pip3 install pycryptodome',
    # 'yum install -y postgresql-devel',
    # 'pip3 install psycopg2',
    # 'pip3 install requests',
    # 'pip3 install selenium==4.1.0',
    # 'pip3 install pandas',
    # 'pip3 install pyOpenSSL',
    # 'pip3 install chardet -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com',  #8.3
    # 'pip3 install openpyxl -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com',
    'pip3 install influxdb -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com',
]
for i in adb:
    time.sleep(1)
    d = os.popen(i)
    print(d.read())

time.sleep(15)
