#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   baseModelView.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/9/23 上午11:10   wangshuai      1.0         None
'''

# import lib
from flask import flash
from flask_appbuilder import ModelView, action, has_access
from flask_appbuilder.models.mixins import AuditMixin
from werkzeug.utils import redirect


class MyModelView(AuditMixin, ModelView):
    page_size = 25

    @has_access
    @action("muldelete", "删除", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())

    def verify(self, pk, msg='无权限'):
        '''
        验证当前用户操作是否合理
        :param pk:
        :return:
        '''
        item = self.datamodel.get(pk, self._base_filters)
        if item.user.id != self.get_user_id():
            flash(str(msg), "danger")
            return True
