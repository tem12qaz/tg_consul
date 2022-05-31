from aiogram import executor, types

from loader import dp
from parser import main_callback, Parser


def on_startup(_):
    parser = Parser()
    parser.start_parse()


@dp.callback_query_handler(main_callback.filter())
async def main_menu(callback: types.CallbackQuery, callback_data):
    account_id = callback_data.get('account_id')
    user_id = callback_data.get('user_id')
    city_id = callback_data.get('city_id')
    date = callback_data.get('date')
    time = callback_data.get('time')

    result = Parser.driver_do(account_id, user_id, city_id, date, time)
    if not result:
        await callback.answer(
            'Date not available for recording or error',
            show_alert=True
        )
    else:

        await callback.answer(
            'Success',
            show_alert=True
        )
        await callback.message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
