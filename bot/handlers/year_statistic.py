from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime, timedelta

from bot.utils.db import get_trainings_last_year

# Создаем роутер для статистики по тренировкам
router = Router()


# Функция для группировки тренировок по месяцам
def group_trainings_by_month(trainings):
    stats = {}

    for distance, duration, date in trainings:

        # Извлекаем месяц и год из даты
        try:
            month = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m")
        except Exception as e:
            print(f"Error parsing date '{date}': {e}")
            continue

        # Конвертируем время в секунды
        try:
            hours, minutes, seconds = map(int, duration.split(":"))
            total_seconds = hours * 3600 + minutes * 60 + seconds
        except Exception as e:
            print(f"Error converting duration '{duration}': {e}")
            continue

        # Инициализируем статистику для месяца, если ее еще нет
        if month not in stats:
            stats[month] = {
                "count": 0,
                "total_distance": 0.0,
                "total_duration": 0  # Храним в секундах
            }

        stats[month]["count"] += 1
        stats[month]["total_distance"] += distance
        stats[month]["total_duration"] += total_seconds

    return stats


# Обработчик для команды /year_statistics
@router.message(Command("year_stats"))
async def year_statistics_command(message: Message):
    user_id = message.from_user.id
    # Получаем тренировки за последний год
    trainings = get_trainings_last_year(user_id)

    if not trainings:
        await message.answer("У вас нет тренировок за последний год.")
        return

    # Группируем тренировки по месяцам
    monthly_stats = group_trainings_by_month(trainings)

    # Формируем текст для отчета
    text = "📊 Статистика по тренировкам за последний год:\n\n"
    total_runs = 0
    total_distance = 0.0
    total_duration = 0

    for month, stats in sorted(monthly_stats.items()):
        text += f"📅 {month}:\n"
        text += f"   - Количество тренировок: {stats['count']}\n"
        text += f"   - Суммарная дистанция: {stats['total_distance']:.2f} км\n"

        # Преобразуем время из секунд в формат "часы:минуты:секунды" для вывода
        total_seconds = stats["total_duration"]
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_duration = f"{hours}ч {minutes}м {seconds}с"

        text += f"   - Суммарное время: {formatted_duration}\n\n"

        total_runs += stats["count"]
        total_distance += stats["total_distance"]
        total_duration += stats["total_duration"]

    # Добавляем итоговые данные за год
    text += f"📅 Общее за год:\n"
    text += f"   - Количество тренировок: {total_runs}\n"
    text += f"   - Суммарная дистанция: {total_distance:.2f} км\n"

    # Преобразуем общее время в секундах в формат "часы:минуты:секунды" для итогового вывода
    total_hours, remainder = divmod(total_duration, 3600)
    total_minutes, total_seconds = divmod(remainder, 60)
    total_duration_str = f"{total_hours}ч {total_minutes}м {total_seconds}с"

    text += f"   - Суммарное время: {total_duration_str}"

    # Отправляем отчет
    await message.answer(text)
