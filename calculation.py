import math

def air_density_one(wen, ya):
    # 单个值的空气密度
    air_v = 1.293*273.15 / (273.15+float(f'{wen}')) *float(f'{ya}') /1013
    # air_v = "%.3f" % float(1.294*273.15 / (273.15+float(f'{wen}')) *float(f'{ya}') /1013)
    return air_v

def air_density(wen_list, ya_list):
    # 空气密度
    air_v = []
    if type(wen_list)==list and type(ya_list)==list and len(wen_list) == len(ya_list):
        air_list = [1.293*273.15 / (273.15+float(f'{wen}')) *float(f'{ya}') /1013 for wen, ya in zip(wen_list, ya_list)]
        # abs_tq = [(1-abs(x - y)/records_Sop) for x, y in zip(records_Pmi, records_Ppi)]
        V = sum(air_list)/len(wen_list)
        air_v.append(str(V))
        return air_v
    else:
        return air_v

def Wind_power_density(wen_list, ya_list,UAVG4_list):
    WpowerV = []
    # 风功率密度
    """
    midu_list----i个点的空气密度
    UAVG4_list----i个点的风速（m/s）值
    midu_cube_list---i个点的空气密度的立方和
    UAVG4_cube_list---i个点的风速的立方和
    """
    print(len(wen_list),len(ya_list),len(UAVG4_list))
    if len(wen_list) == len(ya_list) == len(UAVG4_list):
        midu_list = [(1.293*273.15 / (273.15+ wen) * ya /1013) for wen, ya in zip(wen_list, ya_list)]
        # print('midu_list:',midu_list)
        midu_cube_list=[midu **3 for midu in midu_list]
        # print('midu_cube_list:',midu_cube_list)
        UAVG4_cube_list=[UAVG4 ** 3 for UAVG4 in UAVG4_list]
        # print('UAVG4_cube_list:',UAVG4_cube_list)
        V = sum([midu_cube * UAVG4_cube for midu_cube, UAVG4_cube in zip(midu_cube_list,UAVG4_cube_list)])/(2*len(UAVG4_list))
        WpowerV.append(str(V))
        # print(WpowerV)
        return WpowerV
    else:
        return WpowerV

def get_average(records):
    # 算数平均
    averageV= []
    V = sum(records) / len(records)
    averageV.append(str(V))
    # print(averageV)
    return averageV

def get_average_jing(records):
    # 算术平均，风速<0时，风速当0算
    averageV = []
    new_records = [0 if i <=0 else i for i in records]
    # print(new_records)
    V = sum(new_records) / len(new_records)
    averageV.append(str(V))
    # print(averageV)
    return averageV

def get_sum(records):
    # 求和
    sumV= []
    V = sum(records)
    sumV.append(str(V))
    # print(sumV)
    return sumV

def get_add(A,B):
    # 两数相加
    accuracyV = []
    V = A+B
    accuracyV.append(str(V))
    return accuracyV

# def get_feng_accuracy(rmseV):
#     # 精度，rmseV：均方根误差
#     accuracyV = []
#     V = 1-rmseV
#     accuracyV.append(str(V))
#     return accuracyV
#
# def get_guang_accuracy(maeV):
#     # 精度 ，maeV：平均绝对误差
#     accuracyV =[]
#     V = 1-maeV
#     accuracyV.append(str(V))
#     return accuracyV
#
# def get_zql(rmseV):
#     # 准确率 ，rmseV：均方根误差
#     zqlV = []
#     V = 1-rmseV
#     zqlV.append(str(V))
#     return zqlV

def get_sub(A,B):
    # 两数相减
    accuracyV = []
    V = A-B
    accuracyV.append(str(V))
    return accuracyV


def get_mse(records_Pmi,records_Ppi):
    """
    均方误差 估计值与真值 偏差
    """
    mseV = []
    if len(records_Pmi) == len(records_Ppi):
        V = sum([(x - y) ** 2 for x, y in zip(records_Pmi, records_Ppi)]) / len(records_Pmi)
        return mseV.append(str(V))
    else:
        return mseV


