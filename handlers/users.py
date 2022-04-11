import io

import button as button
from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InputMedia

from data.config import FLOOD_RATE
from data.messages import SELECT_LANG_MESSAGE, CART_ROW
from db.models import TelegramUser
from keyboards.keyboards import *
from loader import dp, bot


@dp.message_handler(CommandStart())
@dp.throttled(rate=FLOOD_RATE)
async def bot_start(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)

    if user is None:
        await message.answer(
            SELECT_LANG_MESSAGE,
            reply_markup=lang_keyboard
        )
    else:
        await bot.send_photo(
            message.from_user.id,
            photo=open('logo.jpg', 'rb'),
            reply_markup=get_main_keyboard(user)
        )
        await message.answer(
            user.message.START_MESSAGE,
            reply_markup=get_meal_or_service_keyboard(user)
        )


@dp.callback_query_handler(lang_callback.filter())
@dp.throttled(rate=FLOOD_RATE)
async def lang_handler(callback: types.CallbackQuery, callback_data):
    await callback.answer()
    user = await TelegramUser.get_or_none(telegram_id=callback.from_user.id)
    if user is None:
        user = await TelegramUser.create(
            telegram_id=callback.from_user.id,
            username=callback.from_user.username,
            lang=callback_data['lang']
        )
    else:
        user.lang = callback_data['lang']
        await user.save()

    message = await bot.send_message(
        callback.from_user.id,
        user.message.START_MESSAGE,
        reply_markup=get_main_keyboard(user)
    )

    await message.delete()

    await bot.send_photo(
        callback.from_user.id,
        photo=open('logo.jpg', 'rb'),
        caption=user.message.START_MESSAGE,
        reply_markup=get_meal_or_service_keyboard(user)
    )


def compare_restaurants(user, rest, callback):
    prod_from_cart = await user.cart.limit(1)
    if prod_from_cart:
        rest2 = await (await prod_from_cart.category).restaurant
        if rest2 != rest:
            await callback.message.edit_caption(
                caption=user.message.ORDER_EXISTING_MESSAGE,
                reply_markup=get_order_keyboard(rest2, user)
            )
            return False
        else:
            return True


async def format_cart_message(user: TelegramUser):
    cart = await user.cart.all()
    if cart:
        rest = await (await (await user.cart.first()).category).restaurant
    else:
        return False, False

    prods_text = ''
    buttons = []
    i = 1
    order_sum = 0
    for prod, count in cart.items():
        sum_ = count * prod.price
        prods_text += CART_ROW.format(
            num=i, name=prod.name, category=await prod.category,
            price=prod.price, count=count, sum=sum_
        )
        buttons.append((CART_BUTTON_ROW.format(name=prod.name(user), count=count), prod.id))
        i += 1
        order_sum += sum_

    text = user.message.CART_MESSAGE.format(
        rest=rest.name(user),
        rows=prods_text,
        sum=order_sum,
        delivery=rest.delivery_price
    )
    keyboard = get_cart_keyboard(rest, order_sum, buttons, user)
    return text, keyboard


