from datetime import datetime

import pytz
from tortoise.models import Model
from tortoise import fields
from flask_security import UserMixin, RoleMixin

from data import buttons, messages
from data.messages import MESSAGE


class Cart:
    def __init__(self, user):
        self.user = user

    async def add(self, product):
        string = f';{product.id}='
        if string in self.user.cart_:
            count = int(self.user.cart_.split(string)[1].split(';')[0])
            self.user.cart_.replace(f'{string}{count}', f'{string}{count+1}')
        else:
            self.user.cart_ += f'{string}1;'

        await self.user.save

    async def remove(self, product):
        string = f';{product.id}='
        if string in self.user.cart_:
            count = int(self.user.cart_.split(string)[1].split(';')[0])
            if count > 1:
                self.user.cart_.replace(f'{string}{count}', f'{string}{count-1}')
            else:
                self.user.cart_.replace(f'{string}{count}', '')
        else:
            self.user.cart_ += f'{string}1;'

        await self.user.save

    async def clear(self):
        self.user.cart_ = ';'
        await self.user.save()

    async def all(self):
        prods = {}
        for prod in self.user.cart_.split(';'):
            if prod == '':
                continue
            prod_id, count = prod.split('=')
            product = await Product.get_or_none(id=int(prod_id))
            if not product:
                continue

            prods[product] = int(count)
        return prods

    async def first(self):
        try:
            prod_id, count = self.user.cart_.split(';')[1]
        except (IndexError, ValueError):
            return None
        else:
            return await Product.get_or_none(id=int(prod_id))


class TelegramUser(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True, index=True)
    username = fields.CharField(128, unique=True, null=True)
    state = fields.CharField(64, default='')
    lang = fields.CharField(4, default='ru')
    cart_ = fields.TextField(default=';')
    address = fields.TextField(null=True)
    name = fields.CharField(128, null=True)

    @property
    def cart(self):
        return Cart(self)

    async def prod_count(self, product):
        count = 0
        for prod in self.cart:
            if prod == product:
                count += 1

        return count

    @property
    def button(self):
        if self.lang == 'ru':
            return buttons.Ru
        elif self.lang == 'en':
            return buttons.En

    @property
    def message(self):
        if self.lang == 'ru':
            return messages.Ru
        elif self.lang == 'en':
            return messages.En

    def __str__(self):
        return str(self.telegram_id)


