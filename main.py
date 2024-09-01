import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ["https://i.imgur.com/pwpWaWu.jpg", "https://i.imgur.com/5GtBn6P.jpg", "https://i.imgur.com/5GtBn6P.jpg"]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Красивое фото","emoji", "Спасибо", "Хорошее фото"]
    await message.answer(random.choice(list))




@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("Продолжаем работу с ботом и улучшением его функционала.")



@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help"  "\n /photo")


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

