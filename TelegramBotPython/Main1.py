import random
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token="6452953463:AAFsYV2w8r8-mt28ad8u4Sq9LJK0CeCiEOg")
dp = Dispatcher(bot)
user_message_count = {}  # Словарь для отслеживания количества сообщений пользователя

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Че как, я твой новый эхо бот!")
    user_message_count[message.from_user.id] = 0

@dp.message_handler()
async def echo(message: types.Message):
    user_id = message.from_user.id
    user_message_count[user_id] = user_message_count.get(user_id, 0) + 1

    if user_message_count[user_id] == 5:
        await message.answer("Хочешь сыграть в камень, ножницы, бумагу? Введи свой выбор (камень/ножницы/бумага).")
    elif user_message_count[user_id] > 5:
        if message.text.lower() in ['камень', 'ножницы', 'бумага']:
            await message.answer("Пошел нахуй")
            user_message_count[user_id] = 0
        else:
            await message.answer("Хочешь сыграть в камень, ножницы, бумагу? Введи свой выбор (камень/ножницы/бумага).")
    else:
        await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)