@dp.callback_query_handler(select_callback.filter())
@dp.throttled(rate=FLOOD_RATE)
async def main_menu(callback: types.CallbackQuery, callback_data):
    await callback.answer()
    user = await TelegramUser.get_or_none(telegram_id=callback.from_user.id)
    if user is None:
        return

    select = callback_data.get('select')

    if user.state != '':
        return

    if select == 'meal' or select == 'clear_cart':
        if select == 'clear_cart':
            await user.cart.clear()

        await bot.edit_message_caption(
            user.telegram_id,
            callback.message.message_id,
            caption=user.message.SELECT_CATEGORY,
            reply_markup=await get_meal_cat_keyboard(user)
        )

    elif select == 'main':
        message = await bot.send_message(
            callback.from_user.id,
            user.message.START_MESSAGE,
            reply_markup=get_main_keyboard(user)
        )

        await message.delete()

        await bot.send_photo(
            callback.from_user.id,
            photo=open('logo.jpg', 'rb'),
            caption=user.message.START_MESSAGE,
            reply_markup=get_meal_or_service_keyboard(user)
        )

    elif select == 'service':
        await callback.message.edit_caption(
            caption=user.message.SELECT_CATEGORY,
            reply_markup=await get_service_cat_keyboard(user)
        )

    elif select == 'top10':
        await callback.message.edit_caption(
            caption=user.message.SELECT_DISH_MESSAGE,
            reply_markup=await get_top_products(user)
        )

    elif '=' in select:
        id_ = int(select.split('=')[1])

        if 'mealcat' in select:
            try:
                await callback.message.edit_media(
                    InputMedia(open('logo.jpg',  'rb')),
                )
            except:
                pass

            prod_from_cart = await user.cart.limit(1)
            if prod_from_cart:
                rest = await (await prod_from_cart.category).restaurant
                await callback.message.edit_caption(
                    caption=user.message.ORDER_EXISTING_MESSAGE,
                    reply_markup=get_order_keyboard(rest, user)
                )

            category = await MealCategory.get_or_none(id=id_)
            if category is None:
                return
            message = user.message.SELECTED_KITCHEN_MESSAGE.format(name=category.name(user))
            keyboard = await get_rest_keyboard(category, user)

        elif 'rest' in select:
            rest = await Restaurant.get_or_none(id=id_)
            if rest is None:
                return

            if not compare_restaurants(user, rest, callback):
                return

            message = user.message.REST_MESSAGE.format(
                name=rest.name(user),
                description=rest.description(user),
                min_price=rest.min_sum,
                delivery=rest.delivery_price,
                time=f'{rest.start_time}-{rest.end_time}'
            )
            keyboard = await get_rest_cat_keyboard(rest, user)

            await callback.message.edit_media(
                InputMedia(open(rest.photo, 'rb')),
                reply_markup=keyboard
            )

        elif 'restcat' in select:
            category = await RestaurantCategory.get_or_none(id=id_)
            if category is None:
                return
            rest = await category.restaurant
            if rest is None:
                return

            if not compare_restaurants(user, rest, callback):
                return

            message = user.message.REST_MESSAGE.format(
                name=rest.name(user),
                description=rest.description(user),
                min_price=rest.min_sum,
                delivery=rest.delivery_price,
                time=f'{rest.start_time}-{rest.end_time}'
            )

            keyboard = await get_products_keyboard(category, user)

        elif 'prod=' or 'add' in select:
            product = await Product.get_or_none(id=id_)
            if product is None:
                return

            if not compare_restaurants(user, await (await product.category).restaurant, callback):
                return

            if 'add' in select:
                await user.cart.add(product)

            rest = await (await product.category).restaurant
            message = user.message.PRODUCT_MESSAGE.format(
                rest=rest.name(user),
                name=product.name(user),
                description=product.description(user),
                price=product.price
            )
            keyboard = await get_product_keyboard(product, user)

        elif 'remove' in select:
            product = await Product.get_or_none(id=id_)
            if product is None:
                return
            await user.cart.remove(product)

            message, keyboard = await format_cart_message(user)
            if not message:
                await callback.message.edit_caption(
                    caption=user.message.CART_EMPTY_MESSAGE
                )
                return

        elif 'servicecat' in select:
            category = await ServiceCategory.get_or_none(id=id_)
            if category is None:
                return
            message = user.message.SERVICE_TYPE_MESSAGE.format(name=category.name(user))
            keyboard = await get_shops_keyboard(category, user)

        elif 'shop' in select:
            shop = await ServiceShop.get_or_none(id=id_)
            if shop is None:
                return
            message = user.message.SERVICE_SHOP_MESSAGE.format(
                name=shop.name(user),
                description=shop.description(user)
            )
            keyboard = await get_services_keyboard(shop, user)

            await callback.message.edit_media(
                InputMedia(open(shop.photo, 'rb')),
                reply_markup=keyboard
            )

        elif 'shop_prod' in select:
            service = await Service.get_or_none(id=id_)
            if service is None:
                return
            message = user.message.SERVICE_SHOP_MESSAGE.format(
                name=service.name(user),
                description=service.description(user)
            )
            keyboard = await get_service_keyboard(service, user)

        elif 'service_order' in select:
            pass

        elif 'order' in select:
            pass

        else:
            return

        await callback.message.edit_caption(
            message,
            reply_markup=keyboard
        )
    else:
        return


@dp.message_handler()
@dp.throttled(rate=FLOOD_RATE)
async def listen_handler(message: types.Message):
    message_ = message
    print(message_)
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        return

    if message.text == user.button.MAIN_MENU_BUTTON and user.state == '':
        message = await bot.send_message(
            message.from_user.id,
            user.message.START_MESSAGE,
            reply_markup=get_main_keyboard(user)
        )

        await message.delete()

        await bot.send_photo(
            message.from_user.id,
            photo=open('logo.jpg', 'rb'),
            caption=user.message.START_MESSAGE,
            reply_markup=get_meal_or_service_keyboard(user)
        )

    elif message.text == user.button.CART_BUTTON and user.state == '':
        text, keyboard = await format_cart_message(user)
        if not text:
            await message.answer_photo(
                photo=open('logo.jpg', 'rb'),
                caption=user.message.CART_EMPTY_MESSAGE
            )
            return

        await message.answer_photo(
            photo=open('logo.jpg', 'rb'),
            caption=text,
            reply_markup=keyboard
        )

    elif message.text == user.button.SETTINGS_BUTTON and user.state == '':
        await message.answer(
            SELECT_LANG_MESSAGE,
            reply_markup=lang_keyboard
        )

    else:
        await message_.delete()