def get_rmse(records_Pmi,records_Ppi,records_Sop):
    # 短期均方根误差
    """
    Pmi-----i时刻的实际功率；
    Ppi-----i时刻的预测功率；
    Sop-----风电场的开机总容量；可配置成预测功率、实发功率和装机容量
    """
    rmseV = []
    if len(records_Pmi) == len(records_Ppi):
        mse = sum([(x - y) ** 2 for x, y in zip(records_Pmi, records_Ppi)]) / len(records_Pmi)
        V = "%.3f" %float(math.sqrt(mse) / records_Sop)
        rmseV.append(str(V))
        return rmseV
    else:
        return rmseV

def get_mae(records_Pmi,records_Ppi,records_Sop):
    """
    平均绝对误差
    Pmi-----i时刻的实际功率；
    Ppi-----i时刻的预测功率；
    Sop-----风电场的开机总容量；可配置成预测功率、实发功率和装机容量
    """
    maeV =[]
    abs_t = []
    if len(records_Pmi) == len(records_Ppi):
        abs_tq = [abs(x - y)/records_Sop for x, y in zip(records_Pmi, records_Ppi)]
        # print(abs_tq)
        for i,k in enumerate(records_Pmi):
            if k<records_Sop*0.03:
                continue
            abs_t.append(abs_tq[i])
        # print(abs_t)
        # print(len(abs_t))
        V = sum(abs_t) / len(abs_t)
        maeV.append(str(V))
        return maeV
    else:
        return maeV

def get_colrel(records_Pmi,records_Ppi):
    # 相关性系数
    """
    Pmi-----i时刻的实际功率；
    Ppi-----i时刻的预测功率；
    """
    colrelV= []
    if len(records_Pmi) == len(records_Ppi):
        average_Pmi = get_average(records_Pmi)
        average_Ppi = get_average(records_Ppi)
        fenzi = sum([(x - average_Pmi) * (y - average_Ppi) for x, y in zip(records_Pmi, records_Ppi)])
        fenmu = math.sqrt(sum(y for y in ((y - average_Ppi) ** 2 for y in records_Ppi)) * sum(
            x for x in ((x - average_Pmi) ** 2 for x in records_Pmi)))
        V= fenzi / fenmu
        # print(colrelV)
        colrelV.append(str(V))
        return colrelV
    else:
        return colrelV

# def get_dq_qualify(records_Pmi,records_Ppi,records_Sop):
#     #短期--合格率
#     """
#     Pmi-----i时刻的实际功率；
#     Ppi-----i时刻的预测功率；
#     """
#     dq_qualifyV = []
#     if len(records_Pmi) == len(records_Ppi):
#         abs_tq = [(1-abs(x - y)/records_Sop) for x, y in zip(records_Pmi, records_Ppi)]
#         q_list = list(filter(lambda z: z >= 0.8, abs_tq))
#         # print(q_list)
#         V = len(q_list)/len(abs_tq)
#         return dq_qualifyV.append(str(V))
#     else:
#         return dq_qualifyV
#
# def get_cdq_qualify(records_Pmi,records_Ppi,records_Sop):
#     #超短期--合格率
#     """
#     Pmi-----i时刻的实际功率；
#     Ppi-----i时刻的预测功率；
#     """
#     cdq_qualifyV = []
#     if len(records_Pmi) == len(records_Ppi):
#         abs_tq = [(1-abs(x - y)/records_Sop) for x, y in zip(records_Pmi, records_Ppi)]
#         q_list = list(filter(lambda z: z >= 0.85, abs_tq))
#         # print(q_list)
#         V = len(q_list) / len(abs_tq)
#         return cdq_qualifyV.append(str(V))
#     else:
#         return cdq_qualifyV

def get_qualify(records_Pmi,records_Ppi,records_Sop,ratio):
    #合格率(短期合格率系数为0.8，超短期合格率为0.85)
    """
    Pmi-----i时刻的实际功率；
    Ppi-----i时刻的预测功率；
    """
    cdq_qualifyV = []
    if len(records_Pmi) == len(records_Ppi):
        abs_tq = [(1-abs(x - y)/records_Sop) for x, y in zip(records_Pmi, records_Ppi)]
        q_list = list(filter(lambda z: z >= ratio, abs_tq))
        # print(q_list)
        V = len(q_list) / len(abs_tq)
        cdq_qualifyV.append(str(V))
        return cdq_qualifyV
    else:
        return cdq_qualifyV

