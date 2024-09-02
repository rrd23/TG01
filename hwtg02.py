import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import random
from googletrans import Translator
from gtts import gTTS

bot = Bot(token=TOKEN)

dp = Dispatcher()

@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ["Красивое фото", "😊", "Спасибо", "Хорошее фото"]
    await message.answer(random.choice(responses))
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('voice.ogg')
    await bot.send_voice(message.chat.id, voice)
    #await message.answer_voice(voice)

translator = Translator()
@dp.message()
async def translate_text(message: Message):
    # Переводим текст пользователя на английский язык
    translation = translator.translate(message.text, dest='en')

    # Отправляем переведенный текст пользователю
    await message.answer(translation.text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())