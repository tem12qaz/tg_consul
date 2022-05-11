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


class TelegramUserView(AdminMixin, ModelView):
    column_filters = ("telegram_id", "id", "username")
    column_list = ('id', 'telegram_id', 'username', 'max_field', 'referral_url', 'wood_key', 'bronze_key',
                   'silver_key', 'gold_key', 'platinum_key', 'legendary_key')
    form_columns = ('telegram_id', 'username', 'max_field', 'referral_url', 'wood_key', 'bronze_key',
                    'silver_key', 'gold_key', 'platinum_key', 'legendary_key')


class MessageView(AdminMixin, ModelView):
    column_list = ('id', 'name', 'text')
    form_columns = ('name', 'text')


class ButtonView(AdminMixin, ModelView):
    column_list = ('id', 'name', 'text')
    form_columns = ('name', 'text')


class AdminView(AdminMixin, ModelView):
    name='TgAdmin'
    column_filters = ("user",)
    column_list = ('id', 'user')
    form_columns = ('user',)


class PriorityView(AdminMixin, ModelView):
    column_list = ('id', 'table')
    form_columns = ('table',)


class TablePriceView(AdminMixin, ModelView):
    column_list = ('id', 'start', 'wood', 'bronze', 'silver', 'gold', 'platinum', 'legendary')
    form_columns = ('start', 'wood', 'bronze', 'silver', 'gold', 'platinum', 'legendary')


class ConfigView(AdminMixin, ModelView):
    column_list = ('id', 'support_url', 'pdf', 'about_photo', 'channel',
                   'chat', 'keys_system', 'delete_time', 'block_time')
    form_columns = ('support_url', 'pdf', 'about_photo', 'channel',
                    'chat', 'keys_system', 'delete_time', 'block_time')

    def name_gen(obj, file_data):
        parts = op.splitext(file_data.filename)
        return secure_filename(f'file-{time.time()}%s%s' % parts)

    def picture_validation(form, field):
        if field.data:
            filename = field.data.filename
            if filename[-4:] != '.jpg' and filename[-4:] != '.png':
                raise ValidationError('file must be .jpg or .png')
        data = field.data.stream.read()
        field.data = data
        return True

    # @staticmethod
    def picture_formatter(view, context, model, name):
        return '' if not getattr(model, name) else 'a picture'

    # column_formatters = dict(photo=picture_formatter)
    # form_overrides = dict(photo=FileUploadField)
    # form_args = dict(photo=dict(validators=[picture_validation]))

    def _list_thumbnail(view, context, model, name):
        if not model.about_photo:
            return ''

        return Markup(
            '<img src="%s">' %
            url_for('static',
                    filename=form.thumbgen_filename(model.about_photo))
        )

    column_formatters = {
        'about_photo': _list_thumbnail
    }

    form_extra_fields = {
        'about_photo': ImageUploadField(
            'about_photo', base_path=file_path, thumbnail_size=(100, 100, True), namegen=name_gen)
    }


class TableView(AdminMixin, ModelView):
    column_filters = ("id", "master", 'mentor1', 'mentor2')
    column_list = ('id', 'type', 'donor1', 'donor2', 'donor3', 'donor4', 'donor5',
                   'donor6', 'donor7', 'donor8', 'partner1', 'partner2',
                   'partner3', 'partner4', 'mentor1', 'mentor2', 'master')
    form_columns = ('type', 'donor1', 'donor2', 'donor3', 'donor4', 'donor5',
                    'donor6', 'donor7', 'donor8', 'partner1', 'partner2',
                    'partner3', 'partner4', 'mentor1', 'mentor2', 'master')


class LogoutView(AdminMixin, BaseView):
    @expose('/')
    def logout_button(self):
        return redirect(url_for('security.logout', next='/admin'))
