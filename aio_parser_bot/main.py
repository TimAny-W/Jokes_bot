import random

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from parser_jokes import run_tasks

bot = Bot(token='5911754199:AAELK4_2iCB-aXPJ1mqkuqIEJBYwmO7FmvE')
dp = Dispatcher(bot)

list_of_jokes = list()


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    global list_of_jokes
    await message.answer('IM BOT WHO CAN HELP U FIND JOKES', reply_markup=user_kb)
    list_of_jokes = await run_tasks()
    print(list_of_jokes)


@dp.callback_query_handler(text='joke_button')
async def joke_button(callback_query: types.CallbackQuery):
    global list_of_jokes
    print(list_of_jokes, 'button')
    if len(list_of_jokes) == 0:
        await bot.send_message(callback_query.from_user.id, 'Обновите базу данных анекдотов', reply_markup=update_base_kb)
    else:
        mess = random.choice(list_of_jokes)
        await bot.send_message(callback_query.from_user.id,
                               f'<b>{mess}</b>',
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=user_kb)
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(text='joke_update')
async def joke_button(callback_query: types.CallbackQuery):
    global list_of_jokes
    list_of_jokes = await run_tasks()
    await bot.answer_callback_query(callback_query.id)
    if len(list_of_jokes) != 0:
        await bot.send_message(callback_query.from_user.id, 'База данных успешно обновлена!',reply_markup=user_kb)
    else:
        await bot.send_message(callback_query.from_user.id, 'Произошла ошибка!')


""""-----------BUTTONS-----------"""
user_kb = InlineKeyboardMarkup(resize_keyboard=True) \
    .add(InlineKeyboardButton('Получить анекдот', callback_data='joke_button'))
update_base_kb = InlineKeyboardMarkup(resize_keyboard=True) \
    .add(InlineKeyboardButton('Обновить базу данных', callback_data='joke_update'))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
