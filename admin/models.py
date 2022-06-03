import pytz
from flask_security import UserMixin, RoleMixin

from flask_app_init import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )


account_city = db.Table('account_city',
                       db.Column('city_id', db.Integer(), db.ForeignKey('city.id')),
                       db.Column('account_id', db.Integer(), db.ForeignKey('account.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


class Config(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sleep_min = db.Column(db.Integer())
    sleep_max = db.Column(db.Integer())


class Proxy(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.String(32))
    password = db.Column(db.String(32))
    ip = db.Column(db.String(32))
    port = db.Column(db.String(32))
    status = db.Column(db.String(16), default='OK')
    # accounts = db.relationship("Account", backref="proxy", lazy='dynamic')

    @property
    def http(self):
        return f'http://{self.user}:{self.password}@{self.ip}:{self.port}/'

    @property
    def https(self):
        return f'https://{self.user}:{self.password}@{self.ip}:{self.port}/'


class Account(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(32))
    password = db.Column(db.String(32))
    up_to_date = db.Column(db.Date())
    status = db.Column(db.String(16), default='SEARCH')
    cities = db.relationship("City", secondary="account_city")
    # proxy_id = db.Column(db.Integer, db.ForeignKey('proxy.id'))
    # proxy = db.relationship('Proxy')

    def __repr__(self):
        return self.login


class City(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32))
    site_id = db.Column(db.Integer())
    users = db.relationship("Account", secondary="account_city")

    def __repr__(self):
        return self.name

