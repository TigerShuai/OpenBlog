#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   admin.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/26 下午5:57   wangshuai      1.0         None
'''

# import lib
from flask import render_template
from app import appbuilder
from app.Admin.blogs_views import NotesTypeView, NotesView, PublicNotesView

appbuilder.add_view(
    NotesTypeView,
    '博客类型列表',
    category="文章",
)

appbuilder.add_view(
    NotesView,
    '博客列表',
    category="文章",
)

appbuilder.add_view(
    PublicNotesView,
    '公开博客',
    category="文章",
)

appbuilder.security_cleanup()  # 自动清理无应用权限


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )
