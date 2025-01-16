from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n"
                         "/start - Начало работы и регистрация\n"
                         "/help - Помощь\n"
                         "/menu - Вывод меню"
                         "/choose_menu - Выбор уровня и цели\n"
                         "/profile - Просмотр своего профиля\n"
                         "/choose_menu - Изменение цели и уровня физической подготовки\n"
                         "/add_run - Добавление беговой тренировки\n"
                         "/last_trainings - Просмотр ваших последних тренировок\n"
                         "/compare_two - Сравнение двух последних тренировок\n"
                         "/year_stats - Просмотр вашей годовой статистики\n"
                         "/achievements_info - Просмотр информации о достижениях\n"
                         "/my_achievements - Просмотр своих достижений\n"
                         "/ask_ai {текст} - Общение с виртуальным тренером \n"
                         "/advice - Получения совета от виртуального тренера в зависимомти от вашего уровня подготовки и цели\n"
                         "/motivation - Получения мотивационного сообщения от виртуального тренера в зависимомти от вашего уровня подготовки и цели\n"
                         "/enable_reminders - Включение напоминаний\n"
                         "/disable_reminders - Выключение напоминаний\n"
                         "/feedback - Оставить отзыв")