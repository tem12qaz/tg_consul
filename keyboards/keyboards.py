from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from tortoise import Model

from data.buttons import *
from db.models import TelegramUser, MealCategory, Restaurant, RestaurantCategory, Product, ServiceCategory, ServiceShop, \
    Service

select_callback = CallbackData("main", 'select')
lang_callback = CallbackData("language", 'lang')


def get_main_keyboard(user: TelegramUser):
    main_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton(user.button.CART_BUTTON)],
            [KeyboardButton(user.button.MAIN_MENU_BUTTON), KeyboardButton(user.button.SETTINGS_BUTTON)]
        ],
        resize_keyboard=True
    )
    return main_keyboard


def get_meal_or_service_keyboard(user: TelegramUser):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=user.button.MEAL_BUTTON, callback_data=select_callback.new(select='meal')),
                InlineKeyboardButton(text=user.button.SERVICE_BUTTON, callback_data=select_callback.new(select='service')),
            ]
        ]
    )
    return keyboard


def get_table_buttons(objects, user: TelegramUser):
    inline_keyboard = []
    for i in range(0, len(objects), 2):
        if i != len(objects) - 1:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=objects[i].name(user.lang), callback_data=select_callback.new(
                            select=objects[i].button_type + '=' + str(objects[i].id)
                        )
                    ),
                    InlineKeyboardButton(
                        text=objects[i+1].name(user.lang), callback_data=select_callback.new(
                            select=objects[i+1].button_type + '=' + str(objects[i+1].id)
                        )
                    ),
                ]
            )
        else:
            inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=objects[i].name(user.lang), callback_data=select_callback.new(
                            select=objects[i].button_type + '=' + str(objects[i].id)
                        )
                    )
                ]
            )
    return inline_keyboard


async def get_top_products(user: TelegramUser):
    prods = await Product.all().order_by('deals').limit(10)
    inline_keyboard = get_table_buttons(prods, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select='meal'
            )
        )]
    )


async def get_meal_cat_keyboard(user: TelegramUser):
    cats = await MealCategory.all()
    inline_keyboard = get_table_buttons(cats, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.TOP_BUTTON, callback_data=select_callback.new(
                select='top10'
            )
        )]
    )
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.OPEN_NOW_BUTTON, callback_data=select_callback.new(
                select='open_now'
            )
        )]
    )
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select=MealCategory.back_to
            )
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_rest_keyboard(category: MealCategory, user: TelegramUser):
    rests = await category.restaurants.all()
    inline_keyboard = get_table_buttons(rests, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select=Restaurant.back_to
            )
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_rest_cat_keyboard(rest: Restaurant, user: TelegramUser):
    cats = await rest.categories.all()
    meal_cat = await Restaurant.category
    inline_keyboard = get_table_buttons(cats, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select=RestaurantCategory.back_to + '=' + str(meal_cat.id)
            )
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_products_keyboard(category: RestaurantCategory, user: TelegramUser):
    prods = await category.products.all()
    rest = await category.restaurant
    inline_keyboard = get_table_buttons(prods, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select=Product.back_to + '=' + str(rest.id)
            )
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_product_keyboard(product: Product, user: TelegramUser):
    rest_cat = await product.category

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=user.button.ADD_BUTTON.format(count=await user.prod_count(product)),
                callback_data=select_callback.new(
                    select='add=' + str(product.id)
                )
            )],
            [InlineKeyboardButton(
                text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                    select='restcat=' + str(rest_cat.id)
                )
            )]
        ]
    )
    return keyboard


def get_order_keyboard(rest: Restaurant, user: TelegramUser):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=user.button.CONTINUE_ORDER_BUTTON,
                callback_data=select_callback.new(
                    select='rest=' + str(rest.id)
                )
            )],
            [InlineKeyboardButton(
                text=user.button.CLEAR_CART_BUTTON, callback_data=select_callback.new(
                    select='clear_cart'
                )
            )]
        ]
    )
    return keyboard


def get_cart_keyboard(rest: Restaurant, sum_,  buttons, user: TelegramUser):
    inline_keyboard = []
    for button in buttons:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text=button[0], callback_data=select_callback.new(
                    select=f'remove_{button[1]}')
            )]
        )
    if sum_ < rest.min_sum:
        text = user.button.MIN_SUM_BUTTON
        select = 'nothing'
    elif not rest.is_work():
        text = user.button.REST_CLOSED_BUTTON
        select = 'nothing'
    else:
        text = user.button.CONFIRM_ORDER_BUTTON
        select = 'order'
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=text, callback_data=select_callback.new(select=select)
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_service_cat_keyboard(user: TelegramUser):
    cats = await ServiceCategory.all()
    inline_keyboard = get_table_buttons(cats, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select=ServiceCategory.back_to
            )
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_shops_keyboard(category: ServiceCategory, user: TelegramUser):
    shops = await category.shops.all()
    inline_keyboard = get_table_buttons(shops, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select=ServiceShop.back_to
            )
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_services_keyboard(shop: ServiceShop, user: TelegramUser):
    shops = await shop.products.all()
    inline_keyboard = get_table_buttons(shops, user)
    inline_keyboard.append(
        [InlineKeyboardButton(
            text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                select=Service.back_to
            )
        )]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_service_keyboard(service: Service, user: TelegramUser):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=user.button.CONFIRM_ORDER_BUTTON,
                callback_data=select_callback.new(
                    select='service_order=' + str(service.id)
                )
            )],
            [InlineKeyboardButton(
                text=user.button.BACK_BUTTON, callback_data=select_callback.new(
                    select='shop=' + str(await service.shop.id)
                )
            )]
        ]
    )
    return keyboard


lang_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=RU_BUTTON, callback_data=lang_callback.new(lang='ru')),
        ],
        [
            InlineKeyboardButton(text=EN_BUTTON, callback_data=lang_callback.new(lang='en'))
        ]
    ]
)

