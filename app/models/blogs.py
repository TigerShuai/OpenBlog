#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   testdb.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/26 下午6:00   wangshuai      1.0         None
'''

# import lib
from flask_appbuilder.security.sqla.models import User, Role
from app import db
from sqlalchemy import text

notes_STATE = {0: '新建', 1: '修改', 2: '屏蔽', 3: '草稿'}


class NotesType(db.Model):
    __tablename__ = 'notestype'
    '''
    文章类别
    '''
    id = db.Column(db.Integer, primary_key=True)
    strtype = db.Column(db.String(20), unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("ab_user.id"))
    user = db.relationship(User)
    notes_type_State = db.Column(db.Integer, nullable=False, default=0)  # 0:新建，1:修改，3:屏蔽

    def get_role(self):
        return self.user.roles

    def __repr__(self):
        return self.strtype


class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)  # 文章id
    notestype_id = db.Column(db.Integer, db.ForeignKey('notestype.id'))
    notestype = db.relationship(NotesType)
    roleId = db.Column(db.Integer, db.ForeignKey("ab_role.id"))
    role = db.relationship(Role)
    userId = db.Column(db.Integer, db.ForeignKey("ab_user.id"))
    user = db.relationship(User)
    title = db.Column(db.String(80), nullable=False)
    body_html = db.Column(db.Text)
    create_time = db.Column(db.DateTime, index=True)
    alter_time = db.Column(db.DateTime, index=True)  # 修改时间
    notesState = db.Column(db.Integer, nullable=False, default=0)  # 0:新建，1:修改，3:屏蔽
    seo_link = db.Column(db.String(256))
    notes_private = db.Column(db.Boolean, server_default=text('False'))  # 是否私有默认f  f:私有,T：开放

    def get_role(self):
        return self.user.roles
