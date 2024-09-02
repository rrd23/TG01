import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
import random
from gtts import gTTS
# Создаем объект бота с использованием токена, который был задан в файле config.py
bot = Bot(token=TOKEN)
# Создаем объект диспетчера для обработки входящих сообщений и команд
dp = Dispatcher()


@dp.message(Command('send_text'))
async def send_text(message: Message):
    # Имя файла
    file_name = "example.txt"

    # Чтение содержимого файла
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()

    # Отправка содержимого файла как текстового сообщения
    await message.answer(content)


async def main():
    await dp.start_polling(bot)

# Если этот файл запускается как основной (а не импортируется), вызывается функция main()
if __name__ == "__main__":
    asyncio.run(main())
