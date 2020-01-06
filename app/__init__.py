#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   __init__.py.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/26 下午5:40   wangshuai      1.0         None
'''

# import lib
import os
from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from flask_cors import CORS


def create_app():
    """ factory function for creating flask application"""
    app = Flask(__name__)
    app.config.from_object('app.configs.config')
    app.config.from_object('app.configs.settings')
    return app


app = create_app()
CORS(app, supports_credentials=False)

db = SQLA(app)
migrate = Migrate(app, db)
from app.libs.security import MySecurityManager
from flask_appbuilder.menu import Menu

appbuilder = AppBuilder(app, db.session, menu=Menu(reverse=False), security_manager_class=MySecurityManager,
                        base_template='baseImgIcon.html')

from app import models, Admin, views
