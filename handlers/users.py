import random
import time
import traceback
from datetime import datetime

import pytz
from aiogram.dispatcher.filters import CommandStart, RegexpCommandsFilter
from aiogram.types import InputMedia
from tortoise.expressions import Q

from data.config import tables_order, FLOOD_RATE
from data.messages import tables_text, roles_en_ru
from data.passgen import get_secret
from db.models import TelegramUser, Table, get_message
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
            try:
                referral_url = message.text.split('=')[-1]
                id_ = referral_url.split('_')[-1]
                inviter = await TelegramUser.get_or_none(id=id_)
            except:
                await message.delete()
                return
            if inviter:
                if inviter.referral_url == referral_url:
                    user.inviter = inviter
                    await user.save()
                    if len(inviter.referrals.all()) % 2 == 0:
                        inviter.wood_key += 1
                        inviter.bronze_key += 1
                        inviter.silver_key += 1
                        inviter.gold_key += 1
                        inviter.platinum_key += 1
                        inviter.legendary_key += 1
                        await inviter.save()

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
        num2=num2
    )
    keyboard = await get_captcha_keyboard(result, to, back, field if field else '')
    await callback.message.edit_caption(
        caption=text,
        reply_markup=keyboard
    )


@dp.callback_query_handler(select_callback.filter())
@dp.throttled(rate=FLOOD_RATE)
async def main_menu(callback: types.CallbackQuery, callback_data):
    await callback.answer()
    user = await TelegramUser.get_or_none(telegram_id=callback.from_user.id)
    if user is None:
        return

    select = callback_data.get('select')

    if '_info' in select:
        text = await get_message(select)

        await bot.edit_message_caption(
            user.telegram_id,
            callback.message.message_id,
            caption=text,
            reply_markup=await get_back_to_info_keyboard()
        )

    elif select == 'info':
        await bot.edit_message_caption(
            user.telegram_id,
            callback.message.message_id,
            caption=await get_message('about'),
            reply_markup=await get_about_keyboard()
        )

    elif 'open_' in select:
        table = select.replace('open_', '')
        if tables_order.index(user.max_field) > tables_order.index(table):
            await callback.message.delete()

        for game, role in (await user.games()).items():
            if game.type == table:
                await callback.message.edit_media(
                    InputMedia(media=open(f'photo/{game.type}.png', 'rb'), type='photo')
                )
                if 'donor' not in role:
                    await callback.message.edit_caption(
                        caption=(await get_message('table_info')).format(
                            name = await get_button(f'{table}_name'),
                            id=game.id,
                            count=await game.donor_count(),
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
                            count=await game.donor_count(),
                            max=4 if game.type == 'start' else 8,
                            role=await get_button(role)
                        ),
                        reply_markup=await get_donor_keyboard(game, role)
                    )
                return

        if table != 'start':
            keys = getattr(user, f'{table}_key')
        block = getattr(user, f'{table}_block')
        if block:
            if block < time.time():
                setattr(user, f'{table}_block', None)
                await user.save()
            else:
                await callback.answer(
                    (await get_message('you_block')),
                    show_alert=True
                )
                return

        if table != 'start' and (await Config.get(id=1)).keys_system and keys < 1:
            await callback.answer(
                (await get_message('need_referrals')).format(count=2 - len(await user.referrals.all()) % 2),
                show_alert=True
            )
            return
        while True:
            field = (await Table.filter(
                Q(Q(donor1=None), Q(donor2=None), Q(donor3=None),
                  Q(donor4=None), Q(donor5=None), Q(donor6=None),
                  Q(donor7=None), Q(donor8=None), join_type="OR") & Q(type=table)
            ).limit(1))[0]
            if field:
                await callback.message.edit_media(
                    InputMedia(media=open(f'photo/{table}.png', 'rb'), type='photo')
                )
                donor_num = await field.add_donor(user)
                if table != 'start' and (await Config.get(id=1)).keys_system and keys > 1:
                    setattr(user, f'{table}_key', keys - 1)
                    await user.save()

                await callback.message.edit_caption(
                    caption=(await get_message('table_donor_info')).format(
                        name=await get_button(f'{table}_name'),
                        id=field.id,
                        count=await field.donor_count(),
                        max=4 if field.type == 'start' else 8,
                        role=(await get_button('donor')) + str(donor_num)
                    ),
                    reply_markup=await get_donor_keyboard(field, f'donor{donor_num}')
                )
                for key, users in (await field.users()).items():
                    if key == 'donors':
                        continue
                    for player in users:
                        if player:
                            await bot.send_message(
                                player.telegram_id,
                                (await get_message('new_donor')).format(
                                    table=await get_button(f'{field.type}_name')
                                )
                            )
            else:
                await callback.answer()
                return

    elif select == 'open':
        await callback.message.edit_media(
            InputMedia(media=(open(('admin/files/' + (await Config.get(id=1)).about_photo), 'rb')), type='photo')
        )
        await callback.message.edit_caption(
            caption=await get_message('open_table'),
            reply_markup=await get_tables(user)
        )

    elif 'captcha' in select:
        back, to, field_id = select.split('.')[1:]
        await get_captcha(callback, back, to, field_id)

    elif 'make_gift_' in select:
        field = await Table.get_or_none(id=int(select.replace('make_gift_', '')))
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
        field = await Table.get_or_none(id=int(select.replace('notify_users_', '')))
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
        field = await Table.get_or_none(id=int(select.split('_')[-1]))
        if not field:
            await callback.message.delete()
            return
        role = None
        break_ = False
        for game, role in (await user.games()).items():
            if game == field:
                break_ = True
                role = role

        if break_:
            await callback.message.delete()
            return

        if 'team_list' in select:
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

            await callback.message.edit_caption(
                caption=text,
                reply_markup=await back_on_table(field)
            )

        elif 'field_donor' in select:
            donor_num = select.split('_')[2]
            donor = await getattr(field, f'donor{donor_num}')
            if not donor:
                await callback.message.delete()
                return

            async def status_text():
                if 'master' in role or 'mentor' in role:
                    if getattr(field, f'donor_{donor_num}_{role}'):
                        return await get_message('donor_is_valid'), True
                    else:
                        return await get_message('donor_not_valid'), False
                else:
                    return '', True

            status_text_, valid = await status_text()
            text = (await get_message('field_donor_info')).format(
                status=status_text_,
                role = f'Даритель {donor_num}',
                username = donor.username,
                inviter = (await donor.inviter).username,
                refs = len(await donor.referrals),
            )

            await callback.message.edit_caption(
                caption=text,
                reply_markup=await get_donor_info_keyboard(field, donor, valid, donor_num, role)
            )

        elif 'field_valid_' in select:
            donor_num = select.split('_')[2]
            donor = await getattr(field, f'donor{donor_num}')
            if not donor:
                return

            if 'mentor' in role or 'master' in role:
                try:
                    setattr(field, f'donor_{donor_num}_{role}', True)
                    await field.save()
                    await bot.send_message(
                        donor.telegram_id,
                        await get_message('you_valid').format(
                            username=user.username,
                            type=await get_button(f'{field.type}_name')
                        )
                    )

                    await callback.message.edit_caption(
                        caption=(await get_message('table_info')).format(
                            name=await get_button(f'{field.type}_name'),
                            id=field.id,
                            count=await field.donor_count(),
                            max=4 if field.type == 'start' else 8,
                            role=await get_button(role)
                        ),
                        reply_markup=await get_player_keyboard(field, role)
                    )

                    if field.donor_valid(donor_num):
                        if field.type == 'start':
                            donor.active = True
                            await donor.save()

                        if await field.is_full():
                            max_donor = 9
                            if field.type == 'start':
                                max_donor = 5
                            for i in range(1, max_donor):
                                if field.donor_valid(i):
                                    pass
                                else:
                                    return
                            for i in range(1, max_donor):
                                setattr(field, f'donor_{donor_num}_mentor1', False)
                                setattr(field, f'donor_{donor_num}_mentor2', False)
                                setattr(field, f'donor_{donor_num}_master', False)
                                setattr(field, f'donor{donor_num}_notify', False)
                            master = await field.master
                            await bot.send_message(
                                master.telegram_id,
                                (await get_message('field_finish')).format(
                                    type=await get_button(f'{field.type}_name')
                                )
                            )
                            if master.max_field != 'legendary':
                                if master.max_field != 'start' or (master.max_field == 'start' and len(await master.referrals.all()) > 2):
                                    master.max_field = tables_order[tables_order.index(master.max_field) + 1]
                                    await master.save()

                            text = get_message('table_update').format(
                                type=await get_button(f'{field.type}_name'),
                            )
                            for role, players in (await field.users()).items():
                                for player in players:
                                    await bot.send_message(
                                        player.telegram_id,
                                        text
                                    )

                            if field != 'start':
                                partner1 = await field.donor5,
                                partner2 = await field.donor6,
                                partner3 = await field.donor7,
                                partner4 = await field.donor8,

                                mentor1 = await field.partner3
                                mentor2 = await field.partner4
                                master = await field.mentor2

                                field.master = await field.mentor1
                                field.mentor1 = await field.partner1
                                field.mentor2 = await field.partner2

                                field.partner1 = await field.donor1
                                field.partner2 = await field.donor2
                                field.partner3 = await field.donor3
                                field.partner4 = await field.donor4

                                await field.save()

                                new_field = await Table(
                                    partner1=partner1,
                                    partner2=partner2,
                                    partner3=partner3,
                                    partner4=partner4,
                                    mentor1=mentor1,
                                    mentor2=mentor2,
                                    master=master,
                                    type=field.type
                                )
                            else:
                                mentor1 = await field.donor3
                                mentor2 = await field.donor4
                                master = await field.mentor2

                                field.master = await field.mentor1
                                field.mentor1 = await field.donor1
                                field.mentor2 = await field.donor2

                                await field.save()

                                new_field = await Table(
                                    mentor1=mentor1,
                                    mentor2=mentor2,
                                    master=master,
                                    type=field.type
                                )

                except Exception as e:
                    print(traceback.format_exc())

        elif 'field_delete_' in select:
            if role != 'master':
                await callback.message.delete()
                return

            donor_num = select.split('_')[2]
            donor = await getattr(field, f'donor{donor_num}')
            if not donor:
                await callback.message.delete()
                return
            if not (
                getattr(field, f'donor_{donor_num}_mentor1') or
                getattr(field, f'donor_{donor_num}_mentor1')):

                setattr(field, f'donor{donor_num}', None)
                setattr(field, f'donor_{donor_num}_mentor1', False)
                setattr(field, f'donor_{donor_num}_mentor2', False)
                await field.save()
                await bot.send_message(
                    donor.telegram_id,
                    (await get_message('you_excluded')).format(
                        type=await get_button(f'{field.type}_name')
                    )
                )
                await callback.message.edit_caption(
                    caption=(await get_message('table_info')).format(
                        name=await get_button(f'{field.type}_name'),
                        id=field.id,
                        count=await field.donor_count(),
                        max=4 if field.type == 'start' else 8,
                        role=await get_button(role)
                    ),
                    reply_markup=await get_player_keyboard(field, role)
                )

        else:
            users = await field.users()
            if 'master' in select:
                player = users['master']
                role = 'Мастер'

            elif 'mentor' in select:
                player = users['mentors'][int(select[-1])]
                role = f'Ментор {select[-1]}'

            elif 'patrner' in select:
                player = users['partners'][int(select[-1])]
                role = f'Партнер {select[-1]}'
            else:
                return

            text = (await get_message('team_list_row')).format(
                role=role,
                username=player.username,
                inviter=(await player.inviter).username,
                refs=len(await player.referrals),
            )

            await callback.message.edit_caption(
                caption=text,
                reply_markup=await get_user_keyboard(field, player)
            )


    elif 'confirm_exit' in select:
        field = await Table.get_or_none(id=int(select.replace('exit_', '')))
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
        field = await Table.get_or_none(id=int(select.replace('exit_', '')))
        if not field:
            await callback.message.delete()
            return
        for game, role in (await user.games()).items():
            if game == field:
                if field.donor_valid(int(role[-1])):
                    await callback.message.delete()
                    return

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
        try:
            inviter = await TelegramUser.get_or_none(id=int(message.text.split('_')[-1]))
        except:
            await message.delete()
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
            photo=open(('admin/files/' + (await Config.get(id=1)).about_photo), 'rb'),
            caption=await get_message('open_table'),
            reply_markup=await get_tables(user)
        )

    elif message.text == await get_button('about'):
        await message.answer_photo(
            photo=open(('admin/files/' + (await Config.get(id=1)).about_photo), 'rb'),
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
                inviter=(await user.inviter).username,
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

    elif message.text == await get_button('support'):
        await message.answer(
            await get_message('support'),
            reply_markup=await get_support_keyboard()
        )







