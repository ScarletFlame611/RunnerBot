import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from bot.utils.config import BOT_TOKEN
from bot.utils.db import init_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.middlewares.registration_check import RegistrationCheckMiddleware
from bot.handlers.start import router as start_router
from bot.handlers import help, choose_menu, add_run, profile, errors, menu, last_trainings, \
    compare_two, year_statistic, achievements, chat_ai, advice, feedback, random_text
from bot.handlers.reminders import start_scheduler, stop_scheduler, enable_reminders, \
    disable_reminders

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    filename="../data/bot.log", filemode="a")
logger = logging.getLogger(__name__)


# Инициализация бота и диспетчера
async def main():
    # Логирование: начало работы
    logger.info("Инициализация базы данных")
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
    dp.include_router(feedback.router)
    dp.include_router(random_text.router)

    # Регистрация команд для напоминаний
    dp.message.register(enable_reminders, Command("enable_reminders"))
    dp.message.register(disable_reminders, Command("disable_reminders"))

    # Запуск планировщика
    await start_scheduler()

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

        # Остановка планировщика при завершении работы бота
        await stop_scheduler()


if __name__ == "__main__":
    logger.info("Запуск main()")
    asyncio.run(main())
