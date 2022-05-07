import random

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from tortoise import Model

from data.buttons import *
from data.config import tables_order, TELEGRAM_URL
from db.models import TelegramUser, Table, get_button, Config, TablePrice

select_callback = CallbackData("main", 'select')


async def get_main_keyboard():
    main_keyboard = ReplyKeyboardMarkup(
        [
            [KeyboardButton(await get_button('open')), KeyboardButton(await get_button('about'))],
            [KeyboardButton(await get_button('pdf')), KeyboardButton(await get_button('status'))],
            [KeyboardButton(await get_button('reff')), KeyboardButton(await get_button('support'))]
        ],
        resize_keyboard=True
    )
    return main_keyboard


async def get_support_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await get_button('support'), url=(await Config.get_or_none(id=1)).support_url)
            ]
        ]
    )
    return keyboard


async def get_captcha_keyboard(result, to, back, field_id=''):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=str(random.randint(20, 100)), callback_data=select_callback.new(
                select=f'captcha.{to}.{back}.{field_id}'
            )),
        ],
        [
            InlineKeyboardButton(text=str(random.randint(20, 100)), callback_data=select_callback.new(
                select=f'captcha.{to}.{back}.{field_id}'
            )),
        ]
    ]
    true_button = InlineKeyboardButton(text=str(result), callback_data=select_callback.new(
            select=f'{to}_{field_id}'
    ))
    false_button = InlineKeyboardButton(text=str(random.randint(20, 100)), callback_data=select_callback.new(
            select=f'captcha.{to}.{back}.{field_id}'
    ))

    row = random.randint(0, 1)
    col = random.randint(0, 1)

    inline_keyboard[row - 1].insert(0, false_button)

    if not col:
        inline_keyboard[row].insert(0, true_button)
    else:
        inline_keyboard[row].append(true_button)

    inline_keyboard.append(
        [
            InlineKeyboardButton(await get_button('cancel'), callback_data=select_callback.new(
                select=back
            )),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_status_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await get_button('channel'), url=(await Config.get_or_none(id=1)).channel),
                InlineKeyboardButton(text=await get_button('chat'), url=(await Config.get_or_none(id=1)).chat)
            ]
        ]
    )
    return keyboard


async def get_user_keyboard(field, user):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await get_button('send_message'),
                                    url=TELEGRAM_URL.format(username=user.username)),
            ],
            [
                InlineKeyboardButton(text=await get_button('back'),
                                     callback_data=select_callback.new(select=f'open_{field.type}')),
            ],
        ]
    )
    return keyboard


async def get_back_to_info_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await get_button('back'),
                                     callback_data=select_callback.new(select=f'info')),
            ],
        ]
    )
    return keyboard


async def get_player_keyboard(field: Table, role):
    me = await get_button('me_emoji')
    inline_keyboard = [
        [
            InlineKeyboardButton(text=await get_button('master') + (me if role == 'master' else ''),
                                 callback_data=select_callback.new(select=f'field_master_{field.id}')),
        ],
        [
            InlineKeyboardButton(text=await get_button('mentor1' + (me if role == 'mentor1' else '')),
                                 callback_data=select_callback.new(select=f'field_mentor1_{field.id}')),

            InlineKeyboardButton(text=await get_button('mentor2' + (me if role == 'mentor2' else '')),
                                 callback_data=select_callback.new(select=f'field_mentor2_{field.id}')),

        ]
    ]
    if field.type != 'start':
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=await get_button('partner1' + (me if role == 'partner1' else '')),
                                     callback_data=select_callback.new(select=f'field_partner1_{field.id}')),

                InlineKeyboardButton(text=await get_button('partner2' + (me if role == 'partner2' else '')),
                                     callback_data=select_callback.new(select=f'field_partner2_{field.id}')),

            ],
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=await get_button('partner3' + (me if role == 'partner3' else '')),
                                     callback_data=select_callback.new(select=f'field_mentor3_{field.id}')),

                InlineKeyboardButton(text=await get_button('partner4' + (me if role == 'partner4' else '')),
                                     callback_data=select_callback.new(select=f'field_partner4_{field.id}')),

            ],
        )
    inline_keyboard.append(
        [
            InlineKeyboardButton(text=await get_button('team_list'),
                                 callback_data=select_callback.new(select=f'field_team_list_{field.id}')),

        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(text=await get_button('see_donors'),
                                 callback_data=select_callback.new(select=f'field_donors_{field.id}')),

        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(text=await get_button('back_to_tables'),
                                 callback_data=select_callback.new(select=f'open')),

        ],
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def donors_keyboard(field: Table, role):
    inline_keyboard = []

    def valid(i):
        if getattr(field, f'donor_{i}_{role}'):
            return '✅'
        else:
            return '❌'

    async def donor_text(i):
        donor = await getattr(field, f'donor{i}')
        if donor:
            return donor.username + valid(i)
        else:
            return (await get_button(f'donor')) + str(i)

    max_donor = 4 if field.type == 'start' else 8

    for i in range(1, max_donor, 2):
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=await donor_text(i),
                                     callback_data=select_callback.new(select=f'field_donor_{i}_{field.id}')),
                InlineKeyboardButton(text=await donor_text(i),
                                     callback_data=select_callback.new(select=f'field_donor_{i}_{field.id}')),
            ],
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(text=await get_button('donor_list'),
                                 callback_data=select_callback.new(select=f'field_donor_list_{field.id}')),

        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(text=await get_button('back'),
                                 callback_data=select_callback.new(select=f'open_{field.id}')),

        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def get_donor_info_keyboard(field, donor, valid, donor_num, role):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=await get_button('send_message'),
                                 url=TELEGRAM_URL.format(username=donor.username)),
        ],
        [
            InlineKeyboardButton(text=await get_button('back'),
                                 callback_data=select_callback.new(select=f'open_{field.type}')),
        ]
    ]
    if not valid:
        if role == 'master' and not (
                getattr(field, f'donor_{donor_num}_mentor1') or
                getattr(field, f'donor_{donor_num}_mentor1')):
            inline_keyboard.insert(
                0,
                [
                    InlineKeyboardButton(text=await get_button('delete_donor'),
                                         callback_data=select_callback.new(
                                             select=f'captcha.field_delete_{donor_num}.open_{field.type}.{field.id}')
                                         ),
                ]
            )
        inline_keyboard.insert(
            0,
            [
                InlineKeyboardButton(text=await get_button('valid_donor'),
                                     callback_data=select_callback.new(
                                         select=f'captcha.field_valid_{donor_num}.open_{field.type}.{field.id}')
                                     ),
            ]
        )


