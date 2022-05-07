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
    max_field = db.Column(db.String(32), default='start')


class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(32))

    donor1_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    donor2_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    donor3_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    donor4_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    donor5_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    donor6_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    donor7_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    donor8_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))

    partner1_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    partner2_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    partner3_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    partner4_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))

    mentor1_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    mentor2_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))

    master_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))

    donor1 = db.relationship("TelegramUser", uselist=False, backref="game_donor1", foreign_keys=[donor1_id])
    donor2 = db.relationship("TelegramUser", uselist=False, backref="game_donor2", foreign_keys=[donor2_id])
    donor3 = db.relationship("TelegramUser", uselist=False, backref="game_donor3", foreign_keys=[donor3_id])
    donor4 = db.relationship("TelegramUser", uselist=False, backref="game_donor4", foreign_keys=[donor4_id])
    donor5 = db.relationship("TelegramUser", uselist=False, backref="game_donor5", foreign_keys=[donor5_id])
    donor6 = db.relationship("TelegramUser", uselist=False, backref="game_donor6", foreign_keys=[donor6_id])
    donor7 = db.relationship("TelegramUser", uselist=False, backref="game_donor7", foreign_keys=[donor7_id])
    donor8 = db.relationship("TelegramUser", uselist=False, backref="game_donor8", foreign_keys=[donor8_id])

    partner1 = db.relationship("TelegramUser", uselist=False, backref="game_partner1", foreign_keys=[partner1_id])
    partner2 = db.relationship("TelegramUser", uselist=False, backref="game_partner2", foreign_keys=[partner2_id])
    partner3 = db.relationship("TelegramUser", uselist=False, backref="game_partner3", foreign_keys=[partner3_id])
    partner4 = db.relationship("TelegramUser", uselist=False, backref="game_partner4", foreign_keys=[partner4_id])

    mentor1 = db.relationship("TelegramUser", uselist=False, backref="game_mentor1", foreign_keys=[mentor1_id])
    mentor2 = db.relationship("TelegramUser", uselist=False, backref="game_mentor2", foreign_keys=[mentor2_id])

    master = db.relationship("TelegramUser", uselist=False, backref="game_master", foreign_keys=[master_id])

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Message(db.Model):
    __telegramusername__ = 'message'
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