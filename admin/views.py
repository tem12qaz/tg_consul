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

from admin.flask_app_init import db

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
    column_list = (
    'id', 'telegram_id', 'username', 'max_field', 'active', 'ban', 'referral_url', 'wood_key', 'bronze_key',
    'silver_key', 'gold_key', 'platinum_key', 'legendary_key')
    form_columns = ('telegram_id', 'username', 'max_field', 'active', 'ban', 'referral_url', 'wood_key', 'bronze_key',
                    'silver_key', 'gold_key', 'platinum_key', 'legendary_key')

    def on_model_change(self, form, model, created):
        if model.ban:
            model.game_donor1 = []
            model.game_donor2 = []
            model.game_donor3 = []
            model.game_donor4 = []
            model.game_donor5 = []
            model.game_donor6 = []
            model.game_donor7 = []
            model.game_donor8 = []
            model.game_partner1 = []
            model.game_partner2 = []
            model.game_partner3 = []
            model.game_partner4 = []
            model.game_mentor1 = []
            model.game_mentor2 = []
            model.game_master = []

            db.session.commit()


class MessageView(AdminMixin, ModelView):
    column_list = ('id', 'name', 'text')
    form_columns = ('name', 'text')


class ButtonView(AdminMixin, ModelView):
    column_list = ('id', 'name', 'text')
    form_columns = ('name', 'text')


class TgAdminView(AdminMixin, ModelView):
    column_filters = ("user",)
    column_list = ('id', 'user')
    form_columns = ('user',)


class PriorityView(AdminMixin, ModelView):
    column_list = ('id', 'table')
    form_columns = ('table',)


class TablePriceView(AdminMixin, ModelView):
    column_list = ('id', 'start', 'start_mentor', 'wood', 'wood_mentor', 'bronze', 'bronze_mentor', 'silver',
                   'silver_mentor', 'gold', 'gold_mentor', 'platinum', 'platinum_mentor',
                   'legendary' 'legendary_mentor')
    form_columns = ('start', 'start_mentor', 'wood', 'wood_mentor', 'bronze', 'bronze_mentor', 'silver',
                    'silver_mentor', 'gold', 'gold_mentor', 'platinum', 'platinum_mentor',
                    'legendary' 'legendary_mentor')


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
                    'partner3', 'partner4', 'mentor1', 'mentor2', 'master',
                    'donor_1_mentor1', 'donor_1_mentor2', 'donor_1_master',
                    'donor_2_mentor1', 'donor_2_mentor2', 'donor_2_master',
                    'donor_3_mentor2', 'donor_3_mentor2', 'donor_3_master',
                    'donor_4_mentor1', 'donor_4_mentor2', 'donor_4_master',
                    'donor_5_mentor1', 'donor_5_mentor2', 'donor_5_master',
                    'donor_6_mentor1', 'donor_6_mentor2', 'donor_6_master',
                    'donor_7_mentor1', 'donor_7_mentor2', 'donor_7_master',
                    'donor_8_mentor1', 'donor_8_mentor2', 'donor_8_master')

    def donor_valid(view, context, model, name):
        if model.type == 'start':
            valid = getattr(model, name[:-1] + '_' + name[-1] + '_master')
        else:
            valid = getattr(model, name[:-1] + '_' + name[-1] + '_master') and \
                    getattr(model, name[:-1] + '_' + name[-1] + '_mentor1') and \
                    getattr(model, name[:-1] + '_' + name[-1] + '_mentor2')

        if valid:
            return str(getattr(model, name)) + '✅'

        else:
            return str(getattr(model, name)) + '❌'

    column_formatters = {
        'donor1': donor_valid,
        'donor2': donor_valid,
        'donor3': donor_valid,
        'donor4': donor_valid,
        'donor5': donor_valid,
        'donor6': donor_valid,
        'donor7': donor_valid,
        'donor8': donor_valid,
    }


class LogoutView(AdminMixin, BaseView):
    @expose('/')
    def logout_button(self):
        return redirect(url_for('security.logout', next='/admin'))
