from tortoise.models import Model
from tortoise import fields
from flask_security import UserMixin, RoleMixin


class Proxy(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('models.TelegramUser', related_name='admin', null=True, on_delete="SET NULL")
    state = fields.CharField(8, default='')
    photo = fields.BinaryField(null=True)
    video = fields.BinaryField(null=True)
    document = fields.BinaryField(null=True)


class Account(Model):
    id = fields.IntField(pk=True)
    table = fields.OneToOneField('models.Table', related_name='priority', null=True, on_delete="SET NULL")


class User(Model, UserMixin):
    id = fields.IntField(pk=True)
    email = fields.CharField(254, unique=True)
    password = fields.CharField(255)
    active = fields.BooleanField()
    roles = fields.ManyToManyField(
        'models.Role', related_name='users', through='roles_users'
    )


class Role(Model, RoleMixin):
    id = fields.IntField(pk=True)
    name = fields.CharField(100, unique=True)
    description = fields.CharField(255)

