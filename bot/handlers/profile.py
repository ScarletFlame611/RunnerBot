from aiogram import Router, F
from aiogram.types import Message
from bot.utils.db import get_user_profile, update_profile_in_db
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Создаем клавиатуру
profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить настройки профиля", callback_data="edit_profile")]
])
router = Router()


# Создаем класс состояний
class ProfileChange(StatesGroup):
    waiting_for_name = State()  # Ожидаем имя
    waiting_for_age = State()  # Ожидаем возраст
    waiting_for_height = State()  # Ожидаем рост
    waiting_for_weight = State()  # Ожидаем вес


# Создаем клавиатуру для редактирования профиля
edit_profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить имя", callback_data="edit_name")],
    [InlineKeyboardButton(text="Изменить возраст", callback_data="edit_age")],
    [InlineKeyboardButton(text="Изменить рост", callback_data="edit_height")],
    [InlineKeyboardButton(text="Изменить вес", callback_data="edit_weight")]
])

router = Router()


@router.message(Command("profile"))
async def profile_command(message: Message):
    user_id = message.from_user.id
    profile = get_user_profile(user_id)
    if not profile:
        await message.answer(
            "Вы ещё не зарегистрированы. Используйте команду /start для регистрации.")
        return
    # Форматирование данных
    total_duration_formatted = format_duration(profile["total_duration"])
    text = (
        f"👤 *Профиль пользователя*\n"
        f"📋 *Имя:* {profile['full_name']}\n"
        f"🎂 *Возраст:* {profile['age']} лет\n"
        f"📏 *Рост:* {profile['height']} см\n"
        f"⚖️ *Вес:* {profile['weight']} кг\n"
        f"🏅 *Уровень:* {profile['level']}\n"
        f"🎯 *Цель:* {profile['goal']}\n\n"
        f"🏃 *Статистика пробежек*\n"
        f"📊 *Всего пробежек:* {profile['total_runs']}\n"
        f"📏 *Общая дистанция:* {profile['total_distance']:.2f} км\n"
        f"⏱ *Общее время:* {total_duration_formatted}"
    )
    profile_image = FSInputFile("../data/images/profile_image.jpg")
    await message.answer_photo(
        photo=profile_image,
        caption=text,
        reply_markup=profile_keyboard,
        parse_mode="Markdown"
    )


# Обработчик нажатия на кнопку "Изменить профиль"
@router.callback_query(F.data == "edit_profile")
async def edit_profile_callback(callback_query: CallbackQuery):
    # Отправляем сообщение с кнопками для выбора параметра для изменения
    await callback_query.message.answer(
        "Выберите, что вы хотите изменить:",
        reply_markup=edit_profile_keyboard
    )
    await callback_query.answer()


# Обработчик для кнопок изменения профиля
@router.callback_query(F.data.in_({"edit_name", "edit_age", "edit_height", "edit_weight"}))
async def change_profile_parameter(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    action = callback_query.data.split("_")[
        1]  # Получаем параметр (name, age, height, weight, goal)
    # Сохраняем параметр, который изменяется
    await state.update_data(parameter=action)
    # Отправляем сообщение для ввода нового значения
    await callback_query.message.answer(f"Введите новое {action}:")
    # Ввод данных для изменения, в зависимости от параметра
    if action == "name":
        await state.set_state(ProfileChange.waiting_for_name)
    elif action == "age":
        await state.set_state(ProfileChange.waiting_for_age)
    elif action == "height":
        await state.set_state(ProfileChange.waiting_for_height)
    elif action == "weight":
        await state.set_state(ProfileChange.waiting_for_weight)


# Обработчик для получения нового значения
@router.message(ProfileChange.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    new_name = message.text.strip()
    user_id = message.from_user.id
    # Проверяем, что имя состоит из букв и содержит хотя бы два слова
    if not new_name.replace(" ", "").isalpha() or len(new_name.split()) < 2:
        await message.answer(
            "Пожалуйста, введите корректное ФИО. Оно должно состоять только из букв и содержать минимум два слова."
        )
        return
    # Обновляем имя в базе данных
    update_profile_in_db(user_id, "full_name", new_name)
    await message.answer(f"Ваше имя успешно обновлено на: {new_name}.")
    await state.clear()


@router.message(ProfileChange.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    new_age = message.text
    user_id = message.from_user.id
    # Проверка, является ли введенное значение числом
    if not new_age.isdigit():
        await message.answer("Пожалуйста, введите корректный возраст (целое число).")
        return
    # Обновляем возраст в базе данных
    update_profile_in_db(user_id, "age", new_age)
    await message.answer(f"Ваш возраст успешно обновлен на {new_age}.")
    await state.clear()


@router.message(ProfileChange.waiting_for_height)
async def process_height(message: Message, state: FSMContext):
    new_height = message.text
    user_id = message.from_user.id
    # Проверка, является ли введенное значение числом
    if not new_height.isdigit():
        await message.answer("Пожалуйста, введите корректный рост в см).")
        return
    # Обновляем рост в базе данных
    update_profile_in_db(user_id, "height", new_height)
    await message.answer(f"Ваш рост успешно обновлен на {new_height}.")
    await state.clear()


@router.message(ProfileChange.waiting_for_weight)
async def process_weight(message: Message, state: FSMContext):
    new_weight = message.text
    user_id = message.from_user.id
    # Проверка, является ли введенное значение числом
    if not new_weight.isdigit():
        await message.answer("Пожалуйста, введите корректный вес (целое число в килограммах).")
        return
    # Обновляем вес в базе данных
    update_profile_in_db(user_id, "weight", new_weight)
    await message.answer(f"Ваш вес успешно обновлен на {new_weight}.")
    await state.clear()


def format_duration(total_duration: str) -> str:
    # Преобразуем строку времени в секунды
    hours, minutes, seconds = map(int, total_duration.split(":"))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    # Конвертируем секунды обратно в часы:минуты:секунды
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}"
