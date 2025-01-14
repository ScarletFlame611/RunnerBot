from aiogram import Router, F
from bot.utils.db import update_user_field
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# Создание inline-клавиатуры для меню выбора
def create_menu_inline_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Выбрать уровень", callback_data="menu:choose_level")
    builder.button(text="Выбрать цель", callback_data="menu:choose_goal")
    builder.adjust(1)
    return builder.as_markup()

def create_level_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Начинающий", callback_data="level:Начинающий")
    builder.button(text="Средний", callback_data="level:Средний")
    builder.button(text="Продвинутый", callback_data="level:Продвинутый")
    builder.adjust(1)  # Кнопки располагаются вертикально
    return builder.as_markup()

# Создание inline-клавиатуры для выбора цели
def create_goal_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Похудение", callback_data="goal:Похудение")
    builder.button(text="Повышение выносливости", callback_data="goal:Повышение выносливости")
    builder.button(text="Поддержание формы", callback_data="goal:Поддержание формы")
    builder.adjust(1)  # Кнопки располагаются вертикально
    return builder.as_markup()


# Обработчик команды /choose_menu
@router.message(F.text == "/choose_menu")
async def choose_menu(message: Message):
    await message.answer(
        "Что вы хотите выбрать?",
        reply_markup=create_menu_inline_keyboard()
    )

# Обработчик кнопок из меню
@router.callback_query(F.data.startswith("menu:"))
async def menu_callback(callback: CallbackQuery):
    action = callback.data.split(":")[1]
    if action == "choose_level":
        # Переход к выбору уровня
        await callback.message.edit_text(
            "Выберите ваш уровень физической подготовки:",
            reply_markup=create_level_inline_keyboard()
        )
    elif action == "choose_goal":
        # Переход к выбору цели
        await callback.message.edit_text(
            "Выберите вашу цель:",
            reply_markup=create_goal_inline_keyboard()
        )
    await callback.answer()

# Обработчик нажатия кнопки выбора уровня
@router.callback_query(F.data.startswith("level:"))
async def set_level_callback(callback: CallbackQuery):
    level = callback.data.split(":")[1]
    update_user_field(user_id=callback.from_user.id, field="level", value=level)
    await callback.message.edit_text(f"Ваш уровень '{level}' успешно сохранён!")  # Редактируем сообщение
    await callback.answer()  # Закрываем всплывающее уведомление

# Обработчик нажатия кнопки выбора цели
@router.callback_query(F.data.startswith("goal:"))
async def set_goal_callback(callback: CallbackQuery):
    goal = callback.data.split(":")[1]
    update_user_field(user_id=callback.from_user.id, field="goal", value=goal)
    await callback.message.edit_text(f"Ваша цель '{goal}' успешно сохранена!")  # Редактируем сообщение
    await callback.answer()  # Закрываем всплывающее уведомление
