import os
import os.path as op
import time

from flask import redirect, url_for, request
from flask_admin.form import FileUploadField, ImageUploadField
from flask_security import current_user

from flask_admin import BaseView, AdminIndexView, expose, form

from flask_admin.contrib.sqla import ModelView
from jinja2 import Markup
from werkzeug.utils import secure_filename
from wtforms import ValidationError

from flask_app_init import db

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(basedir, 'files')


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin_home.html')


class ProxyView(AdminMixin, ModelView):
    column_list = ('id', 'user', 'password', 'ip', 'port', 'status')
    form_columns = ('user', 'password', 'ip', 'port', 'status')


class AccountView(AdminMixin, ModelView):
    column_list = ('id', 'login', 'password', 'month', 'status', 'cities')
    form_columns = ('login', 'password', 'month', 'status', 'cities')


class CityView(AdminMixin, ModelView):
    column_list = ('id', 'name', 'site_id')
    form_columns = ('name', 'site_id')


class ConfigView(AdminMixin, ModelView):
    column_list = ('id', 'sleep_min', 'sleep_max')
    form_columns = ('sleep_min', 'sleep_max')


class LogoutView(AdminMixin, BaseView):
    @expose('/')
    def logout_button(self):
        return redirect(url_for('security.logout', next='/admin'))
