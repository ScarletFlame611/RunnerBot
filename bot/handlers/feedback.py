import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.utils.db import save_feedback

logger = logging.getLogger(__name__)
router = Router()

# Определяем состояния
class FeedbackForm(StatesGroup):
    rating = State()  # Состояние для оценки
    review = State()  # Состояние для отзыва

# Команда для начала заполнения анкеты
@router.message(Command("feedback"))
async def start_feedback(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, оцените наш бот от 1 до 5:")
    await state.set_state(FeedbackForm.rating)

# Обработка оценки
@router.message(FeedbackForm.rating, F.text.isdigit() & F.text.in_({"1", "2", "3", "4", "5"}))
async def process_rating(message: Message, state: FSMContext):
    await state.update_data(rating=int(message.text))  # Сохраняем оценку
    await message.answer("Спасибо! Теперь оставьте ваш отзыв или напишите 'Пропустить':")
    await state.set_state(FeedbackForm.review)

# Обработка отзыва
@router.message(FeedbackForm.review)
async def process_review(message: Message, state: FSMContext):
    # Получаем данные от пользователя
    review = message.text if message.text.lower() != "пропустить" else None
    data = await state.get_data()  # Достаем данные из FSM
    rating = data["rating"]

    try:
        # Сохраняем в базу данных
        save_feedback(user_id=message.from_user.id, rating=rating, review=review)
        await message.answer("Спасибо за ваш отзыв! Мы ценим ваше мнение 😊")
    except Exception as e:
        await message.answer("Произошла ошибка при сохранении отзыва. Попробуйте позже.")
        print(f"Ошибка сохранения отзыва: {e}")
        logger.error(f"Ошибка сохранения отзыва: {e}")
    finally:
        await state.clear()  # Завершаем FSM

# Если введены некорректные данные
@router.message(FeedbackForm.rating)
async def invalid_rating(message: Message):
    await message.answer("Введите число от 1 до 5.")
