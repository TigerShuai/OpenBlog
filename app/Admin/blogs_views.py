#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   admin_views.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/26 下午5:58   wangshuai      1.0         None

'''
from flask_appbuilder import ModelView
from flask_appbuilder.models.mixins import AuditMixin
from flask_appbuilder.models.sqla.filters import FilterEqual, FilterNotEqual
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app.libs.blgosModelView import blogsModelView
from app.models.blogs import NotesType, Notes, notes_STATE


class NotesTypeView(AuditMixin, ModelView):
    datamodel = SQLAInterface(NotesType)
    label_columns = {
        'id': '类型ID',
        'test_id': '文章ID',
        'strtype': '类型名称',
        'notes_type_State': '状态',
        'user': '用户',
        'get_role': '用户权限',
    }
    list_title = '博客类型列表'
    class_permission_name = list_title
    edit_title = '编辑博客类型'
    show_title = '查看博客类型'
    add_title = '新增博客类型'

    add_columns = ('strtype',)
    list_columns = ('strtype', 'get_role', 'user')
    edit_columns = ('strtype',)
    show_columns = ('strtype',)
    base_filters = [['notes_type_State', FilterEqual, 0]]

    def pre_add(self, item):
        '''
        add添加之前调用，修改None默认id为当前用户id，做用户id和笔记类型id绑定
        :param item:
        :return:
        '''
        item.userId = self.get_user_id()


class NotesView(blogsModelView):
    datamodel = SQLAInterface(Notes)
    add_template = 'widgets/add_from.html'
    edit_template = 'widgets/edit_from.html'
    show_template = 'widgets/show_from.html'
    base_order = ('alter_time', 'desc')
    list_title = '博客列表'
    class_permission_name = list_title
    edit_title = '编辑博客'
    show_title = '查看博客'
    add_title = '新增博客'

    label_columns = {
        'id': '文章ID',
        'userId': '用户id',
        'notestype.strtype': '文章类型',
        'notestype': '文章类型',
        'title': '标题',
        'body_html': '内容',
        'create_time': '发布时间',
        'seo_link': '引用链接',
        'alter_time': '修改时间',
        'user.username': '用户',
        'notesState': '文章状态',
        # 'user.roles':'权限名',
        'get_role': '权限名',
    }
    base_filters = [['notesState', FilterNotEqual, 2]]
    search_columns = ('id', 'notestype', 'title', 'create_time', 'alter_time', 'user', 'notesState')
    list_columns = ('title', 'user.username', 'notestype.strtype', 'alter_time', 'get_role', 'notesState')
    edit_columns = ('id', 'notestype', 'title', 'body_html', 'create_time', 'notesState')
    show_columns = (
        'id', 'notestype', 'title', 'body_html', 'create_time', 'alter_time', 'userId', 'user', 'notesState')
    formatters_columns = {
        'user': lambda x: x.username,
        'notesState': lambda x: notes_STATE.get(x)
    }


class PublicNotesView(blogsModelView):
    datamodel = SQLAInterface(Notes)
    add_template = 'widgets/add_from.html'
    edit_template = 'widgets/edit_from.html'
    show_template = 'widgets/show_from.html'
    base_order = ('alter_time', 'desc')
    list_title = '公开博客'
    class_permission_name = list_title
    edit_title = '编辑博客'
    show_title = '查看博客'
    add_title = '新增博客'

    label_columns = {
        'id': '文章ID',
        'userId': '用户id',
        'notestype.strtype': '文章类型',
        'notestype': '文章类型',
        'title': '标题',
        'body_html': '内容',
        'create_time': '发布时间',
        'seo_link': '引用链接',
        'alter_time': '修改时间',
        'user.username': '用户',
        'notesState': '文章状态',
        # 'user.roles':'权限名',
        'get_role': '权限名',
        'notes_private': '博客权限',
    }
    base_filters = [['notesState', FilterNotEqual, 2], ['notes_private', FilterEqual, True]]
    search_columns = ('notestype', 'title')
    list_columns = ('title', 'notestype.strtype', 'alter_time', 'notesState')
    edit_columns = ('id', 'notestype', 'title', 'body_html', 'create_time', 'notesState')
    show_columns = (
        'id', 'notestype', 'title', 'body_html', 'create_time', 'alter_time', 'userId', 'user', 'notesState')
    formatters_columns = {
        'user': lambda x: x.username,
        'notesState': lambda x: notes_STATE.get(x)
    }
