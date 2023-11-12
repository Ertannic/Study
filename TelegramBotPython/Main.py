import logging

from aiogram import Bot, Dispatcher, executor, types

bot = Bot (token="6452953463:AAFsYV2w8r8-mt28ad8u4Sq9LJK0CeCiEOg")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Че как, я твой новый эко бот!.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)