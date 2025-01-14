from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime
from bot.utils.db import log_run, get_user_profile, add_achievement
from aiogram.filters import Command

router = Router()


achievements_conditions = {
    "Первый шаг": lambda distance, duration, total_runs, total_distance: total_runs == 1,
    "Марафонец": lambda distance, duration, total_runs, total_distance: total_distance >= 42.2,
    "Часовой бегун": lambda distance, duration, total_runs, total_distance: duration > 3600,
    "Спортивная десятка": lambda distance, duration, total_runs, total_distance: distance >= 10,
    "Первая пятёрка": lambda distance, duration, total_runs, total_distance: total_runs == 5,
    "Первый десяток": lambda distance, duration, total_runs, total_distance: total_runs == 10,
    "Рекордсмен ленивых": lambda distance, duration, total_runs, total_distance: distance < 1,
}
# Состояния для FSM
class LogRunStates(StatesGroup):
    waiting_for_distance = State()
    waiting_for_duration = State()

# Начало процесса добавления тренировки
@router.message(Command("add_run"))
async def log_run_command(message: Message, state: FSMContext):
    await message.answer("Введите дистанцию (в километрах):")
    await state.set_state(LogRunStates.waiting_for_distance)

# Получаем дистанцию
@router.message(LogRunStates.waiting_for_distance)
async def process_distance(message: Message, state: FSMContext):
    try:
        distance = float(message.text)
        if distance <= 0:
            raise ValueError
        await state.update_data(distance=distance)
        await message.answer("Введите длительность тренировки (в формате ЧЧ:ММ:СС):")
        await state.set_state(LogRunStates.waiting_for_duration)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число больше нуля.")

# Получаем длительность
@router.message(LogRunStates.waiting_for_duration)
async def process_duration(message: Message, state: FSMContext):
    duration = message.text
    if not validate_duration(duration):
        await message.answer("Пожалуйста, введите длительность в формате ЧЧ:ММ:СС.")
        return

    data = await state.get_data()
    user_id = message.from_user.id
    distance = data["distance"]

    # Получаем текущую дату и время
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Сохраняем тренировку в БД
    log_run(user_id=user_id, distance=distance, duration=duration, date=current_date)
    user_profile = get_user_profile(user_id)
    total_runs = user_profile["total_runs"]
    total_distance = user_profile["total_distance"]
    await message.answer(f"Тренировка успешно добавлена!\n\nДата: {current_date}")
    unlocked_achievements = []
    for achievement, condition in achievements_conditions.items():
        if condition(distance, duration_in_seconds(duration), total_runs, total_distance):
            unlocked_achievements.append(achievement)
            add_achievement(user_id, achievement)
    if unlocked_achievements:
        await message.answer(
            f"Поздравляем! Вы получили следующие достижения:\n{', '.join(unlocked_achievements)}")
    await state.clear()

# Валидация длительности
def validate_duration(duration: str) -> bool:
    """Проверяет формат длительности (ЧЧ:ММ:СС)."""
    import re
    return bool(re.match(r"^\d{2}:\d{2}:\d{2}$", duration))

def duration_in_seconds(duration):
    hours, minutes, seconds = map(int, duration.split(":"))
    return hours * 3600 + minutes * 60 + seconds