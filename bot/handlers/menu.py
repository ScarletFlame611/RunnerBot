from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    FSInputFile
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Создаем роутер
router = Router()


# Создаем клавиатуру для меню
def create_menu_keyboard():
    builder = InlineKeyboardBuilder()

    # Первый ряд (2 кнопки)
    builder.row(
        InlineKeyboardButton(
            text="Профиль", callback_data="call_profile"
        ),
        InlineKeyboardButton(
            text="Тренировки", callback_data="call_training"
        )
    )

    # Второй ряд (2 кнопки)
    builder.row(
        InlineKeyboardButton(
            text="Достижения", callback_data="call_menu_ach"
        ),
        InlineKeyboardButton(
            text="Напоминания", callback_data="call_menu_rem"
        )
    )
    builder.row(InlineKeyboardButton(
        text="Виртуальный тренер", callback_data="call_menu_ai"
    ))

    return builder.as_markup()


# Обработчик для команды /menu
@router.message(Command("menu"))
async def menu_command(message: Message):
    profile_image = FSInputFile("../data/images/menu.jpg")
    await message.answer_photo(
        photo=profile_image,
        caption="Добро пожаловать в RunnerBot! \n\n📋 Главное меню с основными командами:",
        reply_markup=create_menu_keyboard(),
        parse_mode="Markdown"
    )


# Обработчик для кнопки "Профиль"
@router.callback_query(lambda c: c.data == "call_profile")
async def profile_button_pressed(callback: CallbackQuery):
    # Отправляем команду /profile через send_message
    await callback.message.answer(
        "👤 Команды профиля: \n\n 1️⃣ Используйте /profile для просмотра своего профиля\n\n2️⃣ Используйте /choose_menu для изменения цели и уровня физической подготовки")

    # Закрываем уведомление о нажатии кнопки
    await callback.answer()


# Обработчик для кнопки "Тренировки"
@router.callback_query(lambda c: c.data == "call_training")
async def training_button_pressed(callback: CallbackQuery):
    # Отправляем сообщение о тренировках
    await callback.message.answer(
        "🏃 Команды тренировок: \n\n"
        "1️⃣ Используйте команду /add_run для добавления беговой тренировки\n\n"
        "2️⃣ Используйте команду /last_trainings для просмотра ваших последних тренировок\n\n"
        "3️⃣ Используйте команду /compare_two для сравнения двух последних тренировок\n\n"
        "4️⃣ Используйте команду /year_stats для просмотра вашей годовой статистики\n\n"
    )

    # Закрываем уведомление о нажатии кнопки
    await callback.answer()


# Обработчик для кнопки "Профиль"
@router.callback_query(lambda c: c.data == "call_menu_ach")
async def profile_button_pressed(callback: CallbackQuery):
    # Отправляем команду /profile через send_message
    await callback.message.answer(
        "🏅 Команды достижений: \n\n 1️⃣ Используйте /achievements_info для просмотра информации о достижениях\n\n2️⃣ Используйте /my_achievements для просмотра своих достижений")

    # Закрываем уведомление о нажатии кнопки
    await callback.answer()


@router.callback_query(lambda c: c.data == "call_menu_ai")
async def profile_button_pressed(callback: CallbackQuery):
    # Отправляем команду /profile через send_message
    await callback.message.answer(
        "🏅 Команды вирутального ассистента: \n\n 1️⃣ Используйте /ask_ai {текст} для общения с виртуальным тренером\n\n2️⃣"
        " Используйте /advice для получения совета от виртуального тренера в зависимомти от вашего уровня подготовки и цели\n\n"
        "3️⃣Используйте /motivation для получения мотивационного сообщения от виртуального тренера в зависимомти от вашего уровня подготовки и цели\n\n"
        "Важно: сообщения от виртуального тренера могут быть непредсказуемыми! При возникновении важных проблем рекомендуется обратиться к специалистам!")

    # Закрываем уведомление о нажатии кнопки
    await callback.answer()


@router.callback_query(lambda c: c.data == "call_menu_rem")
async def profile_button_pressed(callback: CallbackQuery):
    # Отправляем команду /profile через send_message
    await callback.message.answer(
        "🏅Полезные команды: \n\n 1️⃣ Используйте /enable_reminders для включения напоминаний\n\n2️⃣"
        " Используйте /disable_reminders для выключения напоминаний\n\n 3️⃣Используйте /feedback для того, чтобы оставить отзыв")

    # Закрываем уведомление о нажатии кнопки
    await callback.answer()