async def get_about_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await get_button('tables_info'),
                                     callback_data=select_callback.new(select='tables_info')),
            ],
            [
                InlineKeyboardButton(text=await get_button('donor'),
                                     callback_data=select_callback.new(select='donor_info')),
                InlineKeyboardButton(text=await get_button('partner'),
                                     callback_data=select_callback.new(select='partner_info')),

            ],
            [
                InlineKeyboardButton(text=await get_button('mentor'),
                                     callback_data=select_callback.new(select='mentor_info')),
                InlineKeyboardButton(text=await get_button('master'),
                                     callback_data=select_callback.new(select='master_info')),

            ],
        ]
    )
    return keyboard


async def back_on_table(field: Table):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await get_button('back'),
                                     callback_data=select_callback.new(select=f'open_{field.type}')),
            ],
        ]
    )
    return keyboard


async def get_donor_keyboard(field: Table, role):
    inline_keyboard = [
        [
            InlineKeyboardButton(text=await get_button('make_a_gift'),
                                 callback_data=select_callback.new(select=f'make_gift_{field.id}')),
        ]
    ]
    if not field.donor_valid(int(role[-1])):
        inline_keyboard.append(
            [InlineKeyboardButton(text=await get_button('exit'),
                                  callback_data=select_callback.new(select=f'exit_{field.id}'))]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(text=await get_button('back_to_tables'),
                                 callback_data=select_callback.new(select=f'open')),

        ],
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    return keyboard


async def get_donor_gift_keyboard(field: Table, price):
    master_un = (await field.master).username
    inline_keyboard = [
        [
            InlineKeyboardButton(text=(await get_button('gift_master')).format(
                user=master_un, sum=price
            ), url=TELEGRAM_URL.format(username=master_un))
        ]
    ]
    if not field.type != 'start':
        mentor1_un = (await field.mentor1).username
        mentor2_un = (await field.mentor2).username

        inline_keyboard += [
            [
                InlineKeyboardButton(text=(await get_button('gift_mentor')).format(
                    user=mentor1_un, sum=price//2
                ), url=TELEGRAM_URL.format(username=mentor1_un))
            ],
            [
                InlineKeyboardButton(text=(await get_button('gift_mentor')).format(
                    user=mentor2_un, sum=price//2
                ), url=TELEGRAM_URL.format(username=mentor2_un))
            ]
        ]

    inline_keyboard.append(
        [
            InlineKeyboardButton(text=await get_button('notify_users'),
                                 callback_data=select_callback.new(select=f'notify_users_{field.id}')),

        ]
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard
    )
    return keyboard


async def get_tables(user: TelegramUser):
    buttons = []
    shift = 0
    if user.max_field != 'start':
        shift = 1
    for table in tables_order[shift:]:
        buttons.append(
            [
                InlineKeyboardButton(text=await get_button(f'{table}_name'),
                                     callback_data=select_callback.new(select=f'open_{table}')),
            ]
        )
        if table == user.max_field:
            break
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def open_field():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=await get_button('table_info'),
                                     callback_data=select_callback.new(select='table_info')),
            ],
            [
                InlineKeyboardButton(text=await get_button('donor'),
                                     callback_data=select_callback.new(select='donor_info')),
                InlineKeyboardButton(text=await get_button('partner'),
                                     callback_data=select_callback.new(select='partner_info')),

            ],
            [
                InlineKeyboardButton(text=await get_button('mentor'),
                                     callback_data=select_callback.new(select='mentor_info')),
                InlineKeyboardButton(text=await get_button('master'),
                                     callback_data=select_callback.new(select='master_info')),

            ],
        ]
    )
    return keyboard
