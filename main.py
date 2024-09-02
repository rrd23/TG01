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

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

    # tts = gTTS(text=rand_tr, lang='ru')
    # tts.save('training.mp3')
    # audio = FSInputFile('training.mp3')
    # await bot.send_audio(message.chat.id, audio)
    # os.remove("training.mp3")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile("training.ogg")
    await bot.send_voice(chat_id=message.chat.id, voice=audio)
    os.remove("training.ogg")






@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('40627.mp3')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id,video)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('voice.ogg')
    await bot.send_voice(message.chat.id, voice)
    #await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(message.chat.id, doc)



# Указываем путь к папке, где хранятся изображения
# os.path.join() объединяет директории и текущий файл, чтобы сформировать абсолютный путь
# os.path.dirname(__file__) возвращает директорию, в которой находится текущий файл
IMAGE_DIR = os.path.join(os.path.dirname(__file__), '')

# Обработчик команды /photo
# Когда пользователь отправляет команду /photo, эта функция выбирает случайное изображение из заданной папки и отправляет его пользователю
@dp.message(Command('photo',prefix='!'))
async def photo(message: Message):
    # Определяем допустимые форматы изображений
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif')

    # Получаем список всех файлов в директории, которые соответствуют поддерживаемым форматам
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(supported_formats)]

    # Если в папке нет изображений, отправляем сообщение пользователю
    if not images:
        await message.answer("Нет доступных изображений в папке.")
        return

    # Выбираем случайное изображение из доступных
    random_image = random.choice(images)
    image_path = os.path.join(IMAGE_DIR, random_image)

    # Используем FSInputFile для создания объекта, представляющего файл изображения
    photo = FSInputFile(image_path)

    # Отправляем выбранное изображение пользователю с подписью
    await message.answer_photo(photo=photo, caption="Вот ваше случайное изображение")

# Закомментированный код показывает предыдущий подход, где фотографии отправлялись по URL.
# Это было заменено на отправку локальных изображений.

# Функция для получения прогноза погоды
# Эта функция делает запрос к OpenWeatherMap API, получает данные о погоде и возвращает их в удобном формате
def get_weather(city):
    # Формируем URL запроса к API с указанием города, ключа API и единиц измерения
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    # Выполняем HTTP GET запрос с заданным URL
    response = requests.get(url, timeout=10)

    # Преобразуем ответ в формат JSON
    data = response.json()

    # Если запрос был успешным (код 200), извлекаем и форматируем данные о погоде
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        city_name = data['name']
        country = data['sys']['country']
        return f"Погода в {city_name}, {country}:\nТемпература: {temperature}°C\nОписание: {weather_description}"
    else:
        # В случае ошибки возвращаем сообщение о неудаче
        return "Не удалось получить данные о погоде. Проверьте название города."

# Обработчик команды /weather
# При получении команды /weather бот отправляет пользователю прогноз погоды для заданного города
@dp.message(Command('weather'))
async def weather(message: Message):
    city = "Moscow"  # Вы можете заменить этот город на любой другой
    weather_info = get_weather(city)
    await message.answer(weather_info)

# Обработчик для реакции на полученные фотографии
# Когда пользователь отправляет фото, бот случайным образом выбирает и отправляет ответное сообщение
@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ["Красивое фото", "😊", "Спасибо", "Хорошее фото"]
    await message.answer(random.choice(responses))
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

# Обработчик команды /help
# Отправляет пользователю список доступных команд и их описание
@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n /weather")

# Обработчик команды /start
# Отправляет приветственное сообщение пользователю, который начал взаимодействие с ботом
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")

#
# @dp.message()
# async def start(message: Message):
#     await message.answer(f"Я тебе ответил, {message.from_user.full_name}!")
#
@dp.message()
async def start(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')

# @dp.message()
# async def echo(message: Message):
#     await message.send_copy(chat_id=message.chat.id)


#
# @dp.message(Command('video'))
# async def video(message: Message):
#     await bot.send_chat_action(message.chat.id, 'upload_video')
#     video = FSInputFile('video.mp4')
#     await bot.send_video(message.chat.id,video)

#
# @dp.message(Command('audio'))
# async def audio(message: Message):
#     await bot.send_chat_action(message.chat.id, 'upload_audio')
#     audio = FSInputFile('40627.mp3')
#     await bot.send_audio(message.chat.id, audio)


# Главная асинхронная функция, которая запускает процесс опроса (polling) от Telegram.
# Polling - это метод, при котором бот постоянно проверяет наличие новых сообщений от пользователей
async def main():
    await dp.start_polling(bot)

# Если этот файл запускается как основной (а не импортируется), вызывается функция main()
if __name__ == "__main__":
    asyncio.run(main())
