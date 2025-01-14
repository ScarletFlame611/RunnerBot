import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.utils.config import BOT_TOKEN
from bot.handlers import help
from bot.handlers import choose_menu
from bot.handlers import add_run
from bot.handlers import profile
from bot.handlers import errors
from bot.handlers import menu
from bot.handlers import last_trainings
from bot.handlers import compare_two
from bot.handlers import year_statistic
from bot.handlers import achievements
from bot.handlers import chat_ai
from bot.handlers import advice
from bot.handlers import random_text
from bot.handlers.start import router as start_router
from bot.middlewares.registration_check import RegistrationCheckMiddleware
from bot.utils.db import init_db
import logging

logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщения
    filename="../data/bot.log",  # Файл логов
    filemode="a",  # Режим записи (добавление)
)

# Создаем логер для текущего модуля
logger = logging.getLogger(__name__)



async def main():
    # Логирование: начало работы
    logger.info("Инициализация базы данных")

    # Инициализация базы данных
    init_db()

    # Настройка бота
    logger.info("Настройка бота и диспетчера")
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Подключение middleware
    logger.info("Подключение middleware")
    dp.message.middleware(RegistrationCheckMiddleware())

    # Регистрация хендлеров
    logger.info("Регистрация хендлеров")
    dp.include_router(start_router)
    dp.include_router(help.router)
    dp.include_router(choose_menu.router)
    dp.include_router(add_run.router)
    dp.include_router(profile.router)
    dp.include_router(errors.router)
    dp.include_router(menu.router)
    dp.include_router(last_trainings.router)
    dp.include_router(compare_two.router)
    dp.include_router(year_statistic.router)
    dp.include_router(achievements.router)
    dp.include_router(chat_ai.router)
    dp.include_router(advice.router)
    dp.include_router(random_text.router)

    # Запуск бота
    try:
        logger.info("Бот запущен! Начало polling...")
        print("Бот запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        logger.info("Закрытие сессии бота")
        await bot.session.close()


if __name__ == "__main__":
    logger.info("Запуск main()")
    asyncio.run(main())
