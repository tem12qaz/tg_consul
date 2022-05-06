import pytz
from flask_security import UserMixin, RoleMixin

from flask_app_init import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )

tz = pytz.timezone('Europe/Moscow')


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


class TelegramUser(db.Model):
    __tablename__ = 'telegramuser'
    id = db.Column(db.Integer(), primary_key=True)
    telegram_id = db.Column(db.BigInteger())
    username = db.Column(db.String(128))
    donor1_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    donor2_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    donor3_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    donor4_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    donor5_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    donor6_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    donor7_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    donor8_id = db.Column(db.Integer, db.ForeignKey('table.id'))

    partner1_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    partner2_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    partner3_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    partner4_id = db.Column(db.Integer, db.ForeignKey('table.id'))

    mentor1_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    mentor2_id = db.Column(db.Integer, db.ForeignKey('table.id'))

    mentor_id = db.Column(db.Integer, db.ForeignKey('table.id'))


class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(32))
    donor1 = db.relationship("TelegramUser", uselist=False, backref="game_donor1")
    donor2 = db.relationship("TelegramUser", uselist=False, backref="game_donor2")
    donor3 = db.relationship("TelegramUser", uselist=False, backref="game_donor3")
    donor4 = db.relationship("TelegramUser", uselist=False, backref="game_donor4")
    donor5 = db.relationship("TelegramUser", uselist=False, backref="game_donor5")
    donor6 = db.relationship("TelegramUser", uselist=False, backref="game_donor6")
    donor7 = db.relationship("TelegramUser", uselist=False, backref="game_donor7")
    donor8 = db.relationship("TelegramUser", uselist=False, backref="game_donor8")

    partner1 = db.relationship("TelegramUser", uselist=False, backref="game_partner1")
    partner2 = db.relationship("TelegramUser", uselist=False, backref="game_partner2")
    partner3 = db.relationship("TelegramUser", uselist=False, backref="game_partner3")
    partner4 = db.relationship("TelegramUser", uselist=False, backref="game_partner4")

    mentor1 = db.relationship("TelegramUser", uselist=False, backref="game_mentor1")
    mentor2 = db.relationship("TelegramUser", uselist=False, backref="game_mentor2")

    master = db.relationship("TelegramUser", uselist=False, backref="game_master")

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    text = db.Column(db.Text())

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name


class Button(db.Model):
    __tablename__ = 'button'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    text = db.Column(db.String(128))

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name


class TablePrice(db.Model):
    __tablename__ = 'tableprice'
    id = db.Column(db.Integer(), primary_key=True)
    start = db.Column(db.Integer())
    wood = db.Column(db.Integer())
    bronze = db.Column(db.Integer())
    silver = db.Column(db.Integer())
    gold = db.Column(db.Integer())
    platinum = db.Column(db.Integer())
    legendary = db.Column(db.Integer())


class Config(db.Model):
    __tablename__ = 'config'
    id = db.Column(db.Integer(), primary_key=True)
    support_url = db.Column(db.String(128))
    pdf = db.Column(db.String(128))
    about_photo = db.Column(db.String(128))
    channel = db.Column(db.String(128))
    chat = db.Column(db.String(128))
    keys_system = db.Column(db.String(128))
    delete_time = db.Column(db.Integer())
    block_time = db.Column(db.Integer())

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru