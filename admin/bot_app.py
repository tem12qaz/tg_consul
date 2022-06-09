import asyncio

from aiogram import executor, types

from loader import dp
from parser import main_callback, Parser


@dp.callback_query_handler(main_callback.filter())
async def main_menu(callback: types.CallbackQuery, callback_data):
    print('----------')
    print(callback_data)
    account_id = callback_data.get('account_id')
    user_id = callback_data.get('user_id')
    city_id = callback_data.get('city_id')
    date = callback_data.get('date')
    time = callback_data.get('time').replace('.', ':')

    # if str(city_id) == '7':
    #     city_id = 95
    #
    # if str(city_id) == '6':
    #     city_id = 94
    #     date = '2023-08-18'
    #     time = '11:00'


    if parser.appointment:
        await callback.answer('Бот уже записывает один из аккаунтов.', show_alert=True)
        return
    else:
        await callback.answer('Загрузка...', show_alert=True)

    parser.appointment = True
    while parser.search:
        await asyncio.sleep(1)

    result = Parser.driver_do(account_id, user_id, city_id, date, time)
    parser.appointment = False
    if not result:
        await callback.message.answer(
            'Date not available for recording or error',
        )
    else:
        await callback.message.answer_photo(
            open('last.png', 'rb'),
        )

if __name__ == '__main__':
    parser = Parser()
    parser.start_parse()
    executor.start_polling(dp, loop=parser.loop)
