import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Инициализация планировщика
scheduler = AsyncIOScheduler()
scheduled_jobs = {}

logger = logging.getLogger(__name__)


# Функция для запуска планировщика
async def start_scheduler():
    if not scheduler.running:
        logger.info("Запуск планировщика задач")
        scheduler.start()


# Функция для остановки планировщика
async def stop_scheduler():
    if scheduler.running:
        logger.info("Остановка планировщика задач")
        scheduler.shutdown(wait=False)


# Функция для отправки напоминания
async def send_reminder(user_id, bot):
    try:
        await bot.send_message(user_id, "Не забудьте про тренировку!")
    except Exception as e:
        logger.error(f"Ошибка при отправке напоминания пользователю {user_id}: {e}")


# Команда для включения напоминаний
async def enable_reminders(message):
    user_id = message.from_user.id
    if user_id in scheduled_jobs:
        await message.answer("Напоминания уже включены!")
        return
    # Добавляем задачу в планировщик
    job = scheduler.add_job(send_reminder, IntervalTrigger(days=1), args=[user_id, message.bot])
    scheduled_jobs[user_id] = job
    await message.answer("Напоминания включены! Вы будете получать напоминания о тренировках.")


# Команда для отключения напоминаний
async def disable_reminders(message):
    user_id = message.from_user.id
    if user_id not in scheduled_jobs:
        await message.answer("Напоминания не были включены.")
        return
    # Удаляем задачу из планировщика
    job = scheduled_jobs.pop(user_id)
    job.remove()
    await message.answer("Напоминания отключены.")
