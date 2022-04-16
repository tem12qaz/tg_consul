import traceback
from datetime import datetime

import pytz
from aiogram.dispatcher.filters import CommandStart, RegexpCommandsFilter
from aiogram.types import InputMedia

from data.config import FLOOD_RATE
from data.messages import SELECT_LANG_MESSAGE, CART_ROW, ORDER_SHOP_MESSAGE
from db.models import TelegramUser, ServiceOrder, Order, Message
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
        if user.state != '':
            await message.delete()
            return

        await message.answer(
            user.message.BOT_MESSAGE,
            reply_markup=get_main_keyboard(user)
        )

        await bot.send_photo(
            message.from_user.id,
            photo=open('logo.jpg', 'rb'),
            caption=user.message.START_MESSAGE,
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
        if user.state != '':
            await callback.message.delete()
            return

        user.lang = callback_data['lang']
        await user.save()

    await bot.send_message(
        callback.from_user.id,
        user.message.BOT_MESSAGE,
        reply_markup=get_main_keyboard(user)
    )

    await bot.send_photo(
        callback.from_user.id,
        photo=open('logo.jpg', 'rb'),
        caption=user.message.START_MESSAGE,
        reply_markup=get_meal_or_service_keyboard(user)
    )


async def compare_restaurants(user, rest, callback):
    prod_from_cart = await user.cart.first()
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
    else:
        return True


async def format_cart_rows(cart, user, buttons_=False, deal=False):
    buttons = []
    prods_text = ''
    order_sum = 0
    i = 1

    for prod, count in cart.items():
        if deal:
            prod.deals += 1
            await prod.save()
        sum_ = count * prod.price
        prods_text += CART_ROW.format(
            num=i, name=prod.name(user), category=(await prod.category).name(user),
            price=prod.price, count=count, sum=sum_
        )
        if buttons_:
            buttons.append((CART_BUTTON_ROW.format(name=prod.name(user), count=count), prod.id))
        i += 1
        order_sum += sum_

    if buttons_:
        return prods_text, order_sum, buttons
    else:
        return prods_text, order_sum


async def format_cart_message(user: TelegramUser):
    cart = await user.cart.all()
    if cart:
        rest = await (await (await user.cart.first()).category).restaurant
    else:
        return False, False

    prods_text, order_sum, buttons = await format_cart_rows(cart, user, True)

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

    elif select == 'open_now':
        await callback.message.edit_caption(
            caption=user.message.SELECT_REST_MESSAGE,
            reply_markup=await get_open_rest_keyboard(user)
        )

    elif select == 'main':
        await callback.message.delete()
        await bot.send_message(
            callback.from_user.id,
            user.message.BOT_MESSAGE,
            reply_markup=get_main_keyboard(user)
        )

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

    elif 'order' == select:
        cart = await user.cart.all()
        rest = await (await (await user.cart.first()).category).restaurant
        if cart and rest.is_work() and sum([i.price*c for i, c in cart.items()]) >= rest.min_sum:
            if user.address:
                message = user.message.USE_OLD_ADDRESS_MESSAGE
                keyboard = get_address_keyboard(user)
                user.state = 'old_address'
            else:
                message = user.message.SELECT_TIME_MESSAGE
                keyboard = get_time_keyboard(user)
                user.state = 'time'

            await user.save()
            await callback.message.answer(
                message,
                reply_markup=keyboard
            )

        else:
            text, keyboard = await format_cart_message(user)
            if not text:
                await callback.message.answer_photo(
                    photo=open('logo.jpg', 'rb'),
                    caption=user.message.CART_EMPTY_MESSAGE
                )
                return
            else:
                await callback.message.answer_photo(
                    photo=open('logo.jpg', 'rb'),
                    caption=text,
                    reply_markup=keyboard
                )
        await callback.message.delete()
        return

    elif '=' in select:
        id_ = int(select.split('=')[1])

        if 'mealcat' in select:
            try:
                await callback.message.edit_media(
                    InputMedia(media=open('logo.jpg',  'rb'), type='photo'),
                )
            except:
                pass

            prod_from_cart = await user.cart.first()
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

        elif 'restcat' in select:
            category = await RestaurantCategory.get_or_none(id=id_)
            if category is None:
                return
            rest = await category.restaurant
            if rest is None:
                return

            if not await compare_restaurants(user, rest, callback):
                return

            message = user.message.REST_MESSAGE.format(
                name=rest.name(user),
                description=rest.description(user),
                min_price=rest.min_sum,
                delivery=rest.delivery_price,
                time=f'{str(rest.start_time).split(":00+")[0]}-{str(rest.end_time).split(":00+")[0]}'
            )

            keyboard = await get_products_keyboard(category, user)

        elif 'prod=' in select or 'add' in select:
            product = await Product.get_or_none(id=id_)
            if product is None:
                return

            if not await compare_restaurants(user, await (await product.category).restaurant, callback):
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
                InputMedia(media=open('admin/files/' + shop.photo, 'rb'), type='photo'),
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
            service = await Service.get_or_none(id=id_)
            if service is None:
                return

            shop = await ServiceShop.get_or_none(id=id_)
            if shop is None:
                return

            order = await ServiceOrder.create(
                shop=shop,
                customer=user,
                product=service
            )

            message = user.message.SERVICE_ORDER_MESSAGE.format(id_=order.id)
            keyboard = go_main_keyboard(user)

            try:
                await bot.send_message(
                    shop.contact,
                    ORDER_SHOP_MESSAGE.format(
                        id_=order.id,
                        username=user.username,
                        name_ru=service.name_ru,
                        name_en=service.name_en
                    )
                )
            except Exception as e:
                print(traceback.format_exc())

        elif 'rest' in select:
            rest = await Restaurant.get_or_none(id=id_)
            if rest is None:
                return

            if not await compare_restaurants(user, rest, callback):
                return

            message = user.message.REST_MESSAGE.format(
                name=rest.name(user),
                description=rest.description(user),
                min_price=rest.min_sum,
                delivery=rest.delivery_price,
                time=f'{str(rest.start_time).split(":00+")[0]}-{str(rest.end_time).split(":00+")[0]}'
            )
            keyboard = await get_rest_cat_keyboard(rest, user)

            await callback.message.edit_media(
                InputMedia(media=open('admin/files/'+rest.photo, 'rb'), type='photo'),
                reply_markup=keyboard
            )

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
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        return

    if message.text == user.button.MAIN_MENU_BUTTON and user.state == '':
        await bot.send_message(
            message.from_user.id,
            user.message.BOT_MESSAGE,
            reply_markup=get_main_keyboard(user)
        )

        await bot.send_photo(
            message_.from_user.id,
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

    elif message.text == user.button.OLD_ADDRESS_BUTTON or message.text == user.button.NEW_ADDRESS_BUTTON:
        if user.state != 'old_address':
            await message.delete()
            return

        elif message.text == user.button.OLD_ADDRESS_BUTTON:
            shop = await (await (await user.cart.first()).category).restaurant
            order = await Order.create(
                shop=shop,
                customer=user,
                address=user.address,
                name=user.name,
                cart_=user.cart_
            )
            user.state = f'time={order.id}'
        else:
            user.state = 'time'

        await user.save()
        await message.answer(
            user.message.SELECT_TIME_MESSAGE,
            reply_markup=get_time_keyboard(user)
        )

    elif user.state == 'time':
        if message.text == user.button.CANCEL_BUTTON:
            user.state = ''
            user.cart_ = ';'
            await user.save()

            await bot.send_message(
                message.from_user.id,
                user.message.BOT_MESSAGE,
                reply_markup=get_main_keyboard(user)
            )

            await bot.send_photo(
                message_.from_user.id,
                photo=open('logo.jpg', 'rb'),
                caption=user.message.START_MESSAGE,
                reply_markup=get_meal_or_service_keyboard(user)
            )
            return

        cart = await user.cart.all()
        shop = await (await (await user.cart.first()).category).restaurant
        order = await Order.create(
            shop=shop,
            customer=user,
            delivery_time=message.text,
            cart_=user.cart_
        )
        user.state = 'area=' + str(order.id)
        await user.save()
        await message.answer(
            user.message.SELECT_AREA_MESSAGE,
            reply_markup=get_area_keyboard(user)
        )

    elif '=' in user.state:
        order = await Order.get_or_none(id=int(user.state.split('=')[1]))
        if order is None:
            user.state = ''
            await message.delete()
            await user.save()
            return

        elif message.text == user.button.CANCEL_BUTTON:
            user.state = ''
            user.cart_ = ';'
            await order.delete()
            await user.save()

            await bot.send_message(
                message.from_user.id,
                user.message.BOT_MESSAGE,
                reply_markup=get_main_keyboard(user)
            )

            await bot.send_photo(
                message_.from_user.id,
                photo=open('logo.jpg', 'rb'),
                caption=user.message.START_MESSAGE,
                reply_markup=get_meal_or_service_keyboard(user)
            )

        elif 'chat' in user.state:
            if 'supplier_chat' in user.state:
                if await order.customer == user:
                    name = order.name
                else:
                    user.state = ''
                    await user.save()
                    await message.delete()
                    return
            elif 'shop_chat' in user.state:
                if (await order.shop).contact == user.telegram_id or (await order.shop).contact == message.chat.id:
                    name = (await order.shop).name_
                else:
                    user.state = ''
                    await user.save()
                    await message.delete()
                    return
            else:
                return
            mess_id = int(user.state.split(';')[0])
            tz = pytz.timezone('Europe/Moscow')
            now = datetime.now(tz).time()

            await Message.create(
                order=order,
                name=name,
                text=message.text,
                time=now
            )

            await bot.edit_message_text(
                await order.chat(user),
                message.chat.id,
                mess_id
            )
            await message.delete()

        elif 'time' in user.state:
            order.delivery_time = message.text[:64]
            await order.save()
            user.state = f'comm={order.id}'
            await user.save()
            await message.answer(
                user.message.COMMUNICATION_MESSAGE,
                reply_markup=get_communication_keyboard(user)
            )

        elif 'area' in user.state:
            if message.text in (user.button.CENTER_BUTTON, user.button.SOUTH_BUTTON,
                                user.button.NORTH_BUTTON, user.button.BIGC_BUTTON):
                order.address += f'Area: {message.text}<br>'
                user.state = f'geo={order.id}'
                await order.save()
                await user.save()
                await message.answer(
                    user.message.INPUT_ADDRESS_MESSAGE,
                    reply_markup=get_geo_keyboard(user)
                )
            else:
                await message_.delete()

        elif 'geo' in user.state:
            if message.location:
                order.address += f'Latitude/Longitude: {message.location.latitude} {message.location.longitude}<br>'
            else:
                order.address += f'Address: {message.text}<br>'

            user.state = f'ads={order.id}'
            await user.save()
            await order.save()

            await message.answer(
                user.message.ADDRESS_APPS_MESSAGE,
                reply_markup=get_ads_keyboard(user)
            )

        elif 'ads' in user.state:
            if message.text != user.button.NO_ADS_BUTTON:
                order.address += f'Additions: {message.text}<br>'
                await order.save()

            if not user.address:
                user.address = order.address

            user.state = f'name={order.id}'
            await user.save()

            await message.answer(
                user.message.NAME_MESSAGE,
                reply_markup=get_cancel_keyboard(user)
            )

        elif 'name' in user.state:
            order.name = message.text[:128]
            if not user.name:
                user.name = message.text[:128]
            user.state = f'comm={order.id}'
            await user.save()
            await order.save()

            await message.answer(
                user.message.COMMUNICATION_MESSAGE,
                reply_markup=get_communication_keyboard(user)
            )

        elif 'comm' in user.state:
            if message.text == user.button.TELEGRAM_BUTTON:
                order.active = True
                await order.save()
                user.state = ''
                await user.save()
                prods_text, order_sum = await format_cart_rows(await order.cart.all(), user, deal=True)
                text = user.message.ORDER_MESSAGE.format(
                    id_=order.id,
                    delivery=(await order.shop).delivery_price,
                    sum=order_sum,
                    rows=prods_text
                )
                keyboard = get_end_order_keyboard(user)
                try:
                    await bot.send_message(
                        (await order.shop).contact,
                        await order.message(prods_text, order_sum)
                    )
                except Exception as e:
                    print(traceback.format_exc())

            elif message.text == user.button.WHATSAPP_BUTTON:
                user.state = f'whatsapp={order.id}'
                text = user.message.WHATSAPP_MESSAGE
                keyboard = get_cancel_keyboard(user)

            elif message.text == user.button.PHONE_BUTTON:
                user.state = f'phone={order.id}'
                text = user.message.PHONE_MESSAGE
                keyboard = get_cancel_keyboard(user)

            else:
                await message.delete()
                return

            await user.save()
            await message.answer(
                text,
                reply_markup=keyboard
            )

        elif 'whatsapp' in user.state:
            if message.text[0] == '+':
                try:
                    int(message.text[1:].replace(' ', ''))
                except TypeError:
                    await message.delete()
                else:
                    if len(message.text[1:].replace(' ', '')) == 11:
                        order.communication = f'WhatsApp {message.text}'[:32]
                        await order.save()
                        prods_text, order_sum = await format_cart_rows(await order.cart.all(), user, deal=True)
                        user.state = ''
                        await user.save()

                        await message.answer(
                            user.message.ORDER_MESSAGE.format(
                                id_=order.id,
                                delivery=(await order.shop).delivery_price,
                                sum=order_sum,
                                rows=prods_text
                            ),
                            reply_markup=get_end_order_keyboard(user)
                        )
                        try:
                            await bot.send_message(
                                (await order.shop).contact,
                                await order.message(prods_text, order_sum)
                            )
                        except Exception as e:
                            print(traceback.format_exc())
                    else:
                        await message.delete()

            else:
                await message.delete()

        elif 'phone' in user.state:
            try:
                int(message.text.replace('+', '').replace(' ', ''))
            except TypeError:
                await message.delete()
            else:
                order.communication = f'Phone {message.text}'[:32]
                await order.save()
                prods_text, order_sum = await format_cart_rows(await order.cart.all(), user, deal=True)
                user.state = ''
                await user.save()

                await message.answer(
                    user.message.ORDER_MESSAGE.format(
                        id_=order.id,
                        delivery=(await order.shop).delivery_price,
                        sum=order_sum,
                        rows=prods_text
                    ),
                    reply_markup=get_end_order_keyboard(user)
                )
                try:
                    await bot.send_message(
                        (await order.shop).contact,
                        await order.message(prods_text, order_sum)
                    )
                except Exception as e:
                    print(traceback.format_exc())
    else:
        await message_.delete()


@dp.message_handler(RegexpCommandsFilter(regexp_commands=['chat([0-9]*)']))
@dp.throttled(rate=FLOOD_RATE)
async def chat(message: types.Message, regexp_command):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    order = await Order.get_or_none(id=int(regexp_command.group(1)), active=True)
    if order is None:
        await message.delete()

    if (await order.customer).telegram_id == user.telegram_id:
        user.state = f'supplier_chat={order.id}'
    elif (await order.shop).contact == user.telegram_id or (await order.shop).contact == message.chat.id:
        user.state = f'shop_chat={order.id}'

    message = await message.answer(
        await order.chat(user)
    )
    user.state = str(message.message_id) + ';' + user.state
    await user.save()





