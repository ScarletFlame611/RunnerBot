from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def random_text_handler(message: Message):
    """Обработчик случайного текста."""
    await message.reply("Я пока не знаю, как на это ответить. Попробуйте использовать команды из меню! 😊")
