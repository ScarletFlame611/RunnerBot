from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.utils.db import get_user_achievements
router = Router()

# Список достижений
ACHIEVEMENTS = [
    "🏅 *Первый шаг*: Завершить первую пробежку.",
    "🏅 *Марафонец*: Пробежать суммарно 42.2 км.",
    "🏅 *Часовой бегун*: Завершить тренировку длительностью более 1 часа.",
    "🏅 *Спортивная десятка*: Пробежать 10 км за одну тренировку.",
    "🏅 *Первая пятёрка*: Завершить 5 тренировок.",
    "🏅 *Первый десяток*: Завершить 10 тренировок.",
    "🏅 *Рекордсмен ленивых*: Завершить пробежку длиной меньше 1 км.",
]

@router.message(Command("achievements_info"))
async def achievements_info_command(message: Message):
    achievements_text = "🎖 *Достижения*\n\n" + "\n".join(ACHIEVEMENTS)
    await message.answer(achievements_text, parse_mode="Markdown")


@router.message(Command("my_achievements"))
async def my_achievements(message: Message):
    """Выводит все достижения пользователя с эмодзи и датой получения."""
    user_id = message.from_user.id

    # Получаем достижения пользователя
    achievements = get_user_achievements(user_id)

    if achievements:
        # Список эмодзи для достижения
        achievement_emojis = {
            "Первый шаг": "👟",
            "Марафонец": "🏃‍♂️",
            "Часовой бегун": "⏱️",
            "Спортивная десятка": "🔟",
            "Первая пятёрка": "5️⃣",
            "Первый десяток": "🔟",
            "Три в одном": "3️⃣",
            "Рекордсмен ленивых": "🐢",
        }

        # Формируем красивое сообщение
        achievements_text = "\n".join([
            f"{achievement_emojis.get(achievement[0], '🏅')} {achievement[0]} - {achievement[1]}"
            for achievement in achievements
        ])
        await message.answer(f"🎉 Ваши достижения:\n\n{achievements_text}")
    else:
        await message.answer("🚫 У вас еще нет достижений.")