#最大误差合格率
# def get_max_feng_errorlv(max_error):
#     """
#     风--最大误差合格率
#     """
#     meqV = []
#     if len(max_error)>0:
#         me_list = list(filter(lambda x: x <=0.25, max_error))
#         print(me_list)
#         V =len(me_list)/len(max_error)
#         # print(meqV)
#         meqV.append(str(V))
#         return meqV
#     else:
#         return meqV
#
# def get_max_guang_errorlv(max_error):
#     """
#     光伏--最大误差合格率
#     """
#     meqV =[]
#     if len(max_error)>0:
#         me_list = list(filter(lambda x: x <=0.2, max_error))
#         print(me_list)
#         V=len(me_list)/len(max_error)
#         # print(meqV)
#         meqV.append(str(V))
#         return meqV
#     else:
#         return meqV

def get_max_errorlv(max_error,ratio):
    """
    最大误差合格率（风系数为：0.25 光伏系数为：0.2）
    """
    meqV =[]
    if len(max_error)>0:
        me_list = list(filter(lambda x: x <= ratio, max_error))
        print(me_list)
        V=len(me_list)/len(max_error)
        # print(meqV)
        meqV.append(str(V))
        return meqV
    else:
        return meqV

def get_er_Harmonic_mean(records_Pfi,records_Pri,records_Sop):
    """
    求第二小时调和平均数准确率
    Pmi-pri----i时刻的实际功率；
    Ppi-pfi----i时刻的预测功率；
    Sop-----风电场的开机总容量；可配置成预测功率、实发功率和装机容量
    """
    erhmV = []
    d_list = []
    if len(records_Pfi) == len(records_Pri):
        for i in range(len(records_Pfi)):
            if (records_Pfi[i] <= records_Sop*0.03) and (records_Pri[i] <=records_Sop*0.03):
                d_list.append(i)
                # print(records_Pfi[i],records_Pri[i])
        for i in d_list:
            del records_Pfi[i]
            del records_Pri[i]
        # print(len(records_Pri))
        # print(d_list)

        he = sum((abs(pri - pfi)) for pri, pfi in zip(records_Pri, records_Pfi))
        V = 1-2*sum(((abs((pri / (pri+pfi) - 0.5))) * ((abs(pri-pfi))/ he ) )for pri, pfi in zip(records_Pri, records_Pfi))
        # print(V)
        erhmV.append(str(V))
        return erhmV
    else:
        return erhmV

def get_day_jiange(interval,records):
    # 日实际发电量，日理论发电量，日累计辐照量，日累计水平总辐射量
    """
    interval---时间间隔（60、300、900）
    records-----列表形式：i时刻的实际功率，i时刻的预测功率，i时刻的辐照度，i时刻的水平辐照度；
    """
    # print(sum(records_Pmi))
    dayjiangelV = []
    V= interval/3600 * sum(records)
    dayjiangelV.append(str(V))
    return dayjiangelV

def get_day_dengxiao(interval,records_Pmi,records_Sop):
    # 日有效利用小时数（等效利用时间）
    """
    interval---时间间隔（60、300、900）
    Pmi-----i时刻的实发功率；
    Sop-----风电场的开机总容量；可配置成预测功率、实发功率和装机容量
    """
    # 时间间隔*当日实发功率加总/装机/3600
    dengxiaoV = []
    V= interval *sum(records_Pmi)/3600/records_Sop
    dengxiaoV.append(str(V))
    return dengxiaoV

def get_day_rizhao(interval,records):
    # 累计日照小时数
    """
    interval---时间间隔（60、300、900）
    records----白天时段辐照度列表
    """
    # 时间间隔*当日实发功率加总/装机/3600
    rizhaoV = []
    records_new = list(filter(lambda z: z >= 0, records))
    # print(records_new)
    V= len(records_new) * interval /3600
    rizhaoV.append(str(V))
    return rizhaoV




if __name__ == '__main__':
    pass



