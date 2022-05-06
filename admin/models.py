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


class ServiceShop(db.Model):
    __tablename__ = 'serviceshop'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    description_ru = db.Column(db.String(512))
    description_en = db.Column(db.String(512))
    contact = db.Column(db.BigInteger())
    photo = db.Column(db.String)
    products = db.relationship('Service', backref='shop', lazy=True, cascade='all,delete')
    orders = db.relationship('ServiceOrder', backref='shop', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('servicecategory.id'))

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    description_ru = db.Column(db.String(512))
    description_en = db.Column(db.String(512))
    photo = db.Column(db.String)
    price = db.Column(db.Integer())
    orders = db.relationship('ServiceOrder', backref='product', lazy=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('serviceshop.id'))


class MealCategory(db.Model):
    __tablename__ = 'mealcategory'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    restaurants = db.relationship('Restaurant', backref='category', lazy=True, cascade='all,delete')

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer(), primary_key=True)
    name_ = db.Column(db.String(64))
    description_ru = db.Column(db.String(512))
    description_en = db.Column(db.String(512))
    contact = db.Column(db.BigInteger())
    photo = db.Column(db.String(64))
    start_time = db.Column(db.Time(timezone=tz))
    end_time = db.Column(db.Time(timezone=tz))
    min_sum = db.Column(db.Integer())
    delivery_price = db.Column(db.Integer())
    categories = db.relationship('RestaurantCategory', backref='restaurant', lazy=True, cascade='all,delete')
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('mealcategory.id'))


    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_


class RestaurantCategory(db.Model):
    __tablename__ = 'restaurantcategory'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    products = db.relationship('Product', backref='category', lazy=True, cascade='all,delete')
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))


    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.Text())
    name = db.Column(db.String(128))
    communication = db.Column(db.String(32))
    delivery_time = db.Column(db.String(64))
    active = db.Column(db.Boolean())
    messages = db.relationship('Message', backref='order', lazy=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    def __chat__(self):
        messages_ = ''
        for mess in self.messages:
            messages_ += MESSAGE.format(
                time=str(mess.time)[:8],
                name=mess.name,
                text=mess.text
            )
        text = CHAT_MESSAGE.format(
            id_=self.id,
            messages=messages_
        )
        return text


class ServiceOrder(db.Model):
    __tablename__ = 'serviceorder'
    id = db.Column(db.Integer(), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    shop_id = db.Column(db.Integer, db.ForeignKey('serviceshop.id'))


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    text = db.Column(db.Text())
    time = db.Column(db.Time(timezone=tz))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    description_ru = db.Column(db.String(512))
    description_en = db.Column(db.String(512))
    price = db.Column(db.Integer())
    deals = db.Column(db.Integer(), default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('restaurantcategory.id'))


    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru

