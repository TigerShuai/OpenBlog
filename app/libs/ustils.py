#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   ustils.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/7/31 下午4:44   wangshuai      1.0         None
'''

# import lib
import datetime


def sysTime_y():
    return datetime.datetime.now().strftime('%Y')  # 系统当前年


def sysTime_m():
    return datetime.datetime.now().strftime('%m')  # 系统当前月


def sysTimey_d():
    return datetime.datetime.now().strftime('%d')  # 系统当前日


def sysTime_hour():
    return datetime.datetime.now().strftime('%H')  # 系统当前时


def sysTime_minute():
    return datetime.datetime.now().strftime('%M')  # 系统当前分


def sysTimey_second():
    return datetime.datetime.now().strftime('%S')  # 系统当前秒


def sysTime_ymd():
    return datetime.datetime.now().strftime('%Y-%m-%d')  # 系统当前年月日


def sysTime_ym():
    return datetime.datetime.now().strftime('%Y-%m')  # 系统当前年月


def sysTime_ymdhm():
    sysTime_ymdhm = datetime.datetime.now().strftime('%Y-%m-%d/%H:%M')
    return sysTime_ymdhm


# timezoneChina = pytz.timezone('Asia/Shanghai')  #中国时区

def sysTime_ymd_nextDay():
    '''
    明天年月日
    :return:
    '''
    nextDay = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
    return nextDay
