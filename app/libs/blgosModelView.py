#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   blgosModelView.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/11/5 下午2:35   wangshuai      1.0         None
'''

# import lib
from flask import render_template, redirect, abort, flash
from app import db
from app.libs.baseModelView import MyModelView
from flask_appbuilder import has_access, expose

from app.models.blogs import NotesType


class blogsModelView(MyModelView):
    @expose("/show/<pk>", methods=["GET"])
    @has_access
    def show(self, pk):
        pk = self._deserialize_pk_if_composite(pk)
        item = self.datamodel.get(pk, self._base_filters)
        notesHtml = item.body_html
        notesTitle = item.title
        strtype = item.notestype.strtype
        widgets = self._show(pk)
        thePath = self.route_base + '/list'

        return render_template('widgets/show_from.html', urlPath=thePath, data=notesHtml, title=notesTitle,
                               type=strtype)

    @expose("/add", methods=["GET", "POST"])
    @has_access
    def add(self):
        widget = self._add()
        data = db.session.query(NotesType.id, NotesType.strtype).all()
        newdict = {}
        for i in data:
            newdict[i[0]] = i[1]
        widget['notes_type'] = newdict
        widget['user_id'] = self.get_user_id()
        if not widget:
            return self.post_add_redirect()
        else:
            return self.render_template(
                self.add_template, title=self.add_title, widgets=widget
            )

    @expose("/edit/<pk>", methods=["GET", "POST"])
    @has_access
    def edit(self, pk):
        if self.verify(pk, msg='❌🙅‍♂🙅‍♂不能修改ta人笔记'):
            return redirect(self.get_default_url())
        pk = self._deserialize_pk_if_composite(pk)
        item = self.datamodel.get(pk, self._base_filters)
        widgets = self._edit(pk)
        data = db.session.query(NotesType.id, NotesType.strtype).all()
        newdict = {}
        for i in data:
            newdict[i[0]] = i[1]
        widgets['notes_type'] = newdict
        widgets['user_id'] = self.get_user_id()
        widgets['notes_private'] = 'true' if item.notes_private else 'false'
        for i in self.edit_columns:
            if isinstance(getattr(item, i), db.Model):
                widgets[i] = getattr(item, i).strtype
            else:
                widgets[i] = getattr(item, i)
        if not widgets:
            return self.post_edit_redirect()
        else:
            return self.render_template(
                self.edit_template,
                title=self.edit_title,
                widgets=widgets,
                related_views=self._related_views,
                item=item,
            )

    def _delete(self, pk):
        """
            Delete function logic, override to implement different logic
            deletes the record with primary_key = pk

            :param pk:
                record primary key to delete
        """
        if self.verify(pk, msg='❌🙅‍♂🙅‍♂不能删除ta人笔记️‍'):
            return redirect(self.update_redirect())
        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)
        try:
            item.notesState = 2
        except Exception as e:
            flash(str(e), "danger")
        else:
            if self.datamodel.edit(item):
                self.post_update(item)
            flash(str('该数据已屏蔽'), "success")
            self.update_redirect()
