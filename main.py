import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types,F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN, WEATHER_API_KEY
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

# Функция для получения прогноза погоды
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        city_name = data['name']
        country = data['sys']['country']
        return f"Погода в {city_name}, {country}:\nТемпература: {temperature}°C\nОписание: {weather_description}"
    else:
        return "Не удалось получить данные о погоде. Проверьте название города."

# Обработчик команды /weather
@dp.message(Command('weather'))
async def weather(message: Message):
    city = "Moscow"  # Вы можете заменить этот город на любой другой
    weather_info = get_weather(city)
    await message.answer(weather_info)



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
