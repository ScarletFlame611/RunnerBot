import logging

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.utils.db import is_user_registered, register_user
from aiogram.filters import Command

router = Router()
logger = logging.getLogger(__name__)


def create_main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],
            [KeyboardButton(text="/help")],
            [KeyboardButton(text="/menu")]
        ],
        resize_keyboard=True
    )


class RegistrationForm(StatesGroup):
    full_name = State()
    age = State()
    height = State()
    weight = State()


@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} вызвал команду /start")
    # Проверяем, зарегистрирован ли пользователь
    if is_user_registered(user_id):
        logger.info(f"Пользователь {user_id} уже зарегистрирован")
        await message.answer("Вы уже зарегистрированы! Можете использовать команды бота.",
                             reply_markup=create_main_menu_keyboard())
        return

    # Если пользователь не зарегистрирован, запускаем регистрацию
    await message.answer("Добро пожаловать! Давайте начнём с регистрации.\nВведите ваше ФИО:")
    await state.set_state(RegistrationForm.full_name)


@router.message(RegistrationForm.full_name)
async def process_full_name(message: Message, state: FSMContext):
    # Проверяем, что введённое сообщение состоит из букв и содержит минимум 2 слова
    if not all(word.isalpha() for word in message.text.split()) or len(message.text.split()) < 2:
        await message.answer("Пожалуйста, введите корректное ФИО (только буквы, минимум 2 слова).")
        return

    # Сохраняем данные, если проверка пройдена
    await state.update_data(full_name=message.text)
    await message.answer("Введите ваш возраст:")
    await state.set_state(RegistrationForm.age)


@router.message(RegistrationForm.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректный возраст (только цифры).")
        return

    await state.update_data(age=int(message.text))
    await message.answer("Введите ваш рост (в см):")
    await state.set_state(RegistrationForm.height)


@router.message(RegistrationForm.height)
async def process_height(message: Message, state: FSMContext):
    if not message.text.isdigit() and not message.text.replace(".", "").isdigit():
        await message.answer(
            "Пожалуйста, введите корректный рост (только цифры или десятичное число).")
        return

    await state.update_data(height=float(message.text))
    await message.answer("Введите ваш вес (в кг):")
    await state.set_state(RegistrationForm.weight)


@router.message(RegistrationForm.weight)
async def process_weight(message: Message, state: FSMContext):
    if not message.text.isdigit() and not message.text.replace(".", "").isdigit():
        await message.answer(
            "Пожалуйста, введите корректный вес (только цифры или десятичное число).")
        return
    user_data = await state.get_data()
    register_user(
        user_id=message.from_user.id,
        full_name=user_data['full_name'],
        age=user_data['age'],
        height=user_data['height'],
        weight=float(message.text)
    )
    await state.clear()
    logger.info(f"Пользователь {message.from_user.id} успешно зарегистрировался")
    await message.answer(
        "Регистрация успешно завершена! Теперь вы можете использовать команды бота.",
        reply_markup=create_main_menu_keyboard()  # Отправляем клавиатуру после регистрации
    )
