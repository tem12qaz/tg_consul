from flask_security import UserMixin, RoleMixin

from flask_app_init import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )

MESSAGE = '''<code>{time}</code> <b>{name}</b>
{text}

'''
CHAT_MESSAGE = '''Chat  Order #{id_}

{messages}

Send /exit to leave the chat
'''


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
    orders = db.relationship('Order', backref='customer', lazy=True)
    service_orders = db.relationship('ServiceOrder', backref='customer', lazy=True)


class ServiceCategory(db.Model):
    __tablename__ = 'servicecategory'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    shops = db.relationship('ServiceShop', backref='category', lazy=True)

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
    products = db.relationship('Service', backref='shop', lazy=True)
    orders = db.relationship('ServiceOrder', backref='shop', lazy=True)
    servicecategory_id = db.Column(db.Integer, db.ForeignKey('servicecategory.id'))

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    description_ru = db.Column(db.String(512))
    description_en = db.Column(db.String(512))
    price = db.Column(db.Integer())
    orders = db.relationship('ServiceOrder', backref='product', lazy=True)
    serviceshop_id = db.Column(db.Integer, db.ForeignKey('serviceshop.id'))


class MealCategory(db.Model):
    __tablename__ = 'mealcategory'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    restaurants = db.relationship('Restaurant', backref='category', lazy=True)

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer(), primary_key=True)
    name_ = db.Column(db.String(64))
    description_ru = db.Column(db.String(512))
    description_en = db.Column(db.String(512))
    contact = db.Column(db.BigInteger())
    photo = db.Column(db.String)
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    min_sum = db.Column(db.Integer())
    delivery_price = db.Column(db.Integer())
    categories = db.relationship('RestaurantCategory', backref='restaurant', lazy=True)
    orders = db.relationship('Order', backref='restaurant', lazy=True)
    mealcategory_id = db.Column(db.Integer, db.ForeignKey('mealcategory.id'))


    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_


class RestaurantCategory(db.Model):
    __tablename__ = 'restaurantcategory'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    products = db.relationship('Product', backref='category', lazy=True)
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
    telegramuser_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))


    def chat(self):
        messages_ = ''
        for mess in self.messages:
            messages_ += MESSAGE.format(
                time=mess.time,
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
    telegramuser_id = db.Column(db.Integer, db.ForeignKey('telegramuser.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    serviceshop_id = db.Column(db.Integer, db.ForeignKey('serviceshop.id'))


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    text = db.Column(db.Text())
    time = db.Column(db.Time())
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
    restaurantcategory_id = db.Column(db.Integer, db.ForeignKey('restaurantcategory.id'))


    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru

