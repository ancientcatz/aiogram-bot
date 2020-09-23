"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from otp_auth import (otpCode, otpVerify)

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


# Master
master = [
    '822518127',
]


# States
class Aiocatz(StatesGroup):
    auth = State()
    passed = State()
# end class

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm Aiocatz!\nPowered by aiogram.")
# end def



@dp.message_handler(commands=['otp'])
async def get_otp(message: types.Message):
    otp = otpCode()
    if str(message.chat.id) not in master :
        await message.answer('Sorry you\'re not my master, you\'re not allowed to use this command')
    else:
        await message.reply(
            '%s' % otp
        )
    # end if
# end def



@dp.message_handler(commands=['give'])
async def give(message: types.Message):
    id = message.get_args()
    otp = otpCode()
    if str(message.chat.id) not in master :
        await message.answer('Sorry you\'re not my master, you\'re not allowed to use this command')
    else:
        await bot.send_message(
            id, '%s' % otp
        )
    # end if
# end def



@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    # end if

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled. Send /new to start a new session', reply_markup=types.ReplyKeyboardRemove())
# end def



@dp.message_handler(Command('new'))
async def greet(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    if str(message.chat.id) not in master :
        await Aiocatz.auth.set()

        await message.answer('Sorry you\'re not my master, send your ID:`{message.chat.id}` to my master to use our services. @AncientCatz')
        await message.answer(
            'Enter your OTP Code'
            'To cancel send /cancel'
        )
    else:
        await Aiocatz.passed.set()

        await message.answer('Welcome dear master')
    # end if
# end def

@dp.message_handler(lambda message: not message.text.isdigit(), state=Aiocatz.auth)
async def otp_verify_invalid(message: types.Message):
    await message.reply(
        'OTP Code gotta be a number (digits only).\n'
        'To cancel send /cancel.'
    )
# end def

@dp.message_handler(lambda message: message.text.isdigit(), state=Aiocatz.auth)
async def otp_verify(message: types.Message, state = FSMContext):
    otp = message.text
    if otpVerify(otp) == False:
        await message.reply(
            'Invalid OTP Code'
            'To cancel send /cancel'
        )
    elif otpVerify(otp) == True:
        await Aiocatz.next()

        await message.answer('Authenticated, you can use our service for one session')
    # end if
# end def

@dp.message_handler(state=Aiocatz.passed)
async def passed(message: types.Message, state = FSMContext):
    await state.finish()
    await message.answer('Coming soon!')
# end def


if __name__ == '__main__':
    print("Telegram bot online!")
    executor.start_polling(dp, skip_updates=True)