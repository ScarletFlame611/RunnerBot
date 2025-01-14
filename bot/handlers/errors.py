import logging

from aiogram.exceptions import TelegramAPIError
from aiogram import Router

router = Router()
logger = logging.getLogger(__name__)


@router.errors()
async def handle_errors(update, exception):
    logger.error(f"Произошла ошибка: {exception}")
    return True
