import os
import asyncio
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Указываем путь к папке, где хранятся изображения
IMAGE_DIR = os.path.join(os.path.dirname(__file__), '')

# Обработчик команды /photo
@dp.message(Command('photo'))
async def photo(message: Message):
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif')
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(supported_formats)]

    if not images:
        await message.answer("Нет доступных изображений в папке.")
        return

    random_image = random.choice(images)
    image_path = os.path.join(IMAGE_DIR, random_image)

    # Используем FSInputFile для открытия файла
    photo = FSInputFile(image_path)
    await message.answer_photo(photo=photo, caption="Вот ваше случайное изображение")

#
# @dp.message(Command('photo'))
# async def photo(message: Message):
#     list = ["https://i.imgur.com/pwpWaWu.jpg", "https://i.imgur.com/5GtBn6P.jpg", "https://i.imgur.com/5GtBn6P.jpg"]
#     rand_photo = random.choice(list)
#     await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')


@dp.message(F.photo)
async def react_photo(message: Message):
    list = ["Красивое фото","emoji", "Спасибо", "Хорошее фото"]
    await message.answer(random.choice(list))


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /photo")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
