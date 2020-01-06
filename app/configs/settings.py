"""
  Created by wangshuai on 2019-07-24 16:43
  Any suggesstions, please send mail to 15617699933@163.com
"""

# -*- coding: utf-8 -*-
import os

DEBUG = True
PROXY_FIX_APP = os.getenv('PROXY_FIX_APP', False)

default_user_db_uri = "postgresql://当前数据库用户:@127.0.0.1/数据库名"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default_user_db_uri)


SQLALCHEMY_RECORD_QUERIES = False  # 慢查询状态是否启用
FLASKY_DB_QUERY_TIMEOUT = 0.01  # 慢查询记录查询阈值

# 阿里云图片处理相关
OSS_KEY = 'You_KEY'
OSS_SECRET = 'You_SECRET'
OSS_URL = 'Bucket 域名'
OSS_NAME = 'You_bucket_Name' #bucket 名称

OSS_IMGSNAME = 'imgs/' #imgs
OSS_VIDEO = 'video/'# video
USER_IP = '' #链接修改为自有域名调用，非必要设置
STATIC_UPLOAD_PATH = '/app/static/upload/'#本地上传路径
IMGS_TYPE = '?x-oss-process=style/bolgs' #样式相关，非必要设置


