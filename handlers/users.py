import random
import traceback
from datetime import datetime

import pytz
from aiogram.dispatcher.filters import CommandStart, RegexpCommandsFilter
from aiogram.types import InputMedia
from flask_security.utils import get_message

from data.config import tables_order, FLOOD_RATE
from data.messages import tables_text, roles_en_ru
from data.passgen import get_secret
from db.models import TelegramUser, Field, AllFields
from keyboards.keyboards import *
from loader import dp, bot


@dp.message_handler(CommandStart())
@dp.throttled(rate=FLOOD_RATE)
async def bot_start(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None or not await user.inviter:
        if user is None:
            user = await TelegramUser.create(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
            )
        if '=' in message.text:
            referral_url = message.text.split('=')[-1]
            id_ = referral_url.split('_')[-1]
            inviter = await TelegramUser.get_or_none(id=id_)
            if inviter:
                if inviter.referral_url == referral_url:
                    user.inviter = inviter
                    await user.save()
                    await message.answer(
                        await get_message('start'),
                        reply_markup=await get_main_keyboard()
                    )
                    await bot.send_message(
                        inviter.telegram_id,
                        (await get_message('new_referral')).format(name=user.username)
                    )
                    return

        await message.answer(
            await get_message('incorrect_id'),
        )
        await message.delete()

    else:
        await message.answer(
            await get_message('start'),
            reply_markup=await get_main_keyboard()
        )


async def get_captcha(callback, back, to, field=None):
    num1 = random.randint(10, 50)
    num2 = random.randint(10, 50)
    result = num1 + num2
    text = (await get_message('captcha')).format(
        num1=num1,
        num2=num2,
        result=result
    )
    keyboard = get_captcha_keyboard(result, to, back, field if field else '')
    await callback.message.edit_caption(
        caption=text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(select_callback.filter())
@dp.throttled(rate=FLOOD_RATE)
async def main_menu(callback: types.CallbackQuery, callback_data):
    await callback.answer()
    tables_order.index()

    user = await TelegramUser.get_or_none(telegram_id=callback.from_user.id)
    if user is None:
        return

    select = callback_data.get('select')

    if user.state != '':
        return

    elif '_info' in select:
        text = await get_message(select)

        await bot.edit_message_caption(
            user.telegram_id,
            callback.message.message_id,
            caption=text,
        )

    elif 'open_' in select:
        table = select.replace('open_', '')
        if tables_order.index(user.max_field) > tables_order.index(table):
            await callback.message.delete()

        for game, role in (await user.games()).items():
            if game.type == table:
                await callback.message.edit_media(
                    InputMedia(open(f'photo/{game.type}.png', 'rb'))
                )
                if 'donor' not in role:
                    await callback.message.edit_caption(
                        caption=(await get_message('table_info')).format(
                            name = await get_button(f'{table}_name'),
                            id=game.id,
                            count=game.donor_count(),
                            max=4 if game.type == 'start' else 8,
                            role=await get_button(role)
                        ),
                        reply_markup=await get_player_keyboard(game, role)
                    )
                else:
                    await callback.message.edit_caption(
                        caption=(await get_message('table_donor_info')).format(
                            name=await get_button(f'{table}_name'),
                            id=game.id,
                            count=game.donor_count(),
                            max=4 if game.type == 'start' else 8,
                            role=await get_button(role)
                        ),
                        reply_markup=await get_donor_keyboard(game, role)
                    )
            else:
                if table != 'start' and (await Config.get(id=1)).keys_system and getattr(user, f'{table}_key') < 1:
                    await callback.answer(
                        (await get_message('need_referrals')).format(count=2 - len(await user.referrals.all()) % 2),
                        show_alert=True
                    )
                    return
                while True:
                    id_ = random.randint(1, (await Field.all().count()))
                    field = (await Field.filter(not_full=True, type=table, id=id_))[0]
                    if field:
                        break

                    await callback.message.edit_media(
                        InputMedia(open(f'photo/{game.type}.png', 'rb'))
                    )
                    await field.add_donor(user)
                    await callback.message.edit_caption(
                        caption=(await get_message('table_donor_info')).format(
                            name=await get_button(f'{table}_name'),
                            id=game.id,
                            count=game.donor_count(),
                            max=4 if game.type == 'start' else 8,
                            role=await get_button(role)
                        ),
                        reply_markup=await get_donor_keyboard(game, role)
                    )

    elif select == 'open':
        await callback.message.edit_media(
            InputMedia(open((await Config.get(id=1)).about_photo, 'rb'))
        )
        await callback.message.edit_caption(
            caption=await get_message('open_table'),
            reply_markup=await get_tables(user)
        )

    elif 'captcha' in select:
        back, to, field_id = select.split(';')[1:]
        await get_captcha(callback, back, to, field_id)

    elif 'make_gift_' in select:
        field = await Field.get_or_none(id=int(select.replace('make_gift_')))
        if not field:
            await callback.message.delete()
            return
        price = getattr(await TablePrice.get(id=1), field.type)

        if field == 'start':
            text = await get_message('start_make_gift').format(
                master_price=price
            )
        else:
            text = (await get_message('make_gift')).format(
                master_price=price,
                mentor_price=price//2
            )
        await callback.message.edit_caption(
            caption=text,
            reply_markup=await get_donor_gift_keyboard(field, price)
        )
    elif 'notify_users_' in select:
        field = await Field.get_or_none(id=int(select.replace('notify_users_')))
        if not field:
            await callback.message.delete()
            return
        await callback.answer(await get_message('success_notification'))

        for game, role in (await user.games()).items():
            if game == field:
                if getattr(field, f'{role}_notify'):
                    return
                else:
                    setattr(field, f'{role}_notify', True)
                    await field.save()
                    users = [await field.master, await field.mentor1, await field.mentor2]
                    for us in users:
                        await bot.send_message(
                            us.telegram_id,
                            (await get_message('gift_notification')).format(
                                donor=user.username,
                                table=await get_button(f'{field.type}_name')
                            )
                        )
    elif 'field' in select:
        field = await Field.get_or_none(id=int(select.split('_')[-1]))
        if not field:
            await callback.message.delete()
            return

        elif 'team_list' in select:
            text = ''
            row = await get_message('team_list_row')
            users = await field.users()
            text += row.format(
                role='Мастер',
                username = users['master'].username,
                inviter = (await users['master'].inviter).username,
                refs = len(await users['master'].referrals),
            )
            i = 0
            for mentor in users['mentors']:
                i += 1
                text += row.format(
                    role=f'Ментор {i}',
                    username=mentor.username,
                    inviter=(await mentor.inviter).username,
                    refs=len(await mentor.referrals),
                )
            i = 0
            if field.type != 'start':
                for partner in users['partners']:
                    i += 1
                    text += row.format(
                        role=f'Партнер {i}',
                        username=partner.username,
                        inviter=(await partner.inviter).username,
                        refs=len(await partner.referrals),
                    )

            await callback.message.edit_caption(
                caption=text,
                reply_markup=await back_on_table(field)
            )

        elif 'see_donors' in select:
            for game, role in (await user.games()).items():
                if game == field:
                    await callback.message.edit_reply_markup(
                        reply_markup=await donors_keyboard(field, role)
                    )

        elif 'field_donor_list_' in select:
            users = await field.users()
            text = ''
            row = await get_message('team_list_row')
            i = 0
            for donor in users['donors']:
                i += 1
                text += row.format(
                    role=f'Даритель {i}',
                    username=donor.username,
                    inviter=(await donor.inviter).username,
                    refs=len(await donor.referrals),
                )


    elif 'confirm_exit' in select:
        field = await Field.get_or_none(id=int(select.replace('exit_')))
        if not field:
            await callback.message.delete()
            return
        for game, role in (await user.games()).items():
            if game == field:
                if field.donor_valid(int(role[-1])):
                    await callback.message.delete()
                    return
                else:
                    await field.remove_donor(user)
                    await callback.message.answer(
                        await get_message('start'),
                        reply_markup=await get_main_keyboard()
                    )
                    await callback.message.delete()
                    return

        await callback.message.delete()

    elif 'exit_' in select:
        field = await Field.get_or_none(id=int(select.replace('exit_')))
        if not field:
            await callback.message.delete()
            return
        if field.donor_valid(user):

        await callback.answer(await get_message('exit_notification'), show_alert=True)
        await get_captcha(callback, f'open_{field.type}', 'confirm_exit', field.id)


@dp.message_handler()
@dp.throttled(rate=FLOOD_RATE)
async def listen_handler(message: types.Message):
    message_ = message
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        await message.delete()

    elif not user.inviter:
        inviter = await TelegramUser.get_or_none(id=int(message.text.split('_')[-1]))
        if inviter is None:
            await message.answer(
                await get_message('incorrect_id')
            )
        else:
            if inviter.referral_url == message.text:
                user.inviter = inviter
                await user.save()
                await message.answer(
                    await get_message('start'),
                    reply_markup=await get_main_keyboard()
                )
            else:
                await message.answer(
                    await get_message('incorrect_id')
                )

    elif message.text == await get_button('open'):
        await message.answer_photo(
            photo=open((await Config.get(id=1)).about_photo, 'rb'),
            caption=await get_message('open_table'),
            reply_markup=await get_tables(user)
        )

    elif message.text == await get_button('about'):
        await message.answer_photo(
            photo=open((await Config.get(id=1)).about_photo, 'rb'),
            caption=await get_message('about'),
            reply_markup=await get_about_keyboard()
        )

    elif message.text == await get_button('pdf'):
        await message.answer_document(
            document=open((await Config.get_or_none(id=1)).pdf, 'rb')
        )

    elif message.text == await get_button('status'):
        tables = await user.games()
        if tables:
            table_text = ''
            for table, role in tables.items():
                table_text += tables_text[table.type].format(
                    status=await get_button(role),
                    count=len((await table.users())['donors'])
                )

        else:
            table_text = await get_message('no_tables')

        await message.answer(
            (await get_message('status')).format(
                id=user.telegram_id, name=user.username,
                iviter=(await user.inviter).username,
                count=len(await user.referrals.all()),
                tables=table_text
            ),
            reply_markup=await get_status_keyboard()
        )

    elif message.text == await get_button('reff'):
        if not user.active:
            await message.answer(
                await get_message('no_active')
            )
        else:
            if not user.referral_url:
                user.referral_url = get_secret(user)
                await user.save()

            await message.answer(
                (await get_message('ref_url')).format(
                    code=user.referral_url
                )
            )

    elif message.text == await get_button('suppport'):
        await message.answer(
            await get_message('support'),
            reply_markup=await get_support_keyboard()
        )







