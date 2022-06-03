import os

from flask import redirect, url_for, request
from flask_security import current_user

from flask_admin import BaseView, AdminIndexView, expose

from flask_admin.contrib.sqla import ModelView


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
    column_list = ('id', 'login', 'password', 'up_to_date', 'status', 'cities', 'proxy')
    form_columns = ('login', 'password', 'up_to_date', 'status', 'cities'. 'proxy')


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
