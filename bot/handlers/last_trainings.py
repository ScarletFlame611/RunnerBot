import sqlite3
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.utils.db import get_last_trainings

router = Router()


# Обработчик для команды /trainings
@router.message(Command("last_trainings"))
async def trainings_command(message: Message):
    user_id = message.from_user.id
    # Получаем последние 5 тренировок (или меньше)
    last_trainings = get_last_trainings(user_id)
    if not last_trainings:
        await message.answer("У вас нет тренировок.")
        return
    text = "📝 Ваши последние тренировки:\n\n"
    for i, training in enumerate(last_trainings, 1):
        distance, duration, date = training
        text += f"{i}. Дистанция: {distance} км, Время: {duration}, Дата: {date}\n"
    # Отправляем текст с тренировками
    await message.answer(text)
