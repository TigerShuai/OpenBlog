#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   security.py    
@Contact :   15617699933@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/7/28 上午11:41   wangshuai      1.0         None

flask_appbuilder  某些功能板块重写
'''
from datetime import datetime
from flask_appbuilder.security.views import UserDBModelView, AuthDBView, RegisterUserModelView
from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder.actions import action
from flask_babel import lazy_gettext
from flask_appbuilder.baseviews import expose
from flask_appbuilder.const import (
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
    AUTH_OID,
    AUTH_REMOTE_USER,
)
from sqlalchemy import and_
from flask_babel import lazy_gettext as _
import logging
from flask_appbuilder.security.forms import LoginForm_db
from flask import flash, g
from flask_login import login_user
log = logging.getLogger(__name__)
from flask import redirect, request
import requests
from sqlalchemy import (
    Column,
    String,
)
from flask_appbuilder.security.sqla.models import User
from app import db,app
from flask_appbuilder._compat import as_unicode


class MyUserDBView(UserDBModelView):

    '''
    测试功能
    '''

    @action("muldelete", "删除", "Delete all Really?", "fa-rocket", single=False)
    def muldelete(self, items):
        self.datamodel.delete_all(items)
        self.update_redirect()
        return redirect(self.get_redirect())


class Myauthdbview(AuthDBView):
    '''
    重写登录，改为钉钉登录模式
    '''
    login_template = "dingLogin.html"

    @expose("/login/", methods=["GET", "POST"])
    def login(self):

        if g.user is not None and g.user.is_authenticated:
            return redirect(self.appbuilder.get_url_for_index)
        form = LoginForm_db()
        if form.validate_on_submit():
            user = self.appbuilder.sm.auth_user_db(
                form.username.data, form.password.data
            )
            if not user:
                flash(as_unicode(self.invalid_login_message), "warning")
                return redirect(self.appbuilder.get_url_for_login)
            login_user(user, remember=False)
            return redirect(self.appbuilder.get_url_for_index)
        return self.render_template(
            self.login_template, title=self.title, form=form, appbuilder=self.appbuilder
        )

    @expose("ding")
    def ding(self):
        dingCode = request.args.get('code')
        try:
            appid = app.config['DING_APPId']
            appSecret = app.config['DING_APPSECRET']
            token = requests.get(f'https://oapi.dingtalk.com/sns/gettoken?appid={appid}&appsecret={appSecret}')
            access_token = token.json()["access_token"]
            tmp_auth_code = requests.post(
                f"https://oapi.dingtalk.com/sns/get_persistent_code?access_token={access_token}",
                json={
                    "tmp_auth_code": dingCode
                })
            tmp_code = tmp_auth_code.json()
            persistent_code = tmp_code['persistent_code']
            openid = tmp_code['openid']
            sns_token_request = requests.post(
                f"https://oapi.dingtalk.com/sns/get_sns_token?access_token={access_token}",
                json={
                    "openid": openid,
                    "persistent_code": persistent_code
                })
            sns_token = sns_token_request.json()['sns_token']
            user_info_request = requests.get(f'https://oapi.dingtalk.com/sns/getuserinfo?sns_token={sns_token}')
            user_info = user_info_request.json()['user_info']
            #   做钉钉openid校验数据库，存在进入，失败，弹出注册页面
            UserData = db.session.query(MyUserModel).outerjoin(MyUserModel.roles).filter(
                and_(MyUserModel.dingOpenID == user_info['openid'],
                     MyUserModel.active == True)).all()
            if UserData:
                login_user(UserData[0])
                return redirect(self.get_redirect())
            else:
                #  这里写注册逻辑
                self.addUser(user_info['nick'], user_info['openid'])
                return self.render_template('dingRegist.html')
        except BaseException as e:
            #  code用户手动刷新导致失效。检索session
            print('失败原因', e)
            self.login_template = 'dingRegist.html'
            return self.render_template(self.login_template)

    def addUser(self, username, dingOpenID, first_name='', last_name='', email='', password=""):
        user = MySecurityManager.user_model()
        user.username = username
        user.dingOpenID = dingOpenID
        user.email = email
        user.active = True
        # user.roles.append(role)
        user.first_name = first_name
        user.last_name = username
        user.password = password
        try:
            self.appbuilder.get_session.add(user)
            self.appbuilder.get_session.commit()
        except Exception as e:
            print(e)
            self.appbuilder.get_session.rollback()
        return user


class MyUserModel(User):
    __tablename__ = "ab_user"
    email = Column(String(64), unique=False, nullable=False)

    def get_full_name(self):
        return u"{1} {0}".format(self.first_name, self.last_name)

    def __repr__(self):
        return self.get_full_name()


class MyRegisterUserModelView(RegisterUserModelView):
    '''
    重写注册逻辑
    '''
    route_base = "/registeruser"
    base_permissions = ["can_list", "can_show", "can_delete", 'can_edit']
    list_title = lazy_gettext("List of Registration Requests")
    show_title = lazy_gettext("Show Registration")
    list_columns = ["username", "registration_date", "email"]
    show_exclude_columns = ["password"]
    search_exclude_columns = ["password"]


class MySecurityManager(SecurityManager):
    # user_model = MyUserModel  # 登录model添加openid
    userdbmodelview = MyUserDBView  # 用户权限视图展示页面
    # authdbview = Myauthdbview  # 钉钉登录模块
    # registerusermodelview = MyRegisterUserModelView  # 重写注册逻辑
    # permissionview_model = MyPermissionView

    def register_views(self):
        '''
        重写register_views  取消展示所有基本视图模板和视图view模板
        :return:
        '''
        # Security APIs
        self.appbuilder.add_api(self.security_api)

        if self.auth_user_registration:
            if self.auth_type == AUTH_DB:
                self.registeruser_view = self.registeruserdbview()
            elif self.auth_type == AUTH_OID:
                self.registeruser_view = self.registeruseroidview()
            elif self.auth_type == AUTH_OAUTH:
                self.registeruser_view = self.registeruseroauthview()
            if self.registeruser_view:
                self.appbuilder.add_view_no_menu(self.registeruser_view)

        self.appbuilder.add_view_no_menu(self.resetpasswordview())
        self.appbuilder.add_view_no_menu(self.resetmypasswordview())
        self.appbuilder.add_view_no_menu(self.userinfoeditview())

        if self.auth_type == AUTH_DB:
            self.user_view = self.userdbmodelview
            self.auth_view = self.authdbview()

        elif self.auth_type == AUTH_LDAP:
            self.user_view = self.userldapmodelview
            self.auth_view = self.authldapview()
        elif self.auth_type == AUTH_OAUTH:
            self.user_view = self.useroauthmodelview
            self.auth_view = self.authoauthview()
        elif self.auth_type == AUTH_REMOTE_USER:
            self.user_view = self.userremoteusermodelview
            self.auth_view = self.authremoteuserview()
        else:
            self.user_view = self.useroidmodelview
            self.auth_view = self.authoidview()
            if self.auth_user_registration:
                pass
                # self.registeruser_view = self.registeruseroidview()
                # self.appbuilder.add_view_no_menu(self.registeruser_view)

        self.appbuilder.add_view_no_menu(self.auth_view)

        self.user_view = self.appbuilder.add_view(
            self.user_view,
            "List Users",
            icon="fa-user",
            label=_("List Users"),
            category="Security",
            category_icon="fa-cogs",
            category_label=_("Security"),
        )

        role_view = self.appbuilder.add_view(
            self.rolemodelview,
            "List Roles",
            icon="fa-group",
            label=_("List Roles"),
            category="Security",
            category_icon="fa-cogs",
        )
        role_view.related_views = [self.user_view.__class__]
