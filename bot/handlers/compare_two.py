from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.utils.db import get_last_two_trainings

router = Router()


def calculate_average_speed(distance, duration):
    # Преобразуем время в минуты
    hours, minutes, seconds = map(int, duration.split(":"))
    total_minutes = hours * 60 + minutes + seconds / 60
    if total_minutes == 0:  # Если время равно нулю, скорость будет нулевой
        return 0
    return distance / total_minutes


# Обработчик для команды /compare_trainings
@router.message(Command("compare_two"))
async def compare_trainings_command(message: Message):
    user_id = message.from_user.id
    last_two_trainings = get_last_two_trainings(user_id)

    if len(last_two_trainings) < 2:
        await message.answer("У вас недостаточно тренировок для сравнения.")
        return

    # Извлекаем данные о тренировках
    training_1 = last_two_trainings[0]
    training_2 = last_two_trainings[1]
    distance_1, duration_1, date_1 = training_1
    distance_2, duration_2, date_2 = training_2

    # Вычисляем среднюю скорость для каждой тренировки
    speed_1 = calculate_average_speed(distance_1, duration_1)
    speed_2 = calculate_average_speed(distance_2, duration_2)

    comparison_text = (
        f"📊 Сравнение двух последних тренировок:\n\n"
        f"1️⃣ Тренировка от {date_1}:\n"
        f"   - Дистанция: {distance_1} км\n"
        f"   - Время: {duration_1}\n"
        f"   - Средняя скорость: {speed_1:.2f} км/мин\n\n"
        f"2️⃣ Тренировка от {date_2}:\n"
        f"   - Дистанция: {distance_2} км\n"
        f"   - Время: {duration_2}\n"
        f"   - Средняя скорость: {speed_2:.2f} км/мин\n\n"
    )

    # Сравнение дистанции, времени и скорости
    distance_comparison = "Больше" if distance_1 > distance_2 else (
        "Меньше" if distance_1 < distance_2 else "Равны")
    duration_comparison = "Больше" if duration_1 > duration_2 else (
        "Меньше" if duration_1 < duration_2 else "Равны")
    speed_comparison = "Больше" if speed_1 > speed_2 else (
        "Меньше" if speed_1 < speed_2 else "Равны")

    comparison_text += (
        f"📏 Сравнение:\n"
        f"   - Дистанция: Тренировка 1 {distance_comparison} Тренировки 2\n"
        f"   - Время: Тренировка 1 {duration_comparison} Тренировки 2\n"
        f"   - Средняя скорость: Тренировка 1 {speed_comparison} Тренировки 2\n"
    )

    await message.answer(comparison_text)
