from flask_security import UserMixin, RoleMixin

from flask_app_init import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
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

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_


class RestaurantCategory(db.Model):
    __tablename__ = 'restaurantcategory'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    products = db.relationship('Restaurant', backref='category', lazy=True)

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer(), primary_key=True)
    name_ru = db.Column(db.String(64))
    name_en = db.Column(db.String(64))
    description_ru = db.Column(db.String(512))
    description_en = db.Column(db.String(512))
    price = db.Column(db.Integer())
    deals = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return 'id' + str(self.id) + ' ' + self.name_ru

