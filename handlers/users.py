import io
import os
import time
import traceback

from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InputMedia, InputFile
from aiogram.utils.exceptions import BotBlocked
from tortoise.expressions import Q

from data.config import FLOOD_RATE
from data.messages import tables_text
from data.passgen import get_secret
from db.models import get_message
from keyboards.keyboards import *
from loader import dp, bot


@dp.message_handler(commands=['mail'])
@dp.throttled(rate=FLOOD_RATE)
async def mail_handler(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    admin = await user.admin
    if user is None or not admin:
        await message.delete()
        return

    admin.state = 'mail'
    await admin.save()
    await message.answer(
        await get_message('mail'),
        reply_markup=await get_delete_keyboard()
    )


@dp.message_handler(CommandStart())
@dp.throttled(rate=FLOOD_RATE)
async def bot_start(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    print(message.text)
    if user is None or not await user.inviter:
        if user is None:
            user = await TelegramUser.create(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                name=message.from_user.full_name
            )
        if ' ' in message.text:
            try:
                referral_url = message.text.split(' ')[-1]
                id_ = referral_url.split('_')[-1]
                inviter = await TelegramUser.get_or_none(id=int(id_)-13560)
            except:
                await message.delete()
                return
            if inviter:
                if inviter.referral_url == referral_url:
                    user.inviter = inviter
                    await user.save()

                    await message.answer(
                        await get_message('agreement'),
                        reply_markup=await get_agreement_keyboard()
                    )

        await message.delete()

    else:
        if user.agree:
            await message.answer(
                await get_message('start'),
                reply_markup=await get_main_keyboard()
            )
        else:
            await message.delete()


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
    user = await TelegramUser.get_or_none(telegram_id=callback.from_user.id)
    if user is None or not await user.inviter:
        return

    select = callback_data.get('select')
    print(select)

    if 'agree' in select:
        user.agree = True
        await user.save()
        inviter = await user.inviter
        await callback.message.answer(
            await get_message('start'),
            reply_markup=await get_main_keyboard()
        )
        await callback.message.delete()
        await bot.send_message(
            inviter.telegram_id,
            (await get_message('new_referral')).format(name=user.username)
        )
        return

    elif not user.agree or user.ban:
        await callback.answer()
        return

    if 'captcha' in select:
        await callback.answer()

        to, back, field_id = select.split('.')[1:]
        print(back, to, field_id)
        await get_captcha(callback, back, to, field_id)

    elif '_info' in select:
        await callback.answer()

        text = await get_message(select)

        await bot.edit_message_caption(
            user.telegram_id,
            callback.message.message_id,
            caption=text,
            reply_markup=await get_back_to_info_keyboard()
        )

    elif select == 'info':
        await callback.answer()

        await bot.edit_message_caption(
            user.telegram_id,
            callback.message.message_id,
            caption=await get_message('about'),
            reply_markup=await get_about_keyboard()
        )

    elif 'open_' in select:
        table = select.replace('open_', '')
        if tables_order.index(user.max_field) < tables_order.index(table):
            await callback.message.edit_media(
                InputMedia(media=open(f'photo/{table}.png', 'rb'), type='photo'),
                reply_markup=await get_tables(user)
            )
            await callback.answer(await get_message('not_allowed'), show_alert=True)
            return
            # await callback.message.delete()

        for game, role in (await user.games()).items():
            if game.type == table:
                await callback.message.delete()
                mess = await callback.message.answer_photo(
                    photo=open(f'photo/{game.type}.png', 'rb')
                )
                if 'donor' not in role or game.donor_valid(int(role[-1])):
                    await mess.edit_caption(
                        caption=(await get_message('table_info')).format(
                            name=await get_button(f'{table}_name'),
                            id=game.id,
                            count=await game.donor_count(),
                            max=4 if game.type == 'start' else 8,
                            role=(await get_button(role[:-1])) + ' ' + role[-1] if role != 'master' else await get_button(role)
                        ),
                        reply_markup=await get_player_keyboard(game, role)
                    )
                else:
                    await mess.edit_caption(
                        caption=(await get_message('donor_table_info')).format(
                            name=await get_button(f'{table}_name'),
                            id=game.id,
                            role=await get_button('donor') + ' ' + role[-1]
                        ),
                        reply_markup=await get_donor_keyboard(game, role)
                    )
                return

        inviter = await user.inviter
        keys = 1
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
                (await get_message('need_referrals')),
                show_alert=True
            )
            return
        await callback.answer()

        while True:
            field = None
            donor_num = None
            if table == 'start':
                for inviter_game, inviter_role in (await inviter.games()).items():
                    if inviter_game.type == 'start':
                        if await inviter_game.not_full:
                            field = inviter_game
                            if inviter_role == 'master':
                                donor_num = await field.add_donor(user)
                            elif inviter_role == 'mentor1':
                                donor_num = 1
                                if not await field.add_donor_num(user, 1):
                                    donor_num = 2
                                    if not await field.add_donor_num(user, 2):
                                        donor_num = await field.add_donor(user)
                            elif inviter_role == 'mentor2':
                                donor_num = 3
                                if not await field.add_donor_num(user, 3):
                                    donor_num = 4
                                    if not await field.add_donor_num(user, 4):
                                        donor_num = await field.add_donor(user)
                            else:
                                donor_num = None
            if not donor_num:
                if table != 'start':
                    field = (await Table.filter(
                        Q(Q(donor1=None), Q(donor2=None), Q(donor3=None),
                          Q(donor4=None), Q(donor5=None), Q(donor6=None),
                          Q(donor7=None), Q(donor8=None), join_type="OR") & Q(type=table) & Q(priority__not_isnull=True)
                    ).limit(1))
                    if not field:
                        field = (await Table.filter(
                            Q(Q(donor1=None), Q(donor2=None), Q(donor3=None),
                              Q(donor4=None), Q(donor5=None), Q(donor6=None),
                              Q(donor7=None), Q(donor8=None), join_type="OR") & Q(type=table)
                        ).limit(1))[0]
                    else:
                        field = field[0]
                else:
                    field = (await Table.filter(
                        Q(Q(donor1=None), Q(donor2=None), Q(donor3=None),
                          Q(donor4=None), join_type="OR") & Q(type=table) & Q(priority__not_isnull=True)
                    ).limit(1))
                    if not field:
                        field = (await Table.filter(
                            Q(Q(donor1=None), Q(donor2=None), Q(donor3=None),
                              Q(donor4=None), join_type="OR") & Q(type=table)
                        ).limit(1))[0]
                    else:
                        field = field[0]
            if field:
                await callback.message.edit_media(
                    InputMedia(media=open(f'photo/{table}.png', 'rb'), type='photo')
                )
                delete = time.time() + (await Config.get(id=1)).delete_time * 3600
                if not donor_num:
                    donor_num = await field.add_donor(user)
                setattr(field, f'donor{donor_num}_time', delete)
                if table != 'start' and (await Config.get(id=1)).keys_system:
                    setattr(user, f'{table}_key', keys - 1)
                    await user.save()

                await callback.message.edit_caption(
                    caption=(await get_message('donor_table_info')).format(
                        name=await get_button(f'{table}_name'),
                        id=field.id,
                        role=(await get_button('donor')) + str(donor_num)
                    ),
                    reply_markup=await get_donor_keyboard(field, f'donor{donor_num}')
                )
                for key, users in (await field.users(list_=True)).items():
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
                return
            else:
                await callback.answer()
                return

    elif select == 'open':
        await callback.answer()

        await callback.message.edit_media(
            InputMedia(media=(open('photo/start.png', 'rb')), type='photo')
        )
        await callback.message.edit_caption(
            caption=await get_message('open_table'),
            reply_markup=await get_tables(user)
        )

    elif 'make_gift_' in select:
        await callback.answer()

        field = await Table.get_or_none(id=int(select.replace('make_gift_', '')))
        if not field:
            await callback.message.delete()
            return
        price = getattr(await TablePrice.get(id=1), field.type)
        price_mentor = getattr(await TablePrice.get(id=1), f'{field.type}_mentor')

        if field == 'start':
            text = (await get_message('start_make_gift')).format(
                master_price=price
            )
        else:
            text = (await get_message('make_gift')).format(
                master_price=price,
                mentor_price=price_mentor
            )
        await callback.message.edit_caption(
            caption=text,
            reply_markup=await get_donor_gift_keyboard(field, price, price_mentor)
        )

    elif 'notify_users_' in select:
        field = await Table.get_or_none(id=int(select.replace('notify_users_', '')))
        if not field:
            await callback.answer()

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
                    if field.type == 'start':
                        users = [await field.master]
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
        break_ = True
        for game, role in (await user.games()).items():
            if game == field:
                break_ = False
                role = role

        if break_:
            await callback.answer()

            await callback.message.delete()
            return

        if 'team_list' in select:
            text = ''
            row = await get_message('team_list_row')
            users = await field.users()
            summ = getattr(await TablePrice.get(id=1), field.type)
            summ_mentor = getattr(await TablePrice.get(id=1), f'{field.type}_mentor')
            text += row.format(
                role=await get_button('master'),
                username=users['master'].username,
                inviter=(await users['master'].inviter).username,
                refs=len(await users['master'].referrals),
                name=users['master'].name,
                sum=summ
            )
            i = 0
            for mentor in users['mentors']:
                i += 1
                text += row.format(
                    role=f'{await get_button("mentor")} {i}' if field.type != 'start' else f'{await get_button("partner")} {i}',
                    username=mentor.username,
                    inviter=(await mentor.inviter).username,
                    refs=len(await mentor.referrals),
                    name = mentor.name,
                    sum=summ_mentor if field.type != 'start' else 'В очереди'
                )
            i = 0
            if field.type != 'start':
                for partner in users['partners']:
                    i += 1
                    text += row.format(
                        role=f'{await get_button("partner")} {i}',
                        username=partner.username,
                        inviter=(await partner.inviter).username,
                        refs=len(await partner.referrals),
                        name=partner.name,
                        sum='В очереди'
                    )
            await callback.message.delete()
            await callback.message.answer(
                text=text,
                reply_markup=await back_on_table(field)
            )

        elif 'field_donors' in select:
            await callback.message.edit_reply_markup(
                reply_markup=await donors_keyboard(field, role)
            )

        elif 'field_donor_list_' in select:
            users = await field.users()
            text = ''
            row = await get_message('donor_list_row')
            i = 0
            for donor in users['donors']:
                i += 1
                if donor:
                    text += row.format(
                        role=f'Даритель {i}',
                        username=donor.username,
                        name=donor.name,
                        inviter=(await donor.inviter).username,
                        refs=len(await donor.referrals),
                    )
            await callback.message.delete()
            await callback.message.answer(
                text=text,
                reply_markup=await back_on_table(field)
            )

        elif 'field_donor' in select:
            print(user.username, role, field.id)
            print('---------------------------')
            donor_num = select.split('_')[2]
            donor = await getattr(field, f'donor{donor_num}')
            if not donor:
                return

            async def status_text():
                if 'master' in role or ('mentor' in role and field.type != 'start'):
                    if getattr(field, f'donor_{donor_num}_{role}'):
                        return await get_message('donor_is_valid'), True
                    else:
                        return await get_message('donor_not_valid'), False
                else:
                    return '', True

            status_text_, valid = await status_text()
            text = (await get_message('field_donor_info')).format(
                status=status_text_,
                role=f'Даритель {donor_num}',
                name=donor.name,
                username=donor.username,
                id=donor.telegram_id,
                inviter=(await donor.inviter).username,
                refs=len(await donor.referrals),
            )

            await callback.message.edit_caption(
                caption=text,
                reply_markup=await get_donor_info_keyboard(field, donor, valid, donor_num, role)
            )

        elif 'picture' in select:
            # return
            pic = await field.picture()
            await bot.send_photo(
                user.telegram_id,
                photo=InputFile(io.BytesIO(pic)),
                reply_markup=await get_delete_keyboard()
            )

        elif 'field_valid_' in select:
            donor_num = select.split('_')[2]
            donor = await getattr(field, f'donor{donor_num}')
            if not donor:
                return

            if 'mentor' in role or 'master' in role:
                try:
                    setattr(field, f'donor_{donor_num}_{role}', True)
                    setattr(field, f'donor{donor_num}_time', None)
                    await field.save()
                    await bot.send_message(
                        donor.telegram_id,
                        (await get_message('you_valid')).format(
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
                            role=(await get_button(role[:-1])) if role != 'master' else await get_button(role)
                        ),
                        reply_markup=await get_player_keyboard(field, role)
                    )

                    if field.donor_valid(donor_num):
                        await field.save()
                        if field.type == 'start':
                            donor.active = True
                            await donor.save()
                            inviter = await donor.inviter
                            inviter.wood_key += 0.5
                            inviter.bronze_key += 0.5
                            inviter.silver_key += 0.5
                            inviter.gold_key += 0.5
                            inviter.platinum_key += 0.5
                            inviter.legendary_key += 0.5
                            await inviter.save()

                        if await field.is_full:
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
                                if (master.max_field != 'start' or (
                                        master.max_field == 'start' and master.active)) and \
                                        master.max_field == field.type:
                                    master.max_field = tables_order[tables_order.index(master.max_field) + 1]
                                    await master.save()

                            text = (await get_message('table_update')).format(
                                type=await get_button(f'{field.type}_name'),
                            )
                            for role, players in (await field.users(list_=True)).items():
                                for player in players:
                                    if player and role != 'master':
                                        await bot.send_message(
                                            player.telegram_id,
                                            text
                                        )

                            if field.type != 'start':
                                partner1 = await field.donor5
                                partner2 = await field.donor6
                                partner3 = await field.donor7
                                partner4 = await field.donor8

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
                                field.clear_donors()
                                await field.save()

                                new_field = await Table.create(
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
                                field.clear_donors()

                                await field.save()

                                new_field = await Table.create(
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
                    getattr(field, f'donor_{donor_num}_mentor2')):
                setattr(field, f'donor{donor_num}', None)
                setattr(field, f'donor_{donor_num}_mentor1', False)
                setattr(field, f'donor_{donor_num}_mentor2', False)
                setattr(field, f'donor_{donor_num}_master', False)
                setattr(field, f'donor{donor_num}_time', False)
                setattr(field, f'donor{donor_num}_notify', False)
                now = time.time()
                block_time = (await Config.get(id=1)).block_time * 3600
                setattr(donor, f'{field.type}_block', now + block_time)
                await field.save()
                await donor.save()
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
            num = select.split('_')[1][-1]
            gift = getattr(await TablePrice.get(id=1), field.type)
            gift_mentor = getattr(await TablePrice.get(id=1), f'{field.type}_mentor')

            if 'master' in select:
                player = users['master']
                role = 'Мастер'

            elif 'mentor' in select:
                player = users['mentors'][int(num) - 1]
                role = f'Ментор {num}'
                if field.type == 'start':
                    gift = 0
                else:
                    gift = gift_mentor

            elif 'partner' in select:
                player = users['partners'][int(num) - 1]
                role = f'Партнер {num}'
                gift = 0

            else:
                return

            text = (await get_message('team_list_row')).format(
                role=role,
                username=player.username,
                inviter=(await player.inviter).username,
                refs=len(await player.referrals),
                name=player.name,
                sum=gift
            )

            await callback.message.edit_caption(
                caption=text,
                reply_markup=await get_user_keyboard(field, player)
            )
        await callback.answer()

    elif 'confirm_exit' in select:
        await callback.answer()

        field = await Table.get_or_none(id=int(select.replace('confirm_exit_', '')))
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
            await callback.answer()
            return
        for game, role in (await user.games()).items():
            if game == field:
                if field.donor_valid(int(role[-1])):
                    await callback.message.delete()
                    return

                await callback.answer(await get_message('exit_notification'), show_alert=True)
                await get_captcha(callback, f'open_{field.type}', 'confirm_exit', field.id)
        await callback.answer()


    elif select == 'delete':
        await callback.answer()

        await callback.message.delete()
        admin = await user.admin
        if admin and admin.state == 'mail':
            admin.state = ''
            admin.photo = None
            admin.video = None
            admin.document = None
            await admin.save()


@dp.message_handler()
@dp.throttled(rate=FLOOD_RATE)
async def listen_handler(message: types.Message):
    message_ = message
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        await message.delete()

    elif not user.inviter:
        try:
            inviter = await TelegramUser.get_or_none(id=int(message.text.split('_')[-1])-13560)
        except:
            await message.delete()
            return
        if inviter is None:
            await message.answer(
                await get_message('incorrect_id')
            )
        else:
            if inviter.referral_url == message.text:
                user.inviter = inviter
                await user.save()
                await message.answer(
                    await get_message('agreement'),
                    reply_markup=await get_agreement_keyboard()
                )
            else:
                await message.answer(
                    await get_message('incorrect_id')
                )

    elif not user.agree or user.ban:
        await message.delete()
        return

    elif message.text == await get_button('open'):
        if not user.username:
            un = message.from_user.username
            if not un:
                await message.answer(
                    await get_message('add_usernaae')
                )
                return
            else:
                user.username = un
                await user.save()

        elif not user.name:
            user.name = message.from_user.full_name
            await user.save()

        await message.answer_photo(
            photo=open('photo/start.png', 'rb'),
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
                    status=await get_button(role[:-1] if role != 'master' else role),
                    count=await table.donor_count()
                )

        else:
            table_text = await get_message('no_tables')

        await message.answer(
            (await get_message('status')).format(
                id=user.telegram_id, name=user.username,
                inviter=(await user.inviter).username,
                count=len(await user.referrals.all()),
                tables=table_text,
                wood=round(user.wood_key - 0.1),
                bronze=round(user.bronze_key - 0.1),
                silver=round(user.silver_key - 0.1),
                gold=round(user.gold_key - 0.1),
                platinum=round(user.platinum_key - 0.1),
                legendary=round(user.legendary_key - 0.1),
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

    elif await user.admin:
        admin = await user.admin
        if admin.state == 'mail':
            users = await TelegramUser.all()
            photo = admin.photo
            user.state = ''
            await user.save()
            for user_ in users:
                try:
                    if photo:
                        await bot.send_photo(
                            user_.telegram_id,
                            photo=photo,
                            caption=message.text,
                            reply_markup=await get_delete_keyboard()
                        )
                    elif admin.document:
                        await bot.send_document(
                            user_.telegram_id,
                            document=admin.document,
                            caption=message.text,
                            reply_markup=await get_delete_keyboard()
                        )
                    elif admin.video:
                        await bot.send_video(
                            user_.telegram_id,
                            video=admin.video,
                            caption=message.text,
                            reply_markup=await get_delete_keyboard()
                        )
                    else:
                        await bot.send_message(
                            user_.telegram_id,
                            message.text,
                            reply_markup=await get_delete_keyboard()
                        )
                except BotBlocked:
                    pass
                except Exception as e:
                    print(traceback.format_exc())
            admin.state = ''
            admin.photo = None
            admin.video = None
            admin.document = None
            await admin.save()
            await message.answer(
                await get_message('mailed')
            )


@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        return

    elif not user.agree or user.ban:
        await message.delete()

        return

    admin = await user.admin

    photo = message.photo[-1]
    name = f'files/{message.from_user.id}_{photo.file_id}.jpg'
    await photo.download(destination_file=name)

    photo_binary = open(name, 'rb').read()
    os.remove(name)

    if 'mail' == admin.state:
        admin.photo = photo_binary
        await admin.save()
        return

    else:
        await message.delete()


@dp.message_handler(content_types=['document'])
async def handle_docs(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        return

    elif not user.agree or user.ban:
        await message.delete()

        return

    admin = await user.admin

    photo = message.document

    name = f'files/{message.from_user.id}_{photo.file_id}.jpg'
    await photo.download(destination_file=name)

    photo_binary = open(name, 'rb').read()
    os.remove(name)

    if 'mail' == admin.state:
        admin.document = photo_binary
        await admin.save()
        return

    else:
        await message.delete()


@dp.message_handler(content_types=['video'])
async def handle_video(message: types.Message):
    user = await TelegramUser.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        return

    elif not user.agree or user.ban:
        await message.delete()

        return

    admin = await user.admin

    photo = message.video

    name = f'files/{message.from_user.id}_{photo.file_id}.mp4'
    await photo.download(destination_file=name)

    photo_binary = open(name, 'rb').read()
    os.remove(name)

    if 'mail' == admin.state:
        admin.video = photo_binary
        await admin.save()
        return

    else:
        await message.delete()