from aiogram import executor, types

from admin.parser import main_callback, Parser
from handlers import dp


@dp.callback_query_handler(main_callback.filter())
async def main_menu(callback: types.CallbackQuery, callback_data):
    account_id = callback_data.get('account_id')
    user_id = callback_data.get('user_id')
    city_id = callback_data.get('city_id')
    date = callback_data.get('date')
    time = callback_data.get('time')

    result = Parser.driver_do(account_id, user_id, city_id, date, time)
    if not result:
        await callback.message.edit_text(
            'Date not available for recording or error'
        )
    else:
        await callback.message.edit_text(
            'Success'
        )


if __name__ == '__main__':
    executor.start_polling(dp)
