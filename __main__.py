"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")



async def email(message: types.Message):
    await message.reply("Your e-mail: %s" % message.text)

@dp.message_handler(Command('greet'))
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer("Enter your e-mail")
    await email()


if __name__ == '__main__':
    print("Telegram bot online!")
    executor.start_polling(dp, skip_updates=True)