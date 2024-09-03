import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
import logging
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание объектов бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Определение состояний для машины состояний
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Инициализация базы данных
init_db()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

# Обработчик для имени
@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

# Обработчик для возраста
@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

# Обработчик для класса (grade)
@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    # Сохранение данных в базу данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)
    ''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer(f"Данные сохранены:\nИмя: {user_data['name']}\nВозраст: {user_data['age']}\nКласс: {user_data['grade']}")

    await state.clear()

# Основная функция для запуска бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