class ServiceCategory(Model):
    button_type = 'servicecat'
    back_to = 'main'

    id = fields.IntField(pk=True)
    name_ru = fields.CharField(64)
    name_en = fields.CharField(64)

    def name(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.name_ru
        elif user.lang == 'en':
            return self.name_en


class ServiceShop(Model):
    button_type = 'shop'
    back_to = 'service'

    id = fields.IntField(pk=True)
    name_ru = fields.CharField(64)
    name_en = fields.CharField(64)
    contact = fields.BigIntField()
    description_ru = fields.CharField(512)
    description_en = fields.CharField(512)
    photo = fields.TextField()
    category = fields.ForeignKeyField('models.ServiceCategory', related_name='shops', index=True)

    def name(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.name_ru
        elif user.lang == 'en':
            return self.name_en

    def description(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.description_ru
        elif user.lang == 'en':
            return self.description_en


class Service(Model):
    button_type = 'service_prod'
    back_to = 'servicecat'

    id = fields.IntField(pk=True)
    name_ru = fields.CharField(64)
    name_en = fields.CharField(64)
    description_ru = fields.CharField(512)
    description_en = fields.CharField(512)
    price = fields.IntField()
    shop = fields.ForeignKeyField('models.ServiceShop', related_name='products', index=True)

    def name(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.name_ru
        elif user.lang == 'en':
            return self.name_en

    def description(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.description_ru
        elif user.lang == 'en':
            return self.description_en


class MealCategory(Model):
    button_type = 'mealcat'
    back_to = 'main'

    id = fields.IntField(pk=True)
    name_ru = fields.CharField(64)
    name_en = fields.CharField(64)

    def name(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.name_ru
        elif user.lang == 'en':
            return self.name_en


class Restaurant(Model):
    button_type = 'rest'
    back_to = 'meal'

    id = fields.IntField(pk=True)
    name_ = fields.CharField(64)
    contact = fields.BigIntField(index=True)
    description_ru = fields.CharField(512)
    description_en = fields.CharField(512)
    photo = fields.TextField()
    start_time = fields.TimeField()
    end_time = fields.TimeField()
    min_sum = fields.IntField(default=0)
    delivery_price = fields.IntField(default=0)
    category = fields.ForeignKeyField('models.MealCategory', related_name='restaurants', index=True)

    def name(self, _):
        if self.is_work():
            prefix = '✅'
        else:
            prefix = '🕐'
        return prefix + self.name_

    def description(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.description_ru
        elif user.lang == 'en':
            return self.description_en

    def is_work(self):
        tz = pytz.timezone('Europe/Moscow')
        now = datetime.now(tz).time()
        if self.start_time.replace(tzinfo=tz) <= now.replace(tzinfo=tz) <= self.end_time.replace(tzinfo=tz):
            return True
        else:
            return False


class RestaurantCategory(Model):
    button_type = 'restcat'
    back_to = 'mealcat'

    id = fields.IntField(pk=True)
    restaurant = fields.ForeignKeyField('models.Restaurant', related_name='categories', index=True)
    name_ru = fields.CharField(64)
    name_en = fields.CharField(64)

    def name(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.name_ru
        elif user.lang == 'en':
            return self.name_en


class Product(Model):
    button_type = 'restprod'
    back_to = 'rest'

    id = fields.IntField(pk=True)
    name_ru = fields.CharField(64)
    name_en = fields.CharField(64)
    description_ru = fields.CharField(512)
    description_en = fields.CharField(512)
    price = fields.IntField()
    category = fields.ForeignKeyField('models.RestaurantCategory', related_name='products', index=True)
    deals = fields.IntField(default=0)

    def description(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.description_ru
        elif user.lang == 'en':
            return self.description_en

    def name(self, user: TelegramUser):
        if user.lang == 'ru':
            return self.name_ru
        elif user.lang == 'en':
            return self.name_en


class Order(Model):
    id = fields.IntField(pk=True)
    shop = fields.ForeignKeyField('models.Restaurant', related_name='orders', index=True, on_delete='SET NULL', null=True)
    customer = fields.ForeignKeyField('models.TelegramUser', related_name='orders', index=True, on_delete='SET NULL', null=True)
    address = fields.TextField(default='')
    name = fields.CharField(128)
    communication = fields.CharField(32, default='Telegram')
    delivery_time = fields.CharField(64, default='')
    cart_ = fields.TextField(default=';')
    active = fields.BooleanField(default=False)

    @property
    def cart(self):
        return Cart(self)

    async def message(self, rows, order_sum):
        text = messages.Ru.REST_ORDER_MESSAGE.format(
            id_=self.id,
            lang=(await self.customer).lang,
            name=self.name,
            communication=self.communication,
            time=self.delivery_time,
            address=self.address,
            rows=rows,
            delivery=(await self.shop).delivery_price,
            sum=order_sum
        )
        return text

    async def chat(self, user: TelegramUser):
        messages_ = ''
        for mess in await self.messages:
            messages_ += MESSAGE.format(
                time=mess.time,
                name=mess.name,
                text=mess.text
            )
        text = user.message.CHAT_MESSAGE.format(
            id_=self.id,
            messages=messages_
        )
        return text


class ServiceOrder(Model):
    id = fields.IntField(pk=True)
    shop = fields.ForeignKeyField('models.ServiceShop', related_name='orders', index=True, on_delete='SET NULL', null=True)
    product = fields.ForeignKeyField('models.Service', related_name='orders', index=True, on_delete='SET NULL', null=True)
    customer = fields.ForeignKeyField('models.TelegramUser', related_name='service_orders', index=True, on_delete='SET NULL', null=True)


class Message(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField('models.Order', related_name='messages', index=True)
    name = fields.CharField(128)
    text = fields.TextField()
    time = fields.TimeField()


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
